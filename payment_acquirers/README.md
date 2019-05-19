## payUmoney
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
