#!flask/bin/python

from flask import Flask, request, jsonify
import networkx as nx

app = Flask(__name__)

myhosts = []
graph = nx.Graph()

mylinks = {}

@app.route('/')
def index():
  return 'File Delivery REST API'

@app.route('/host', methods=['POST', 'GET'])
def host():
  data = request.get_json()
  if request.method=='POST':
    graph.add_node(data['name'] , data)
    return jsonify(graph.nodes())
  else:
    return jsonify({})

@app.route('/hosts', methods=['GET'])
def hosts():
  return jsonify(graph.nodes())

@app.route('/link', methods=['POST'])
def link():
  data = request.get_json()
  if len(myhosts) < 0:
    return None

  graph.add_edge(data['source_host'], data['dest_host'])

  return jsonify(graph.edges())

@app.route('/links', methods=['GET'])
def links():
  return jsonify(graph.edges())

@app.route('/path/<host_a>/to/<host_b>', methods=['GET'])
def find_cheapest_path(host_a, host_b):
  return jsonify(nx.shortest_path(graph, host_a, host_b))

if __name__ == '__main__':
  app.run(debug=True)
