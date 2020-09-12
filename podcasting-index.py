import argparse
from datetime import date
import hashlib
import json
import requests
import time

# create and parse our args
parser = argparse.ArgumentParser()
parser.add_argument(dest='search_query', type=str, help="Query to search podcastindex.org for")
args = parser.parse_args()

# setup some basic vars for the search api. 
# for more information, see https://api.podcastindex.org/developer_docs
api_key = 'YOUR API KEY HERE'
api_secret = 'YOUR API SECRET HERE'
query = args.search_query
url = "https://api.podcastindex.org/api/1.0/search/byterm?q=" + query

# uncomment these to make debugging easier.
# print ('api key: ' + api_key);
# print ('api secret: ' + api_secret);
# print ('query: ' + query);
# print ('url: ' + url);

# the api follows the Amazon style authentication
# see https://docs.aws.amazon.com/AmazonS3/latest/dev/S3_Authentication2.html

# we'll need the unix time
epoch_time = int(time.time())

# our hash here is the api key + secret + time 
data_to_hash = api_key + api_secret + str(epoch_time)
# which is then sha-1'd
sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

# now we build our request headers
headers = {
    'X-Auth-Date': str(epoch_time),
    'X-Auth-Key': api_key,
    'Authorization': sha_1,
    'User-Agent': 'postcasting-index-python-cli'
}

# perform the actual post request
r = requests.post(url, headers=headers)

# if it's successful, dump the contents (in a prettified json-format)
# else, dump the error code we received
if r.status_code == 200:
    print ('<< Received >>')
    pretty_json = json.loads(r.text)
    print (json.dumps(pretty_json, indent=2))
else:
    print ('<< Received ' + str(r.status_code) + '>>')

