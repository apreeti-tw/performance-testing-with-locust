from locust import HttpUser, TaskSet, task, between, SequentialTaskSet
import re


class UserBehavior(TaskSet):
    def __init__(self, parent):
        super().__init__(parent)
        self.jsession_id = ""
        self.user_session_filter = ""
        self.view_state = ""

    def on_start(self):
        resp = self.client.get("/InsuranceWebExtJS", name="launch")
        self.jsession_id = resp.cookies["JSESSIONID"]
        self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]

        with self.client.post("/InsuranceWebExtJS/index.jsf", name="login",
                              data={"login-form": "login-form", "login-form:email": "test@valid.com"
                                  , "login-form:password": "test", "login-form:login.x": "57"
                                  , "login-form:login.y": "10", "javax.faces.ViewState": self.view_state},
                              cookies={"JSESSIONID": self.jsession_id}, catch_response=True) as resp2:
            if "Logged in" in resp2.text:
                resp2.success()
                print("User logged in")
                self.user_session_filter = resp2.cookies["UserSessionFilter.sessionId"]
            else:
                resp2.failure("Error logging in")

    @task(2)
    class Agent_Lookup(SequentialTaskSet):
        @task(4)
        def select_agent_lookup(self):
            with self.client.get("/InsuranceWebExtJS/agent_lookup.jsf",
                                 name="agent lookup",
                                 cookies={"JSESSIONID": self.parent.jsession_id,
                                          "UserSessionFilter.sessionId": self.parent.user_filter_session},
                                 catch_response=True) as resp:
                if "Get in touch" in resp.text:
                    resp.success()
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                    print("Successful agent lookup")
                else:
                    resp.failure("Agent lookup failed")

        @task(2)
        def show_all_agents(self):
            with self.client.post("/InsuranceWebExtJS/agent_lookup.jsf",
                                  name="show all agents",
                                  cookies={"JSESSION": self.parent.jsession_id,
                                           "UserSessionFilter.sessionId": self.parent.user_filter_session},
                                  data={"show-all": "show-all", "show-all:search-all.x": "42",
                                        "show-all:search-all.y": "12", "javax.faces.ViewState": self.parent.view_state},
                                  catch_response=True) as resp:
                if "Here is the list of all available Agents" in resp.text:
                    resp.success()
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                    print("All agents showed up")
                else:
                    resp.failure("Agents not found")

        @task(1)
        def self_interrupt(self):
            print("Stopping agent lookup")
            self.interrupt()

    @task(4)
    class Autoquote(SequentialTaskSet):
        @task(4)
        def select_autoquote(self):
            with self.client.get("/InsuranceWebExtJS/quote_auto.jsf", name="select autoquote",
                                 cookies={"JSESSIONID": self.parent.jsession_id,
                                          "UserSessionFilter.sessionId": self.parent.user_session_filter},
                                 catch_response=True) as resp:
                if "Get Instant Auto Quote" in resp.text:
                    resp.success()
                    print("Autoquote selected")
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                else:
                    resp.failure("Autoquote selection failed")

        @task(2)
        def personal_details_1(self):
            with self.client.post("/InsuranceWebExtJS/quote_auto.jsf", name="getinstantquote_1",
                                  data={"autoquote": "autoquote",
                                        "autoquote:zipcode": "00000000",
                                        "autoquote:e-mail": "qamile2@gmail.com",
                                        "autoquote:vehicle": "car",
                                        "autoquote:next.x": "38",
                                        "autoquote:next.y": "10",
                                        "javax.faces.ViewState": self.parent.view_state},
                                  cookies={'JSESSIONID': self.parent.jsession_id,
                                           'UserSessionFilter.sessionId':
                                               self.parent.user_session_filter},
                                  catch_response=True) as resp:
                if "You're almost done!" in resp.text:
                    resp.success()
                    print("Instant Auto Quote - Continued")
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                else:
                    resp.failure("Instant Auto Quote")

        @task(2)
        def personal_details_2(self):
            with self.client.post("/InsuranceWebExtJS/quote_auto2.jsf", name="getinstantquote_2",
                                  cookies={"JSESSIONID": self.parent.jsession_id,
                                           "UserSessionFilter.sessionId": self.parent.user_session_filter},
                                  data={"autoquote": "autoquote",
                                        "autoquote:age": "0",
                                        "autoquote:gender": "Male",
                                        "autoquote:type": "Excellent",
                                        "autoquote:next.x": "35",
                                        "autoquote:next.y": "7",
                                        "javax.faces.ViewState": self.parent.view_state}, catch_response=True) as resp:
                if "Last Screen!" in resp.text:
                    resp.success()
                    print("Last Screen!")
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                else:
                    resp.failure("Last Screen not displayed")

        @task(2)
        def personal_details_3(self):
            with self.client.post("/InsuranceWebExtJS/quote_auto3.jsf", name="getinstantquote_3",
                                  cookies={"JSESSIONID": self.parent.jsession_id,
                                           "UserSessionFilter.sessionId": self.parent.user_session_filter},
                                  data={"autoquote": "autoquote",
                                        "autoquote:year": "2008",
                                        "makeCombo": "Chrysler",
                                        "autoquote:make": "Chrysler",
                                        "modelCombo": "Aspen",
                                        "autoquote:model": "Aspen",
                                        "autoquote:finInfo": "Own",
                                        "autoquote:next.x": "26",
                                        "autoquote:next.y": "9",
                                        "javax.faces.ViewState": self.parent.view_state}, catch_response=True) as resp:
                if "Your Instant Quote is" in resp.text:
                    resp.success()
                    print("Quote generated successfully")
                    self.parent.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                else:
                    resp.failure("Quote generation failed")

        @task(1)
        def self_interrupt(self):
            print("Stopping autoquote")
            self.interrupt()


class MyTask(HttpUser):
    wait_time = between(3, 5)
    host = "http://demo.borland.com"
    tasks = [UserBehavior]
