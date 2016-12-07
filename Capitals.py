from datetime import datetime
from google.cloud import datastore
import utility


class Capitals(object):
    """Represent a Capital in the database"""
    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "capitals"

    def store_capital(self, data):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)

        entity['id'] = data['id']
        entity['country'] = data['country']
        entity['name'] = data['name']
        entity['location'] = { 'latitude': data['location']['latitude'],
                                'longitude': data['location']['longitude'],
                            }
        entity['countryCode'] = data['countryCode']
        entity['continent'] = data['continent']
        return self.ds.put(entity)

    def fetch_capitals(self):
        query = self.ds.query(kind=self.kind)
        query.order = ['id']
        return self.get_query_results(query)

    def get_query_results(self, query):
        results = list()
        for entity in list(query.fetch()):
            results.append(dict(entity))
        return results

# def parse_note_time(note):
#     """converts a greeting to an object"""
#     return {
#         'text': note['text'],
#         'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
#     }
