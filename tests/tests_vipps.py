import os
import unittest

from vipps import VippsEcomApi, VippsSignupApi

import env


VIPPS_CLIENT_ID = env.VIPPS_CLIENT_ID
VIPPS_CLIENT_SECRET = env.VIPPS_CLIENT_SECRET
VIPPS_SUBSCRIPTION_KEY = env.VIPPS_SUBSCRIPTION_KEY
VIPPS_MERCHANT_SERIAL_NUMBER = env.VIPPS_MERCHANT_SERIAL_NUMBER
VIPPS_SERVER = env.VIPPS_SERVER
VIPPS_CALLBACK_PREFIX = env.VIPPS_CALLBACK_PREFIX
VIPPS_FALLBACK_URL = env.VIPPS_FALLBACK_URL


class TestVippsEcomApi(unittest.TestCase):
    def setUp(self):
        self.client = VippsEcomApi(
            client_id=VIPPS_CLIENT_ID,
            client_secret=VIPPS_CLIENT_SECRET,
            vipps_subscription_key=VIPPS_SUBSCRIPTION_KEY,
            merchant_serial_number=VIPPS_MERCHANT_SERIAL_NUMBER,
            vipps_server=VIPPS_SERVER,
            callback_prefix=VIPPS_CALLBACK_PREFIX,
            fall_back=VIPPS_FALLBACK_URL,
        )
        self.order_id = "acme-shop-123-order123abc"
        self.amount = 151
        self.transaction_text = "One pair of Vipps socks"

    def test_initiate(self):
        initiate = self.client.init_payment(
            order_id=self.order_id,
            amount=self.amount,
            transaction_text=self.transaction_text,
        )

        self.assertTrue(initiate.get("orderId") == self.order_id)
        self.assertTrue(initiate.get("url"))
