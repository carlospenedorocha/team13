from datetime import datetime
from google.cloud import datastore, pubsub
import utility
import base64

class Capitals(object):
    """Represent a Capital in the database"""
    def __init__(self):
        self.ds = datastore.Client(project=utility.project_id())
        self.kind = "capitals"

    def store_capital(self, data):
        key = self.ds.key(self.kind, str(data['id']))
        entity = datastore.Entity(key=key)

        entity['id'] = data['id']
        entity['country'] = data['country']
        entity['name'] = data['name']
        entity['location'] = datastore.Entity(key=self.ds.key('location'))
        entity['location']['latitude'] = data['location']['latitude']
        entity['location']['longitude'] = data['location']['longitude']
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

    def delete_capital(self, capId):
        key = self.ds.key(self.kind, capId)
        self.ds.delete(key)

    def get_capital(self, capital_id): 
        query = self.ds.query(kind=self.kind)
        query.add_filter('id', '=', capital_id)
        return self.get_query_results(query)

    def publish_message(self, topic_name, data):
        """Publishes a message to a Pub/Sub topic with the given data."""
        pubsub_client = pubsub.Client()
        topic = pubsub_client.topic(topic_name)

        # Data must be a bytestring
        encData = base64.b64encode(data)

        message_id = topic.publish(encData)

        print('Message {} published.'.format(message_id))

        return message_id

# def parse_note_time(note):
#     """converts a greeting to an object"""
#     return {
#         'text': note['text'],
#         'timestamp': note['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
#     }
