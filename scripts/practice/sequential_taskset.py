from locust import HttpUser, SequentialTaskSet, task, constant_pacing


class UserBehavior(SequentialTaskSet):
    def on_start(self):
        print("starting user behavior")

    @task
    def task_1(self):
        print("I am task 1")

    @task
    def task_2(self):
        print("I am task 2")


class MyTask(HttpUser):
    wait_time = constant_pacing(3)
    host = "http://api.openbrewerydb.org"
    tasks = [UserBehavior]
