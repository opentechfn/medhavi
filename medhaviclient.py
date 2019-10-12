import json
import requests

# Post json data
url = "http://127.0.0.1:8000/data"
json = json.loads(open("data.json").read())
data = requests.post(url=url, json=json)
if data:
    print("********************Post data sucessfull*************************")
    print data

# Get all resources
url = "http://127.0.0.1:8000/resource"
data = requests.get(url)
if data:
    print("********************All Resources*************************")
    print data.content

# Get all nodes
url = "http://127.0.0.1:8000/node"
data = requests.get(url)
if data:
    print("*******************All Nodes******************************")
    print data.content

# Get ML Data
url = "http://127.0.0.1:8000/mldata"
data = requests.get(url)
if data:
    print("*******************ML DATA********************************")
    print data.content

# Get Node Resources
url = "http://127.0.0.1:8000/node/resources"
data = requests.get(url)
if data:
    print("*******************Node Resources*************************")
    print data.content
