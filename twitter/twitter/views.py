from django.shortcuts import render, redirect
import pymongo
import networkx as nx
import matplotlib.pyplot as plt
# from transformers import pipeline


# analyzer = pipeline(
#     task='text-classification',
#     model="cmarkea/distilcamembert-base-sentiment",
#     tokenizer="cmarkea/distilcamembert-base-sentiment"
# )

def create_network(tweets):


    nodes = []
    edges = []

    for tweet in tweets:
        node_tmp = {"id": tweet["author_id"], "mentions": 0, "group" : 1 }
        print(node_tmp)
        check = True
        for node in nodes:
            if node["id"] == node_tmp["id"]:
                check = False
        if check:
            nodes.append(node_tmp)

        if 'entities' in tweet:
            if 'mentions' in tweet['entities']:
                for mention in tweet['entities']['mentions']:
                    edges.append({"source": tweet["author_id"], "target": mention["id"]})
                    check = True
                    node_tmp = {"id": mention["id"], "mentions" :1, "group":0}
                    for node in nodes :
                        if node["id"] == node_tmp["id"]:
                            check = False
                    if check:
                        nodes.append(node_tmp)

    network = nx.Graph()

    print(nodes)
    print(edges)

    for node in nodes:
        network.add_node(node["id"])

    for edge in edges:
        network.add_edge(edge["source"], edge["target"])

    pos = nx.spring_layout(network)

    #nx.draw(network, pos, with_labels=False, alpha=0.4)
    #plt.show()

    network_array ={"nodes" : nodes, "links": edges}
    return network_array

def mongoDB_connect():
    conn_str = "mongodb+srv://ingemedia:YYY5E6Z7lwaMFUoN@cluster0.k5gis.mongodb.net/test"
    client = pymongo.MongoClient(conn_str)

    try:
        print(client.server_info())
    except Exception:
        print("Unable to connect to the server")

    mongodb_ingemedia = client["ingemedia"]

    return mongodb_ingemedia

def creatwordcloud(docs) :
    alltokens = []

    for doc in docs:
        alltokens += doc['token']

    tableau_occurence=[]
    for token in alltokens :
        check = True
        for token2 in tableau_occurence :

            if token == token2['text'] :
             check = False
             token2['frequency'] += 1
        if check :
            tableau_occurence.append({'text' : token , 'frequency' : 1})

    print(tableau_occurence)
    return tableau_occurence

def wordcloud(request):
    db = mongoDB_connect()
    col = db["tweets"]

    query = {
        "source": "GoogleColab_AT_123_RS"
    }

    docs = col.find(query)

    tweets = []
    tableau_occurence = creatwordcloud(docs)

    #create_network(docs)


    for tweet in docs:
        # result = analyzer(
        #     tweet["text"],
        # )
        # tweet["rating"] = result
        tweets.append({"text": tweet["text"], "rating": 0})

    return render(request, "WordCloud.html", {"tableau_occurence": tableau_occurence})


def network(request):
     db = mongoDB_connect()
     col = db["tweets"]

     query = {
        "source": "GoogleColab_AT_123",
        "query" : "@afpfr"
     }

     docs = col.find(query)

     net = create_network(docs)

     return render(request, "network.html", {"network": net})
def tableau(request):
   db = mongoDB_connect()
   col = db["tweets"]

   query = {
       "source": "GoogleColab_AT_123",
       "query": "@afpfr"
   }

   docs = col.find(query)
   print(docs)

   tweets = []
   for doc in docs:
       tweets.append({"text": doc["text"]})



   return render(request, "tableau.html", { "docs": tweets})

