import json
import os
from stream.sub.data import SubscriptionData


class SubscriptionProvider:
    def __init__(self, subs):
        self.subs = subs

    # get instance of subscription class and save it to json
    def save(self):
        data = self._to_json()
        with open('subs.json', 'w') as f:
            f.write(json.dumps(data))

    def load(self):
        if os.path.isfile('subs.json'):
            with open('subs.json') as f:
                data = json.load(f)
            self._from_json(data)

    def add(self, sub):
        pass

    def delete(self):
        pass

    def _to_json(self):
        res = []
        for sub in self.subs.data:
            res.append(sub.__dict__)
        return res

    def _from_json(self, json_data):
        self.subs.data.clear()
        for item in json_data:
            sub = SubscriptionData(item['name'], item['guild'], item['channel'], item['everyone'])
            self.subs.data.append(sub)
