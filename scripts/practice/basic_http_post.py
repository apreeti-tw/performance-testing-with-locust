from locust import HttpUser, task, constant, SequentialTaskSet


class Setup(SequentialTaskSet):
    @task
    def launch(self):
        resp = self.client.get("category/Speakers/4", name="launch_speakers")
        print(resp)

    @task
    def login(self):
        self.client.post("/accountservice/ws/AccountLoginRequest", name="login",
                         data='<?xml version="1.0" encoding="UTF-8"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><AccountLoginRequest xmlns="com.advantage.online.store.accountservice"><email></email><loginPassword>Testperf1</loginPassword><loginUser>testperf</loginUser></AccountLoginRequest></soap:Body></soap:Envelope>')


class HttpDemo(HttpUser):
    wait_time = constant(3)
    host = "http://advantageonlineshopping.com/#/"
    tasks = [Setup]
