import utility
import json
import io
from flask import Flask
from flask import jsonify

from google.cloud import storage, exceptions
# from google.cloud.storage import Blob

class StorageHandler:
    """Represent a google cloud storage handler"""
    def __init__(self):
        #self.gcs = cloudstorage.Storage()
        self.gcs = storage.Client(project=utility.project_id())

    def check_bucket(self, bucket_name):
        try:
            self.gcs.get_bucket(bucket_name)
            return True
        except exceptions.NotFound:
            print 'Error: Bucket {} does not exists.'.format(bucket_name)
            return False
        except exceptions.BadRequest:
            print 'Error: Invalid bucket name {}'.format(bucket_name)
            return None
        except exceptions.Forbidden:
            print 'Error: Forbidden, Access denied for bucket {}'.format(bucket_name)
            return None

    # Adds a capital to the bucket
    def add_to_bucket(self, bucket_name, capital_id, item):
        #itemid = str(item['id'])

        #if bucket does not exist create it
        bucket_exists = self.check_bucket(bucket_name)

        if bucket_exists is not None and not bucket_exists:
            self.create_bucket(bucket_name)

        self.store_file_to_gcs(bucket_name, str(capital_id) + ".json", item)
        return True

    def create_bucket(self, bucket_name):
        try:
            print 'creating bucket {}'.format(bucket_name)
            self.gcs.create_bucket(bucket_name)
            return True
        except Exception as e:
            print "Error: Create bucket Exception"
            print e
            return False

    def store_file_to_gcs(self, bucket_name, filename, item):

        if self.check_bucket(bucket_name):
            bucket = self.gcs.get_bucket(bucket_name)
            blob = bucket.blob(filename)
            utility.log_info('jsonifying data')
            data = json.dumps(item)
            utility.log_info('uploading data')
            blob.upload_from_string(data)

            # try:
            #     self.gcs.open(filepath, 'r')
            #     return True
            # except IOError:
            #     print 'Error: Cannot open the file {}'.format(filepath)
        return True

    def list_objects(self, bucket_name):

        if self.check_bucket(bucket_name):
            bucket = self.gcs.get_bucket(bucket_name)
            print "Object in bucket " + bucket_name
            for blob in list(bucket.list_blobs()):
                print blob.name
