import logging
import requests


logger = logging.getLogger("vipps")


class VippsEcomApi:
    """Vipps eCommerce API version 2"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        vipps_subscription_key: str,
        merchant_serial_number: str,
        vipps_server: str,
        callback_prefix: str,
        fall_back: str,
        access_token: str = None,
        vipps_system_name: str = None,
        vipps_system_version: str = None,
        vipps_system_plugin_name: str = None,
        vipps_system_plugin_version: str = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.vipps_subscription_key = vipps_subscription_key
        self.merchant_serial_number = merchant_serial_number
        self.vipps_server = vipps_server
        self.callback_prefix = callback_prefix
        self.fall_back = fall_back
        self._access_token = access_token
        self.vipps_system_name = vipps_system_name
        self.vipps_system_version = vipps_system_version
        self.vipps_system_plugin_name = vipps_system_plugin_name
        self.vipps_system_plugin_version = vipps_system_plugin_version

    def _make_call(self, method: str, endpoint: str, headers: dict, json=None) -> dict:
        """Used in main api calls

        Args:
            method (str): post, get or put
            endpoint (str): endpoint to make a call
            headers (dict): headres for a call
            json (dict, optional): body of the request. Defaults to None.

        Returns:
            dict: response body as a dict
        """

        if method == "get":
            req = requests.get
        elif method == "post":
            req = requests.post
        elif method == "put":
            req = requests.put

        url = f"{self.vipps_server}{endpoint}"

        logger.debug(f"VippsEcomApi._make_call: making api call to the url: {url}")

        r = req(url, headers=headers, json=json)

        if r.ok:
            return r.json()

        r.raise_for_status()

    def _get_access_token(self) -> None:
        """makes api call to get a Barer Access Token"""

        endpoint = "/accesstoken/get"
        headers = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "Ocp-Apim-Subscription-Key": self.vipps_subscription_key,
        }

        r = self._make_call(method="post", endpoint=endpoint, headers=headers)

        self._access_token = r.get("access_token", None)

    @property
    def access_token(self) -> str:
        """Checks if access token already obtained

        Returns:
            str: Access Token
        """
        if self._access_token is None:
            self._get_access_token()
        return self._access_token

    @property
    def headers(self) -> dict:
        """Base headers used in main api calls

        Returns:
            dict: headers
        """

        kwargs = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": self.vipps_subscription_key,
            "Merchant-Serial-Number": self.merchant_serial_number,
            "Vipps-System-Name": self.vipps_system_name,
            "Vipps-System-Version": self.vipps_system_version,
            "Vipps-System-Plugin-Name": self.vipps_system_plugin_name,
            "Vipps-System-Plugin-Version": self.vipps_system_plugin_version,
        }
        return kwargs

    def init_payment(self, order_id: str, amount: int, transaction_text: str) -> dict:
        """Initiate
        https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md#initiate

        Args:
            order_id (str): Order id
            amount (int): amount in cents
            transaction_text (str): information about transaction

        Returns:
            dict: responce body as a dict
        """

        endpoint = "/ecomm/v2/payments"

        data = {
            "customerInfo": {},
            "merchantInfo": {
                "merchantSerialNumber": self.merchant_serial_number,
                "callbackPrefix": self.callback_prefix,
                "fallBack": f"{self.fall_back}/{order_id}",
            },
            "transaction": {
                "orderId": order_id,
                "amount": amount,
                "transactionText": transaction_text,
            },
        }

        return self._make_call(
            method="post", endpoint=endpoint, headers=self.headers, json=data
        )

    def capture_payment(
        self, order_id: str, amount: int, transaction_text: str
    ) -> dict:
        """Capture
        https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md#capture

        Args:
            order_id (str): Order id
            amount (int): amount in cents
            transaction_text (str): information about transaction

        Returns:
            dict: responce body as a dict
        """

        endpoint = f"/ecomm/v2/payments/{order_id}/capture"

        headers = self.headers
        headers.update({"orderId": order_id})

        data = {
            "merchantInfo": {"merchantSerialNumber": self.merchant_serial_number},
            "transaction": {"amount": amount, "transactionText": transaction_text},
        }

        return self._make_call(
            method="post", endpoint=endpoint, headers=headers, json=data
        )

    def cancel_payment(self, order_id: str, transaction_text: str) -> dict:
        """Cancel
        https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md#cancel

        Args:
            order_id (str): Order id
            transaction_text (str): information about transaction

        Returns:
            dict: responce body as a dict
        """

        endpoint = f"/ecomm/v2/payments/{order_id}/cancel"

        headers = self.headers
        headers.update({"orderId": order_id})

        data = {
            "merchantInfo": {"merchantSerialNumber": self.merchant_serial_number},
            "transaction": {"transactionText": transaction_text},
        }

        return self._make_call(
            method="put", endpoint=endpoint, headers=headers, json=data
        )

    def refund_payment(self, order_id: str, amount: int, transaction_text: str) -> dict:
        """Refund
        https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md#refund

        Args:
            order_id (str): Order id
            amount (int): amount in cents
            transaction_text (str): information about transaction

        Returns:
            dict: responce body as a dict
        """

        endpoint = f"/ecomm/v2/payments/{order_id}/refund"
        data = {
            "merchantInfo": {"merchantSerialNumber": self.merchant_serial_number},
            "transaction": {
                "amount": amount,
                "transactionText": transaction_text,
            },
        }

        return self._make_call(
            method="post", endpoint=endpoint, headers=self.headers, json=data
        )

    def details_payment(self, order_id: str) -> dict:
        """Details
        https://github.com/vippsas/vipps-ecom-api/blob/master/vipps-ecom-api.md#get-payment-details

        Args:
            order_id (str): Order id

        Returns:
            dict: responce body as a dict
        """

        endpoint = f"/ecomm/v2/payments/{order_id}/details"

        return self._make_call(method="get", endpoint=endpoint, headers=self.headers)

    def force_approve_payment(
        self, order_id: str, customer_phone_number: str, token: str
    ) -> dict:
        """This endpoint allows developers to approve a payment through the Vipps eCom API without
        the use of the Vipps app. This is useful for automated testing. Express checkout is not
        supported for this endpoint. The endpoint is only available in our Test environment.
        Attempted use of the endpoint in production is not allowed, and will fail.

        Args:
            order_id (str): Order id
            customer_phone_number (str): Some phone number for testing
            token (str): token from the URL in initialize response

        Returns:
            dict: responce body as a dict
        """
        endpoint = f"/ecomm/v2/integration-test/payments/{order_id}/approve"
        data = {"customerPhoneNumber": customer_phone_number, "token": token}
        url = f"{self.vipps_server}{endpoint}"

        logger.debug(f"VippsEcomApi._make_call: making api call to the url: {url}")

        r = requests.post(url, headers=self.headers, json=data)

        if r.ok:
            return r

        r.raise_for_status()


class VippsSignupApi:
    """Vipps Signup API"""

    def __init__(
        self,
        vipps_server: str,
        orgnumber: str,
        partner_id: str,
        subscription_package_id: str,
        merchant_website_url: str,
        signup_callback_token: str,
        signup_callback_url: str,
        form_type: str,
    ):
        self.vipps_server = vipps_server
        self.orgnumber = orgnumber
        self.partner_id = partner_id
        self.subscription_package_id = subscription_package_id
        self.merchant_website_url = merchant_website_url
        self.signup_callback_token = signup_callback_token
        self.signup_callback_url = signup_callback_url
        self.form_type = form_type

    def partial_signup(self) -> dict:

        endpoint = "/v1/partial/signup"
        url = f"{self.vipps_server}{endpoint}"

        data = {
            "orgnumber": self.orgnumber,
            "partnerId": self.partner_id,
            "subscriptionPackageId": self.subscription_package_id,
            "merchantWebsiteUrl": self.merchant_website_url,
            "signupCallbackToken": self.signup_callback_token,
            "signupCallbackUrl": self.signup_callback_url,
            "form-type": self.form_type,
        }

        logger.debug(
            f"VippsSignupApi.partial_signup: making api call to the url: {url}"
        )

        r = requests.post(url, json=data)

        if r.ok:
            return r.json()

        r.raise_for_status()
