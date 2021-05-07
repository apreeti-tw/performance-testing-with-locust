from locust import HttpUser, task, constant, SequentialTaskSet


class Setup(SequentialTaskSet):
    @task
    def launch(self):
        with self.client.get("category/Speakers/4", name="launch_speakers", catch_response=True) as response1:
            if "Advantage Shopping" in response1.text:
                response1.success()
            else:
                response1.failure("Failed to launch url")


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
                              '></soap:Envelope>', catch_response=True) as response:
            if "success" in response.text:
                response.success()
            else:
                response.failure("Failed to login")



class HttpDemo(HttpUser):
    wait_time = constant(3)
    host = "http://advantageonlineshopping.com/#/"
    tasks = [Setup]
