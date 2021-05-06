from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task(2)
    class Cart_Behavior(TaskSet):
        @task(4)
        def add_to_cart(self):
            print("I am add to cart")

        @task(2)
        def delete_cart(self):
            print("I am delete cart")

        @task(1)
        def self_interrupt(self):
            print("Stopping cart")
            self.interrupt()

    @task(4)
    class Product_Behavior(TaskSet):
        @task(2)
        def add_product(self):
            print("I am add product")

        @task(4)
        def view_product(self):
            print("I am delete product")

        @task(1)
        def self_interrupt(self):
            print("Stopping product")
            self.interrupt()


class MyTask(HttpUser):
    wait_time = between(3, 5)
    host = "http://api.openbrewerydb.org"
    tasks = [UserBehavior]
