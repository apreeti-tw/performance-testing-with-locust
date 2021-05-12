from locust import task, SequentialTaskSet, constant, HttpUser
import re
import logging

logger = logging.getLogger(__name__)

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
                logger.info("User logged in")
            else:
                resp1.failure("CRITICAL")
                logger.critical("Error logging in")

    @task
    def select_agent_lookup(self):
        with self.client.get("/InsuranceWebExtJS/agent_lookup.jsf",
                             name="agent lookup",
                             cookies={"JSESSIONID": self.jsession_id,
                                      "UserSessionFilter.sessionId": self.user_filter_session},
                             catch_response=True) as resp:
            if "Get in touch" in resp.text:
                resp.success()
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                logger.info("Successful agent lookup")
            else:
                resp.failure("ERROR")
                logger.error("Agent lookup failed")

    @task
    def show_all_agents(self):
        with self.client.post("/InsuranceWebExtJS/agent_lookup.jsf",
                              name="show all agents",
                              cookies={"JSESSION": self.jsession_id,
                                       "UserSessionFilter.sessionId": self.user_filter_session},
                              data={"show-all": "show-all", "show-all:search-all.x": "42",
                                    "show-all:search-all.y": "12", "javax.faces.ViewState": self.view_state},
                              catch_response=True) as resp:
            if "Here is the list of all available Agents" in resp.text:
                resp.success()
                self.view_state = re.findall("j_id\d+:j_id\d+", resp.text)[0]
                logger.info("All agents showed up")
            else:
                resp.failure("ERROR")
                logger.error("Agents not found")


class MyUser(HttpUser):
    wait_time = constant(3)
    host = "http://demo.borland.com"
    tasks = [UserBehavior]
