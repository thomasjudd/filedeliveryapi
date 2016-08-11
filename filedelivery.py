#!flask/bin/python

from flask import Flask, request, jsonify
import math

app = Flask(__name__)

graph = {}

@app.route('/')
def index():
  return 'File Delivery REST API'

@app.route('/host', methods=['POST', 'GET'])
def host():
  data = request.get_json()
  if request.method=='POST':
     graph[data['name']] = {
       'name': data['name'],
       'cost': 999999, #sufficiently large inital value gets overwritten in dijkstra
       'visited': False,
       'neighbor_keys': []
     }
  return jsonify(graph)

@app.route('/hosts', methods=['GET'])
def hosts():
  return jsonify(graph.nodes())

@app.route('/link', methods=['POST'])
def link():
  data = request.get_json()

  graph[data['source_host']]['neighbor_keys'].append(graph[data['dest_host']]['name'])
  graph[data['dest_host']]['neighbor_keys'].append(graph[data['source_host']]['name'])

  return jsonify(graph)

@app.route('/links', methods=['GET'])
def links():
  return jsonify(graph)

@app.route('/path/<host_a>/to/<host_b>', methods=['GET'])
def find_cheapest_path(host_a, host_b):
  start_node['cost'] = 0
  EDGE_COST = 1

  curr_node = start_node
  
  while len(visted) < len(nodes):
    curr_node['visited'] = True
    visited.append(curr_node)
    for node in curr_node['neighbors']:
      min_node = None
      if node['cost'] > curr_node['cost'] + EDGE_COST and not node['visited']:
        node['cost'] = curr_node['cost'] + EDGE_COST
        if min_node['cost'] > node['cost']:
          min_node = node 
    curr_node = min_node

  return jsonify(visited)




if __name__ == '__main__':
  app.run(debug=True)
