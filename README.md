# Vipps Python Library

The Unofficial* Vipps Python library provides convenient access to the [Vipps AS API](https://github.com/vippsas) from applications written in the Python language.

## Currently Supports:
 * [Vipps eCom API v2](https://github.com/vippsas/vipps-ecom-api)
 * [Vipps Signup API v1](https://github.com/vippsas/vipps-signup-api)

## Documentation
See the [Vipps Developers resources](https://github.com/vippsas/vipps-developers)

## Installation
`pip install vipps`

## Requirements
 Test on `Python3.7`
 * Python 3.7
 * requests 2+

## Usage
Vipps eCommerce API version 2. Initiate payment and get redirect Url:
```py
from vipps import VippsEcomApi


payment = VippsEcomApi(
    client_id="fb492b5e-7907-4d83-ba20-c7fb60ca35de",
    client_secret="Y8Kteew6GE2ZmeycEt6egg==",
    vipps_subscription_key="0f14ebcab0ec4b29ae0cb90d91b4a84a",
    merchant_serial_number="123456",
    vipps_server="https://apitest.vipps.no",
    callback_prefix="https://example.com/vipps/callbacks-for-payment-updates"
    fall_back="https://example.com/vipps/fallback-order-result-page/acme-shop-123-order123abc"
)

# Initiate payment
initiate = payment.init_payment(
    order_id="acme-shop-123-order123abc",
    amount=200,
    transaction_text="One pair of Vipps socks",
)

# Redirect Url
redirect_url = initiate.get("url")

# Capture Payment
capture = payment.capture_payment(
    order_id="acme-shop-123-order123abc",
    amount=200,
    transaction_text="One pair of Vipps socks",
)

# Cancel Payment
cancel = payment.cancel_payment(
    order_id="acme-shop-123-order123abc",
    transaction_text="One pair of Vipps socks",
)

# Refund Payment
refund = payment.refund_payment(
    order_id="acme-shop-123-order123abc",
    amount=200,
    transaction_text="One pair of Vipps socks",
)

# Payment details
details = payment.details_payment(
    order_id="acme-shop-123-order123abc"
)
```

## *Unofficial
I am not affiliate or associate of the Vipps AS in any possible way. Used publicly available info to build this software. 


## TODO
* Vipps Login API
* Test Coverage
* Docs for all endpoints
