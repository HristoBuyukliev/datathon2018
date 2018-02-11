from flask import Flask
from flask import request
from data import read_data, read_g5
from flask_cors import CORS

import json

graphData = read_data()
g5 = read_g5()
g5_ids = set(g5['HASH_ID'])
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    node_id = request.args.get("node_id")
    if node_id not in graphData.index:
        return json.dumps([])
    links = graphData.loc[node_id]
    nodes = [
        {"id": node_id,
         "group": 1,
         'g5': node_id in g5_ids
         }
    ]
    result_links = []
    for k, link in links.iterrows():
        nodes.append({
            "id": k,
            "group": 1
        })
        result_links.append({
            'source': node_id,
            'target': k,
            'right': True,
            "value": 1
        })
    return json.dumps({'nodes': nodes, 'links': result_links})


app.run()
