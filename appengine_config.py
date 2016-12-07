import os
from google.appengine.ext import vendor

# Add the correct packages path if running on Production
# (this is set by Google when running on GAE in the cloud)
if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # on mac
    #vendor.add('venv/lib/python2.7/site-packages')

    # on windows
    vendor.add('venv/Lib/site-packages')
