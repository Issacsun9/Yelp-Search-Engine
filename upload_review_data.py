from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from tqdm import tqdm
import time
import gc
from retrying import retry

import re

# clean urls
def clean_url(text):
    text = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text)
    text = re.sub('www.[^s]+','', text)
    text = re.sub('\n', '', text)
    return text

host = 'search-cse6242-proj-5o2zltjhpvd3v6ecpwhepau5my.us-east-1.es.amazonaws.com' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


@retry(stop_max_attempt_number=10)
def upload_data(short_select_reviews):
        time.sleep(120)
        search = OpenSearch(
                hosts=[{'host': host, 'port': 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
        )
        print("******************restart******************")

        current_count = search.count(index="yelp_search")['count']
        print("current count: ", current_count)

        for index, i in tqdm(enumerate(short_select_reviews[current_count:])):

                search.index(index="yelp_search", doc_type="_doc", id=str(index + current_count + 1), body=i)
                if index % 5000 == 0:
                        time.sleep(5)
