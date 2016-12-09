from datetime import datetime
from google.cloud import datastore
import utility
import Capitals

class CapitalGui:

    def __init__(self):
        self.ds = datastore.Client(utility.project_id())
        self.kind = "capitals"

    def store_greeting(self, comment):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)

        entity['comment'] = comment
        entity['timestamp'] = datetime.utcnow()

        return self.ds.put(entity)

    def fetch_capitals(self):
        capital = Capitals.Capitals()
        return capital.fetch_unique_capitals()

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results

