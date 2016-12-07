from datetime import datetime
from google.cloud import datastore
import utility


class Capitals(object):
    """Represent a Capital in the database"""
    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "capitals"

    def store_capital(self, id, country, name, latitude, longitude, countryCode, continent):
        key = self.ds.key(self.kind)
        entity = datastore.Entity(key)

        entity['id'] = id
        entity['country'] = country
        entity['name'] = name
        entity['location'] = { 'latitude': latitude,
                                'longitude': longitude,
                            }
        entity['countryCode'] = countryCode
        entity['continent'] = continent
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
