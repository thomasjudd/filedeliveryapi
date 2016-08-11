RESTful API to track remote computers and the links between them. When queried it should return the cheapest path to deliver a file from a host to any other host

POST method to /host creates a new host
GET  /hosts gets a listing of all hosts in any format
POST /link create a link between two hosts with a description of that link
GET /links to get a listing of all links (edges)
GET /path/:A/to/:B to retrieve the easiest way to transfer a file between host A and host B
