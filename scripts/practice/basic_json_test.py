from locust import between, task, HttpUser, SequentialTaskSet


class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.token = ""
        self.user_id = "1711"

    def on_start(self):
        with self.client.post("/token",
                              name="retrieve token",
                              data={"client_id": "",
                                    "client_secret": "",
                                    "grant_type": "client_credentials"},
                              catch_response=True) as resp:
            if "access_token" in resp.text:
                self.token = resp.json()["access_token"]
                resp.success()
            else:
                resp.failure("Token generation failed")

    @task
    def unlock_barn(self):
        with self.client.post("/api/"+self.user_id+"/barn-unlock",
                              name="unlock barn",
                              headers={"Authorization": "Bearer "+self.token},
                              catch_response=True) as resp:
            if "\"success\":true" in resp.text:
                resp.success()
            else:
                resp.failure("Barn unlock failed")


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://coop.apps.symfonycasts.com"
    tasks = [UserBehavior]
