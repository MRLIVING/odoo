
## go2pay
### go2pay.php
```
== General ==
Request URL: https://${PAY_HOST}/payment/go2pay.php
Request Method: POST
Status Code: 200 
Remote Address: 52.68.106.16:443
Referrer Policy: no-referrer-when-downgrade

== Request Header ==
authority: pay.hoogahome.com
:method: POST
:path: /payment/go2pay.php
:scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
cache-control: max-age=0
content-length: 619
content-type: application/x-www-form-urlencoded
cookie: _ga=GA1.2.338646521.1555392120; _fbp=fb.1.1558184701814.540219740
origin: http://${ODOO_HOST}
referer: http://${ODOO_HOST}/shop/payment
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36

==  Request Form Data ==
txnid: SO012-1
amount: 5250.0
productinfo: SO012-1
firstname: adminweb
email: eric@mrliving.com.tw
phone: 0922641978
service_provider: payu_paisa
hash: f1c32c510c465efcfb5eb3c1e5d72599d709918ccebcf85b16de94888b2b5213a552f6bf171c5a02d0a90203b183b0cc5aeafea60adf13480716d3c62bb18d3c
surl: http://${ODOO_HOST}/payment/payumoney/return
furl: http://${ODOO_HOST}/payment/payumoney/error
curl: http://${ODOO_HOST}/payment/payumoney/cancel
udf1: /payment/process
oid: SO012-1
price: 5250
uname: adminweb
key: 86eb159b42d995622f5f3e4803d14767717286aed2c01ee67092d68ae91889f8

```

## [payUmoney](https://www.payumoney.com/)
### /payment/payumoney/return
```
== General ==
Request URL: http://${HOSTNAME}/payment/payumoney/return
Request Method: POST
Status Code: 302 FOUND
Remote Address: 35.229.165.196:8069
Referrer Policy: no-referrer-when-downgrade

== Request Header ==
POST /payment/payumoney/return HTTP/1.1
Host: ${HOSTNAME}
Connection: keep-alive
Content-Length: 1092
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: null
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: frontend_lang=zh_TW; session_id=5fe0ebfb7854bf869c76eb12ead91c61aa31a5c8; im_livechat_history=["/","/web/login","/shop","/shop/product/duke-dinning-table-15","/shop/cart","/shop/payment","/payment/process","/shop/confirmation","/shop/product/chacha-bed-side-table-14"]

== Request Form Data ==
isConsentPayment: 0
mihpayid: 403993715519371381
mode: CC
status: success
unmappedstatus: captured
key: rjQUPktU
txnid: SO005-1
amount: 2625.00
addedon: 2019-05-19 06:59:47
productinfo: SO005-1
firstname: adminweb
lastname: 
address1: 
address2: 
city: 
state: 
country: 
zipcode: 
email: eva@morning.com
phone: 9922641978
udf1: /payment/process
udf2: 
udf3: 
udf4: 
udf5: 
udf6: 
udf7: 
udf8: 
udf9: 
udf10: 
hash: 5e68f74c10d33f200796b6cf0c936a5f71f6692459da020a7bd540a583cffd60ee83cb8c4d7ff8318b315b010b0590f5e7884ba159767a6e6964ddc45d97059e
field1: 691158
field2: 153329
field3: 20190519
field4: MC
field5: 399606001382
field6: 00
field7: 0
field8: 3DS
field9:  Verification of Secure Hash Failed: E700 -- Approved -- Transaction Successful -- Unable to be determined--E000
PG_TYPE: AXISPG
encryptedPaymentId: 991E2E94B016BD5D6B15B175BDF8BC5B
bank_ref_num: 691158
bankcode: CC
error: E000
error_Message: No Error
name_on_card: eva
cardnum: 512345XXXXXX2346
cardhash: This field is no longer supported in postback params.
amount_split: {"PAYU":"2625.00"}
payuMoneyId: 1112043521
discount: 0.00
net_amount_debit: 2625
```

## Reference
* [TapPay doc](https://docs.tappaysdk.com/tutorial/)
  * [Test Account](https://docs.tappaysdk.com/tutorial/zh/reference.html#test-account)
* [10 分鐘串接 TapPay 金流付錢去!](https://ithelp.ithome.com.tw/articles/10192314)
* [Odoo 綠界金流模組](https://github.com/ECPay/Odoo_Payment)
* [PayUmoney - test salt & test key](https://developer.payumoney.com/general/)
