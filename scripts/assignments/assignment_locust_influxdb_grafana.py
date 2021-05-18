from locust import task, HttpUser, constant, SequentialTaskSet, events
from influxdb import InfluxDBClient
import socket
import json
import datetime
import pytz


hostname = socket.gethostname()
client = InfluxDBClient(host='localhost', port='8086')
client.switch_database('LocustInflux')


def on_request_success(request_type, name, response_time, response_length, **kwargs):
    SUCCESS_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s",' \
                       '"status":"%s"' \
                       '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                       '}]'
    json_string = SUCCESS_TEMPLATE % (
        'LaunchURL', hostname, name, request_type, 'SUCCESS', datetime.datetime.now(tz=pytz.UTC), response_time,
        response_length)
    client.write_points(json.loads(json_string))
    print(json_string)


def on_request_failure(request_type, name, response_time, response_length, exception, **kwargs):
    FAIL_TEMPLATE = '[{"measurement": "%s","tags": {"hostname":"%s","requestName": "%s","requestType": "%s",' \
                    '"exception": "%s", ' \
                    '"status":"%s"' \
                    '},"time":"%s","fields": {"responseTime": "%s","responseLength":"%s"}' \
                    '}]'
    json_string = FAIL_TEMPLATE % (
        'LaunchURL', hostname, name, request_type, exception, 'FAIL', datetime.datetime.now(tz=pytz.UTC),
        response_time,
        response_length)
    client.write_points(json.loads(json_string))
    print(json_string)


events.request_success.add_listener(on_request_success)
events.request_failure.add_listener(on_request_failure)


class UserBehavior(SequentialTaskSet):
    @task
    def profile(self):
        self.client.get('/breweries', name="get breweries")


class MyUser(HttpUser):
    wait_time = constant(4)
    host = 'https://api.openbrewerydb.org'
    tasks = [UserBehavior]
