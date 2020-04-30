# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hashlib

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

import logging
import hashlib
from urllib.parse import urlparse

_logger = logging.getLogger(__name__)


class PaymentAcquirerPayumoney(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('payumoney', 'PayUmoney')])
#    payumoney_merchant_key = fields.Char(string='Merchant Key', required_if_provider='payumoney', groups='base.group_user')
#    payumoney_merchant_salt = fields.Char(string='Merchant Salt', required_if_provider='payumoney', groups='base.group_user')
    payumoney_merchant_key = fields.Char(string='Merchant Key(merchantid)', required_if_provider='payumoney', groups='base.group_user')
    payumoney_merchant_salt = fields.Char(string='Merchant Salt(security_key)', required_if_provider='payumoney', groups='base.group_user')

    def _get_payumoney_urls(self, environment):
        """ PayUmoney URLs"""
        if environment == 'prod':
#            return {'payumoney_form_url': 'https://secure.payu.in/_payment'}
             return {'payumoney_form_url': 'https://pay2.hoogahome.com/payment/go2pay.php'}
        else:
#            return {'payumoney_form_url': 'https://test.payu.in/_payment'}
             return {'payumoney_form_url': 'https://pay2.hoogahome.com/payment_test/go2pay.php'}

    def _payumoney_generate_sign(self, inout, values):
        """ Generate the shasign for incoming or outgoing communications.
        :param self: the self browse record. It should have a shakey in shakey out
        :param string inout: 'in' (odoo contacting payumoney) or 'out' (payumoney
                             contacting odoo).
        :param dict values: transaction values

        :return string: shasign
        """
        if inout not in ('in', 'out'):
            raise Exception("Type must be 'in' or 'out'")

        if inout == 'in':
#            keys = "key|txnid|amount|productinfo|firstname|email|udf1|||||||||".split('|')
#            sign = ''.join('%s|' % (values.get(k) or '') for k in keys)
#            sign += self.payumoney_merchant_salt or ''
            security_key = self.payumoney_merchant_salt 
            price = '{amo:.0f}'.format(amo=values['amount'])
            sign = '{sk}{oi}{pr}'.format(sk=security_key, oi=values['txnid'], pr=price)
            _logger.info('$security_key{oi}{pr}'.format(oi=values['txnid'], pr=price))
        else:
#            keys = "|status||||||||||udf1|email|firstname|productinfo|amount|txnid".split('|')
#            sign = ''.join('%s|' % (values.get(k) or '') for k in keys)
#            sign = self.payumoney_merchant_salt + sign + self.payumoney_merchant_key
            security_key = self.payumoney_merchant_salt 
            sign = '{sk}{status}{txnid}{authcode}'.format(sk=security_key, 
                                                                status=values['status'],
                                                                txnid=values['txnid'], 
                                                                authcode=values['authcode'])
            

        shasign = hashlib.sha256(sign.encode('ISO-8859-1')).hexdigest()
#        shasign = hashlib.sha512(sign.encode('utf-8')).hexdigest()
        _logger.info('sign: {sign} hash: {h}'.format(sign=sign, h=shasign))
        return shasign

    @api.multi
    def payumoney_form_generate_values(self, values):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        #-- replace proto to https if it is a domain name (not ip)
        hostport = urlparse(base_url).netloc
        if not all( [s.isdigit() for s in hostport.split(':')[0].split('.')] ):
            base_url = base_url.replace('http://', 'https://')

        payumoney_values = dict(values,
#                                key=self.payumoney_merchant_key,
                                txnid=values['reference'],
                                amount=values['amount'],
                                productinfo=values['reference'],
                                firstname=values.get('partner_name'),
                                email=values.get('partner_email'),
                                phone=values.get('partner_phone'),
                                service_provider='payu_paisa',
                                surl=urls.url_join(base_url, '/payment/payumoney/return'),
                                furl=urls.url_join(base_url, '/payment/payumoney/error'),
                                curl=urls.url_join(base_url, '/payment/payumoney/cancel'),
                                #-- parameters for go2pay.php
                                oid=values['reference'],
                                price='{amo:.0f}'.format(amo=values['amount']),
                                uname=values.get('partner_name'),
                                com='hgh',
                                isInstallment='true'
                                )

        payumoney_values['udf1'] = payumoney_values.pop('return_url', '/')
#        payumoney_values['hash'] = self._payumoney_generate_sign('in', payumoney_values)
        payumoney_values['key'] = self._payumoney_generate_sign('in', payumoney_values)
        return payumoney_values

    @api.multi
    def payumoney_get_form_action_url(self):
        self.ensure_one()
        return self._get_payumoney_urls(self.environment)['payumoney_form_url']


class PaymentTransactionPayumoney(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _payumoney_form_get_tx_from_data(self, data):
        _logger.info('_payumoney_form_get_tx_from_data()')
        """ Given a data dict coming from payumoney, verify it and find the related
        transaction record. """
        reference = data.get('txnid')
#        pay_id = data.get('mihpayid')
        authcode = data.get('authcode')
        shasign = data.get('hash')
#        if not reference or not pay_id or not shasign:
#            raise ValidationError(_('PayUmoney: received data with missing reference (%s) or pay_id (%s) or shashign (%s)') % (reference, pay_id, shasign))
        if not reference or not authcode or not shasign:
            raise ValidationError(_('PayUmoney: received data with missing reference (%s) or authcode (%s) or shashign (%s)') % (reference, authcode, shasign))

        transaction = self.search([('reference', '=', reference)])

        if not transaction:
            error_msg = (_('PayUmoney: received data for reference %s; no order found') % (reference))
            raise ValidationError(error_msg)
        elif len(transaction) > 1:
            error_msg = (_('PayUmoney: received data for reference %s; multiple orders found') % (reference))
            raise ValidationError(error_msg)

        #verify shasign
        shasign_check = transaction.acquirer_id._payumoney_generate_sign('out', data)
#TODO...
        if shasign_check.upper() != shasign.upper():
            raise ValidationError(_('PayUmoney: invalid shasign, received %s, computed %s, for data %s') % (shasign, shasign_check, data))
        return transaction

    @api.multi
    def _payumoney_form_get_invalid_parameters(self, data):
        _logger.info('_payumoney_form_get_invalid_parameters()')
        invalid_parameters = []

#        if self.acquirer_reference and data.get('mihpayid') != self.acquirer_reference:
#            invalid_parameters.append(
#                ('Transaction Id', data.get('mihpayid'), self.acquirer_reference))
        #check what is buyed
        if float_compare(float(data.get('amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('Amount', data.get('amount'), '%.2f' % self.amount))

        return invalid_parameters

    @api.multi
    def _payumoney_form_validate(self, data):
        _logger.info('_payumoney_form_validate')
        status = data.get('status')
        result = self.write({
            'acquirer_reference': data.get('payuMoneyId'),
            'date': fields.Datetime.now(),
        })
        if status == 'success':
            self._set_transaction_done()
        elif status != 'pending':
            self._set_transaction_cancel()
        else:
            self._set_transaction_pending()
        return result
