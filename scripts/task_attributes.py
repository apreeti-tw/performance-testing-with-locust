from locust import HttpUser, task, constant_pacing


def task_1(self):
    print("I am task 1")


def task_2(self):
    print("I am task 2")


class MyTask(HttpUser):
    wait_time = constant_pacing(3)
    host = "http://api.openbrewerydb.org"
    tasks = {task_1: 2, task_2: 4}
