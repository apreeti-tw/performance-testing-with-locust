from locust import HttpUser, task, constant


class MyTask(HttpUser):
    wait_time = constant(3)
    host = "http://api.openbrewerydb.org"

    def on_start(self):
        print("I am logging in")

    @task
    def index_page(self):
        print("I am doing my work")

    def on_stop(self):
        print("I am logging out")
