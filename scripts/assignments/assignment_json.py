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

    @task(2)
    def unlock_barn(self):
        with self.client.post("/api/" + self.user_id + "/barn-unlock",
                              name="unlock barn",
                              headers={"Authorization": "Bearer " + self.token},
                              catch_response=True) as resp:
            if "\"success\":true" in resp.text:
                resp.success()
            else:
                resp.failure("Barn unlock failed")

    @task(1)
    def self_interrupt(self):
        self.interrupt()


class MyUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://coop.apps.symfonycasts.com"
    tasks = [UserBehavior]


class ReqRes(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = ""

    @task(3)
    def create_user(self):
        with self.client.post("api/users",
                              name="create user",
                              json={
                                  "name": "morpheus",
                                  "job": "leader"
                              },
                              catch_response=True) as resp:
            if "\"id\":" in resp.text:
                resp.success()
                self.user_id = str(resp.json()["id"])
            else:
                resp.failure("user creation failed")

    @task(2)
    def delete_user(self):
        with self.client.delete("api/users/"+self.user_id,
                                name="delete user",
                                catch_response=True) as resp:
            if str(resp.status_code) == '204':
                resp.success()
            else:
                resp.failure("User deletion failed")

    @task(1)
    def self_interrupt(self):
        self.interrupt()


class MyReqRes(HttpUser):
    wait_time = between(1, 3)
    host = "https://reqres.in/"
    tasks = [ReqRes]
