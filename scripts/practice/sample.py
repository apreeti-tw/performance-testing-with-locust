from locust import HttpUser, task, between


class MyWebUser(HttpUser):
    wait_time = between(5, 9)
    host = "http://api.openbrewerydb.org"
    weight = 3

    @task
    def index_page(self):
        print("I am a web user")


class MyMobileUser(HttpUser):
    wait_time = between(5, 9)
    host = "http://api.openbrewerydb.org"
    weight = 1

    @task
    def index_page(self):
        print("I am a mobile user")
