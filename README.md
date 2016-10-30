# specialname


-------
# ToDos

- share to fb/wx
- algorithm
- intro/example on index page
- UI
- reading/writing of name
- diff config of sandbox/production
- store selected chars to order when create payment
- use admin to manage product prices
- nginx + gunicorn


-------

# Access Token

curl -v https://api.sandbox.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "AaaPugJL3aRgMCXPBsyF8kB0CWTp4KIv8qHHIrT0RCyfC9sFOdU475Dhp-O_Qrz1cVm_afuMEnlvcYTf:ECKE9pvmGa_IGKUQz35vt4a_Lsv71y0OxBRLRgvQsSQJR7c0V9UP2Bu80nz_hVlo0mDhIlKk8fj8hAi-" \
  -d "grant_type=client_credentials"






# Create a payment

curl -v https://api.sandbox.paypal.com/v1/payments/payment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <Access-Token>" \
  -d '{
  "intent":"sale",
  "redirect_urls":{
    "return_url":"http://example.com/your_redirect_url.html",
    "cancel_url":"http://example.com/your_cancel_url.html"
  },
  "payer":{
    "payment_method":"paypal"
  },
  "transactions":[
    {
      "amount":{
        "total":"7.47",
        "currency":"USD"
      }
    }
  ]
}'

    {
      "id":"PAY-6RV70583SB702805EKEYSZ6Y",
      "create_time":"2013-03-01T22:34:35Z",
      "update_time":"2013-03-01T22:34:36Z",
      "state":"created",
      "intent":"sale",
      "payer":{
        "payment_method":"paypal"
      },
      "transactions":[
        {
          "amount":{
            "total":"7.47",
            "currency":"USD",
            "details":{
              "subtotal":"7.47"
            }
          },
          "description":"This is the payment transaction description."
        }
      ],
      "links":[
        {
          "href":"https://api.sandbox.paypal.com/v1/payments/payment/PAY-6RV70583SB702805EKEYSZ6Y",
          "rel":"self",
          "method":"GET"
        },
        {
          "href":"https://www.sandbox.paypal.com/webscr?cmd=_express-checkout&token=EC-60U79048BN7719609",
          "rel":"approval_url",
          "method":"REDIRECT"
        },
        {
          "href":"https://api.sandbox.paypal.com/v1/payments/payment/PAY-6RV70583SB702805EKEYSZ6Y/execute",
          "rel":"execute",
          "method":"POST"
        }
      ]
    }

# Get payment approval
Direct the user to the `approval_url`, When the user approves the payment, PayPal redirects the user to the `return_url`

# Execute the payment
        
    http://return_url?paymentId=PAY-6RV70583SB702805EKEYSZ6Y&token=EC-60U79048BN7719609&PayerID=7E7MGXCWTTKK2

curl https://api.sandbox.paypal.com/v1/payments/payment/PAY-6RV70583SB702805EKEYSZ6Y/execute/ \
  -v \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer Access-Token' \
  -d '{ "payer_id" : "7E7MGXCWTTKK2" }'
  

