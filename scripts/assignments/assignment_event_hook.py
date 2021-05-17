import re
import socket

from locust import SequentialTaskSet, constant, HttpUser, events, task

hostname = socket.gethostname()


def success_handler(request_type, name, response_time, response_length, **kwargs):
    success_template = '"hostname": {}, "request_type": {}, "name": {}, "result": OK, "response_time": {}, ' \
                       '"response_length": {}'.format(
        hostname, request_type, name, response_time, response_length)
    print(success_template)


def failure_handler(request_type, name, response_time, response_length, exception, **kwargs):
    failure_template = '"hostname": {}, "request_type": {}, "name": {}, "result": Not OK, "response_time": {}, ' \
                       '"response_length": {}, "exception": {}'.format(
        hostname, request_type, name, response_time, response_length, exception)
    print(failure_template)


events.request_success.add_listener(success_handler)
events.request_failure.add_listener(failure_handler)


class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super(UserBehavior, self).__init__(parent)
        self.jsession_id = ""
        self.user_filter_session = ""
        self.view_state = ""

    def on_start(self):
        resp = self.client.get("/InsuranceWebExtJS", name="launch url")
        self.jsession_id = resp.cookies["JSESSIONID"]
        self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]

    @task
    def login(self):
        with self.client.post("/InsuranceWebExtJS/index.jsf",
                              name="login",
                              cookies={"JSESSIONID": self.jsession_id},
                              data={"login-form": "login-form", "login-form:email": "",
                                    "login-form:password": "", "login-form:login.x": "66",
                                    "login-form:login.y": "10", "javax.faces.ViewState": self.view_state},
                              catch_response=True) as resp1:
            if "Logged in as" in resp1.text:
                resp1.success()
                self.user_filter_session = resp1.cookies["UserSessionFilter.sessionId"]
                print("User logged in: ")
            else:
                resp1.failure("Error logging in")
                print("Error logging in: ")


class MyUser(HttpUser):
    wait_time = constant(3)
    host = "http://demo.borland.com"
    tasks = [UserBehavior]
