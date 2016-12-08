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
        for entity in list(query.fetch(limit=20)):
            results.append(dict(entity))
        return results

    def get_capital_via_query(self, queryString):
        myquery = queryString.split(':')
        query = self.ds.query(kind=self.kind)
        query.add_filter(myquery[0], '=', myquery[1])
        return self.get_query_results(query)

    def get_capital_via_search(self, searchString):
        query = self.ds.query(kind=self.kind)
        query.add_filter('country', '=', searchString)
        query2 = self.ds.query(kind=self.kind)
        query2.add_filter('id', '=', searchString)
        query3 = self.ds.query(kind=self.kind)
        query3.add_filter('name', '=', searchString)
        query4 = self.ds.query(kind=self.kind)
        query4.add_filter('countryCode', '=', searchString)
        query5 = self.ds.query(kind=self.kind)
        query5.add_filter('continent', '=', searchString)
        response = list()
        response.extend(self.get_query_results(query))
        response.extend(self.get_query_results(query2))
        response.extend(self.get_query_results(query3))
        response.extend(self.get_query_results(query4))
        response.extend(self.get_query_results(query5))
        return response

    def delete_capital(self, capId):
        key = self.ds.key(self.kind, capId)
        self.ds.delete(key)

    def get_capital(self, capital_id):
        """Get capital capital_id from datastore"""
        query = self.ds.query(kind=self.kind)
        query.add_filter('name', '=', capital_id)
        return self.get_query_results(query)

    def publish_message(self, topic_name, data):
        """Publishes a message to a Pub/Sub topic with the given data."""

        splitTopic = topic_name.split('/')
        projectName = splitTopic[1]
        topicName = splitTopic[3]

        pubsub_client = pubsub.Client(project=projectName)

        topic = pubsub_client.topic(topicName)

        # Data must be a bytestring
        encData = base64.b64encode(data)

        message_id = topic.publish(encData)

        return message_id
