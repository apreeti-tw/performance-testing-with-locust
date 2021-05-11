from locust import SequentialTaskSet, HttpUser, task, between
import os
import sys
import re
import random
from utilities.csv_reader import CSVReader


root_dir = os.path.dirname(os.path.abspath(__file__))
print(root_dir)
sys.path.append(root_dir)
data_folder = os.path.join(root_dir, "data")
file_folder = os.path.join(data_folder, "credentials.csv")
my_reader = CSVReader(file_folder).readCSV()


class UserBehavior(SequentialTaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jsession_id = ""
        self.user_session_filter = ""
        self.view_state = ""
        self.username = ""
        self.password = ""

    def on_start(self):
        self.username = random.choice(my_reader)['username']
        self.password = random.choice(my_reader)['password']
        print(self.username, self.password)
        resp = self.client.get("/InsuranceWebExtJS", name="launch")
        self.jsession_id = resp.cookies["JSESSIONID"]
        self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]

        with self.client.post("/InsuranceWebExtJS/index.jsf", name="login",
                              data={"login-form": "login-form", "login-form:email": self.username
                                  , "login-form:password": self.password, "login-form:login.x": "57"
                                  , "login-form:login.y": "10", "javax.faces.ViewState": self.view_state},
                              cookies={"JSESSIONID": self.jsession_id}, catch_response=True) as resp2:
            if "Logged in" in resp2.text:
                resp2.success()
                print("User logged in")
                self.user_session_filter = resp2.cookies["UserSessionFilter.sessionId"]
            else:
                resp2.failure("Error logging in")

    @task
    def select_autoquote(self):
        with self.client.get("/InsuranceWebExtJS/quote_auto.jsf", name="select autoquote",
                             cookies={"JSESSIONID": self.jsession_id,
                                      "UserSessionFilter.sessionId": self.user_session_filter},
                             catch_response=True) as resp:
            if "Get Instant Auto Quote" in resp.text:
                resp.success()
                print("Autoquote selected")
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
            else:
                resp.failure("Autoquote selection failed")

    @task
    def personal_details_1(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto.jsf", name="getinstantquote_1",
                              data={"autoquote": "autoquote",
                                    "autoquote:zipcode": "00000000",
                                    "autoquote:e-mail": "qamile2@gmail.com",
                                    "autoquote:vehicle": "car",
                                    "autoquote:next.x": "38",
                                    "autoquote:next.y": "10",
                                    "javax.faces.ViewState": self.view_state},
                              cookies={'JSESSIONID': self.jsession_id,
                                       'UserSessionFilter.sessionId':
                                           self.user_session_filter},
                              catch_response=True) as resp:
            if "You're almost done!" in resp.text:
                resp.success()
                print("Instant Auto Quote - Continued")
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
            else:
                resp.failure("Instant Auto Quote")

    @task
    def personal_details_2(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto2.jsf", name="getinstantquote_2",
                              cookies={"JSESSIONID": self.jsession_id,
                                       "UserSessionFilter.sessionId": self.user_session_filter},
                              data={"autoquote": "autoquote",
                                    "autoquote:age": "0",
                                    "autoquote:gender": "Male",
                                    "autoquote:type": "Excellent",
                                    "autoquote:next.x": "35",
                                    "autoquote:next.y": "7",
                                    "javax.faces.ViewState": self.view_state}, catch_response=True) as resp:
            if "Last Screen!" in resp.text:
                resp.success()
                print("Last Screen!")
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
            else:
                resp.failure("Last Screen not displayed")

    @task
    def personal_details_3(self):
        with self.client.post("/InsuranceWebExtJS/quote_auto3.jsf", name="getinstantquote_3",
                              cookies={"JSESSIONID": self.jsession_id,
                                       "UserSessionFilter.sessionId": self.user_session_filter},
                              data={"autoquote": "autoquote",
                                    "autoquote:year": "2008",
                                    "makeCombo": "Chrysler",
                                    "autoquote:make": "Chrysler",
                                    "modelCombo": "Aspen",
                                    "autoquote:model": "Aspen",
                                    "autoquote:finInfo": "Own",
                                    "autoquote:next.x": "26",
                                    "autoquote:next.y": "9",
                                    "javax.faces.ViewState": self.view_state}, catch_response=True) as resp:
            if "Your Instant Quote is" in resp.text:
                resp.success()
                print("Quote generated successfully")
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
            else:
                resp.failure("Quote generation failed")


class MyUser(HttpUser):
    wait_time = between(2, 4)
    tasks = [UserBehavior]
