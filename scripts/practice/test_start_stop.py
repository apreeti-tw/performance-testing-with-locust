from locust import HttpUser, task, constant, events


@events.test_start.add_listener
def script_start(**kwargs):
    print("Starting test")


@events.test_stop.add_listener
def script_stop(**kwargs):
    print("Stopping test")


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
