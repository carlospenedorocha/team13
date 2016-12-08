import utility
# import cloudstorage
from google.cloud import storage, exceptions
from google.cloud.storage import Blob

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

        self.store_file_to_gcs(bucket_name, str(capital_id) + ".json")
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

    def store_file_to_gcs(self, bucket_name, filename):

        if self.check_bucket(bucket_name):
            bucket = self.gcs.get_bucket(bucket_name)
            blob = Blob(filename, bucket)

            try:
                with open(filename, 'rb') as input_file:
                    blob.upload_from_file(input_file)
                return True
            except IOError:
                print 'Error: Cannot find the file {}'.format(filename)
        return False

    def fetch_object_from_gcs(self, bucket_name, fileobject):

        if self.check_bucket(bucket_name):
            bucket = self.gcs.get_bucket(bucket_name)
            blob = Blob(fileobject, bucket)
            outfile = fileobject + ".out"

            try:
                with open(outfile, 'wb') as output_file:
                    blob.download_to_file(output_file)
                return True
            except IOError:
                print ('Error: Cannot find the object {}'.format(fileobject))

        return False

    def list_objects(self, bucket_name):

        if self.check_bucket(bucket_name):
            bucket = self.gcs.get_bucket(bucket_name)
            print "Object in bucket " + bucket_name
            for blob in list(bucket.list_blobs()):
                print blob.name
