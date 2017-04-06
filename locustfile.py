import uuid
import logging
import requests

from requests.exceptions import ConnectionError
from locust import HttpLocust, TaskSet, events


def quitting_handler(**kw):
    try:
        requests.post("http://localhost:5000/shutdown")
    except ConnectionError:
        pass

events.quitting += quitting_handler

def sub(l):
    logging.debug("sub:" + l.user_id)
    with l.client.get("/sub/?id=%s" % l.user_id, catch_response=True, name="/sub") as response:
        if response.status_code == 200:
            response.success()
        elif  response.status_code == 0:
            response.failure("Timeout")
        else:
            response.failure("%d, %s" % (response.status_code, response.content))

        logging.debug( "sub:" + l.user_id + " - " + response.content)

def pub(l):
    logging.debug("pub:" + l.user_id)
    with l.client.post("/pub/?id=%s" % l.user_id, catch_response=True, data="TEST", name="/pub") as response:
        if response.status_code in [201,202]:
            response.success()
        else:
            response.failure("%d, %s" % (response.status_code, response.content))



class SubUserBehavior(TaskSet):
    tasks = {sub: 1}

    def on_start(self):
        self.user_id = str(uuid.uuid4())
        requests.post("http://localhost:5000/?id=%s" % self.user_id)

class PubUserBehavior(TaskSet):
    tasks = {pub: 1}

    def on_start(self):
        res = requests.get("http://localhost:5000/")
        assert res.status_code == 200
        self.user_id = res.text

class PubLongPollUser(HttpLocust):
    task_set = PubUserBehavior
    min_wait = 100
    max_wait = 300

class SubLongPollUser(HttpLocust):
    task_set = SubUserBehavior
    min_wait = 100
    max_wait = 300
