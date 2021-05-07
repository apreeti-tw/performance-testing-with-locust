from locust import HttpUser, task, constant


class HttpDemo(HttpUser):
    wait_time = constant(3)
    host = "http://advantageonlineshopping.com/#/"

    @task
    def http_get(self):
        self.client.get("category/Speakers/4", name="speakers")
