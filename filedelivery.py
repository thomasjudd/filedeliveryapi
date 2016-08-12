#!flask/bin/python

from flask import Flask, request, jsonify
import math
import random
import string


app = Flask(__name__)

graph = {}

def generate_nodes():
  num_links = 48
  alphabet = list(string.ascii_lowercase)
  for letter in alphabet:
     graph[letter] = {
       'name': letter,
       'cost': 999999, #sufficiently large inital value gets overwritten in dijkstra
       'visited': False,
       'neighbor_keys': []
     }
  for i in range(num_links):
    start = random.randint(0, len(alphabet)-1)
    end = random.randint(0, len(alphabet)-1)
    if not graph[alphabet[end]]['name'] in graph[alphabet[start]]['neighbor_keys']:
      graph[alphabet[start]]['neighbor_keys'].append(graph[alphabet[end]]['name'])

    if not graph[alphabet[start]]['name'] in graph[alphabet[end]]['neighbor_keys']:
      graph[alphabet[end]]['neighbor_keys'].append(graph[alphabet[start]]['name'])

@app.route('/')
def index():
  generate_nodes()
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
  return jsonify(graph)

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
  start_node = graph[host_a]
  start_node['cost'] = 0
  curr_node = start_node
  end_node = graph[host_b]
  EDGE_COST = 1

  tmp = []
  path = []
  for i in range(len(graph)):
    path.append(curr_node)
    unvisited_neighbors = []
    for node in curr_node['neighbor_keys']:
      if not graph[node]['visited']:
        unvisited_neighbors.append(graph[node])     
        if graph[node]['cost'] > (curr_node['cost'] + EDGE_COST):
          graph[node]['cost'] = curr_node['cost'] + EDGE_COST

    curr_node['visited'] = True
    tmp.append(unvisited_neighbors)
    curr_node = unvisited_neighbors[0].copy()

  return jsonify(path)



if __name__ == '__main__':
  app.run(debug=True)
