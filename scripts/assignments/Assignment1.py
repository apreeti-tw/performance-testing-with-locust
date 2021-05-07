from locust import constant, task, SequentialTaskSet, HttpUser
import re


class UserBehavior(SequentialTaskSet):
    @task
    def launch(self):
        with self.client.get("category/Speakers/4", name="launch", catch_response=True) as resp1:
            if "Advantage Shopping" in resp1.text:
                resp1.success()
            else:
                resp1.failure('Error launching')

    @task
    def login(self):
        with self.client.post("/accountservice/ws/AccountLoginRequest", name="login",
                              data='<?xml version="1.0" encoding="UTF-8"?><soap:Envelope '
                                   'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
                                   'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                                   'xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><AccountLoginRequest '
                                   'xmlns="com.advantage.online.store.accountservice"><email></email><loginPassword'
                                   '>Testperf1 '
                                   '</loginPassword><loginUser>testperf</loginUser></AccountLoginRequest></soap:Body'
                                   '></soap:Envelope>', catch_response=True) as resp2:
            if "200" in resp2.text:
                resp2.success()
            else:
                resp2.failure("Error logging in")

    @task
    def view_product(self):
        with self.client.get("catalog/api/v1/products/20", name="view product", catch_response=True) as resp3:
            if "200" in resp3.text:
                resp3.success()
            else:
                print(resp3)
                resp3.failure('Error viewing the product')

    @task
    def add_to_cart(self):
        with self.client.get("order/api/v1/carts/832339246/product/20/color/414141?quantity=1", name="add to cart",
                             catch_response=True) as resp4:
            if "200" in resp4.text:
                resp4.success()
                global cart_number
                print(re.search("[0-9]", resp4.text))
                cart_number = re.search("[0-9]", resp4.text)
            else:
                resp4.failure('Error adding to cart')

    @task
    def place_order(self):
        with self.client.post("order/api/v1/orders/users/832339246", name="place order",
                              data={"orderPaymentInformation": {"Transaction_AccountNumber": "112987298763",
                                                                "Transaction_Currency": "USD",
                                                                "Transaction_CustomerPhone": "",
                                                                "Transaction_MasterCredit_CVVNumber": "232",
                                                                "Transaction_MasterCredit_CardNumber": "4886488648864886",
                                                                "Transaction_MasterCredit_CustomerName": "somename",
                                                                "Transaction_MasterCredit_ExpirationDate": "122027",
                                                                "Transaction_PaymentMethod": "MasterCredit",
                                                                "Transaction_ReferenceNumber": "0",
                                                                "Transaction_SafePay_Password": "",
                                                                "Transaction_SafePay_UserName": "",
                                                                "Transaction_TransactionDate": "5052021",
                                                                "Transaction_Type": "PAYMENT"},
                                    "orderShippingInformation": {"Shipping_Address_Address": "",
                                                                 "Shipping_Address_City": "",
                                                                 "Shipping_Address_CountryCode": "40",
                                                                 "Shipping_Address_CustomerName": "testperf ",
                                                                 "Shipping_Address_CustomerPhone": "",
                                                                 "Shipping_Address_PostalCode": "",
                                                                 "Shipping_Address_State": "", "Shipping_Cost": "809.97",
                                                                 "Shipping_NumberOfProducts": "3",
                                                                 "Shipping_TrackingNumber": "0"}, "purchasedProducts": [
                                      {"hexColor": "414141", "productId": "20", "quantity": "3", "hasWarranty": "false"}]},
                              catch_response=True) as resp4:
            if "200" in resp4.text:
                resp4.success()
            else:
                resp4.failure('Error placing the order')


class Main(HttpUser):
    wait_time = constant(3)
    host = "http://advantageonlineshopping.com/#/"
    tasks = [UserBehavior]
