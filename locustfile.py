import uuid

from locust import HttpLocust, TaskSet

def sub(l):
    with l.client.get("/sub/" + l.user_id, catch_response=True) as response:
        if response.status_code == 200:
            response.success()
        else:
            response.failure("%d, %s" % (response.status_code, response.content))

def pub(l):
    with l.client.post("/pub/" + l.user_id, catch_response=True, data="TEST") as response:
        if response.status_code in [201,202]:
            response.success()
        else:
            response.failure("%d, %s" % (response.status_code, response.content))



class UserBehavior(TaskSet):
    tasks = {sub: 3, pub: 1}


    def on_start(self):
        self.user_id = str(uuid.uuid4())

class LongPollUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 100
    max_wait = 300
