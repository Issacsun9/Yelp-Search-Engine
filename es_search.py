from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
import re
import json
import sqlite3
from collections import defaultdict
from datetime import datetime
from ner_menu import *

host = 'search-cse6242-proj-5o2zltjhpvd3v6ecpwhepau5my.us-east-1.es.amazonaws.com'
region = 'us-east-1'  # e.g. us-west-1

service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

search = OpenSearch(
    hosts=[{'host': host, 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)


def elasticSearch(keyword, city):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "review": keyword
                        }
                    },
                    {
                        "match": {
                            "city": city
                        }
                    }
                ]
            }
        }
    }

    res = search.search(body=query, index="yelp_search")

    return res


def elasticGetByIndex(_id):
    res = search.get(id=_id, index="yelp_search")

    return res


def getBusiness(keyword, city):
    conn = sqlite3.connect('business.db')
    c = conn.cursor()

    es_search_res = elasticSearch(keyword, city)["hits"]["hits"]
    related_business_list = defaultdict(dict)

    return_schema = ("business_id", "business_name", "address", "city", "longitude", "latitude", "stars", "is_open",
                     "AppointmentOnly", "Hours")

    for i in es_search_res:
        c.execute("SELECT * FROM business_info WHERE business_id= '%s'" % i["_source"]["business_id"])
        related_business_info = c.fetchall()[0]

        if related_business_info[0] in related_business_list.keys():
            related_business_list[related_business_info[0]]["review"].append(
                (i["_source"]["review"], i["_score"]))
        else:
            temp_dict = {i: j for i, j in zip(return_schema[1:], related_business_info[1:])}
            related_business_list[related_business_info[0]] = temp_dict
            related_business_list[related_business_info[0]]["review"] = [
                (i["_source"]["review"], i["_score"])]
    return related_business_list


def filterResults(related_business_list, dining_time):
    weekday = datetime.strptime(dining_time, "%Y-%m-%d").weekday()
    open = {}
    closed = {}
    appointment = {}
    for business_id, business in related_business_list.items():
        if business["Hours"].split(" ")[weekday] != "Closed":
            open[business_id] = business
        elif business["AppointmentOnly"] == 1:
            appointment[business_id] = business
        else:
            closed[business_id] = business

    return open, closed, appointment


def rankResults(related_business_list):
    sorted_results = sorted(related_business_list, key=lambda x: x["stars"])
    return sorted_results


def searchResults(keyword, city, nlp_food, dining_time=None):
    related_business_list = getBusiness(keyword, city)

    res = []

    if dining_time:
        open, closed, appointment = filterResults(related_business_list, dining_time)
    else:
        open = related_business_list
        closed, appointment = None, None

    for i, j in sorted(open.items(), key=lambda x: x[1]["stars"], reverse=True):
        attributes = []
        for review in j["review"]:
            menu = [i.text for i in ner(review[0], nlp_food)]
            drop_duplicated = list(
                set([re.sub(u"([^\u0041-\u005a\u0061-\u007a ])", "", word.lower()) for word in menu]))
            drop_nan = [i for i in drop_duplicated if i]
            attributes = sorted(drop_nan, key=lambda x: len(x), reverse=True)[:5]
        menu = []
        res.append({"name": j["business_name"],
                    "star": j["stars"],
                    "attributes": attributes,
                    "service": True,
                    "Menu": menu,
                    "latitude": j["latitude"],
                    "longitude": j["longitude"],
                    "city": j["city"]})

    if appointment:
        for i, j in sorted(appointment.items(), key=lambda x: x[1]["stars"], reverse=True):
            attributes = ["Appointment Only"]
            for review in j["review"]:
                menu = [i.text for i in ner(review[0], nlp_food)]
                drop_duplicated = list(
                    set([re.sub(u"([^\u0041-\u005a\u0061-\u007a ])", "", word.lower()) for word in menu]))
                drop_nan = [i for i in drop_duplicated if i]
                attributes = sorted(drop_nan, key=lambda x: len(x), reverse=True)[:4]

            menu = []
            res.append({"name": j["business_name"],
                        "star": j["stars"],
                        "attributes": attributes,
                        "service": False,
                        "Menu": menu,
                        "latitude": j["latitude"],
                        "longitude": j["longitude"],
                        "city": j["city"]})

    if closed:
        for i, j in sorted(closed.items(), key=lambda x: x[1]["stars"], reverse=True):
            attributes = []
            for review in j["review"]:
                menu = [i.text for i in ner(review[0], nlp_food)]
                drop_duplicated = list(
                    set([re.sub(u"([^\u0041-\u005a\u0061-\u007a ])", "", word.lower()) for word in menu]))
                drop_nan = [i for i in drop_duplicated if i]
                attributes = sorted(drop_nan, key=lambda x: len(x), reverse=True)[:5]

            menu = []
            res.append({"name": j["business_name"],
                        "star": j["stars"],
                        "attributes": attributes,
                        "service": False,
                        "Menu": menu,
                        "latitude": j["latitude"],
                        "longitude": j["longitude"],
                        "city": j["city"]})

    return res


if __name__ == "__main__":
    print(json.dumps(searchResults("sandwich", "Philadelphia")))
