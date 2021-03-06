
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import certifi

application = Flask(__name__)

#Keywords
keyword_dict = {'keyword 1':'movies','keyword 2':'technology','keyword 3':'sports','keyword 4':'life','keyword 5':'news','keyword 6':'travel','keyword 7':'health','keyword 8':'awesome','keyword 9':'energy','keyword 10':'music','Nothing here':'no','':'no'}
geo_dict = {'d1':10,'d2':50,'d3':100,'d4':200,'d5':500,'d6':1000,'d7':5000,'Nothing here':0,'': 0}

#Define ElasticSearch credentials
es = Elasticsearch(hosts = [{"host" : "AWS_Host",
                              "port" : 443}],
                              use_ssl='True')

@application.route ('/',methods = ['POST', 'GET'])
def update_map():
    center_lat = 0.00
    center_long = 0.00
    key = "Nothing here"
    dist = "Nothing here"
    tweets = []
    if request.method == 'POST':
        
        key = request.form['keyword']
        dist = request.form['geo_dist']
        tweets = gettweets(keyword_dict[key])
    
    #Update HTML webpage
    return render_template("index.html",lat = center_lat, long = center_long, key = keyword_dict[key], dist = geo_dict[dist], tweets = tweets)

def gettweets(keyword):
    
    tweets = []
    
    if keyword == "no":
        keyword = ""

    body_content = {"query":{"match":{"_all":keyword}}}

    #Get relevant tweet stream
    stream = es.search(index = "final-tweet-index", doc_type = "twitter", body = body_content, size = 10000)    
    tweets = stream["hits"]["hits"]
    
    return tweets   

if __name__ == "__main__":
    
    application.run(host='0.0.0.0', debug = True)
