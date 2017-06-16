from urllib.request import urlopen,Request
from urllib.parse import urlencode
import json
import sys

endpoint = "http://data.linkedmdb.org/sparql?"

actorname = input("Type the actor first name for your query:")

sparqlq = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
SELECT ?actor_id ?actor_name WHERE {
?actor movie:actor_actorid ?actor_id .
?actor movie:actor_name ?actor_name .
filter(regex(?actor_name, '"""+actorname+""" ',"i"))
}
"""

# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()

# convert to json object
jso = json.loads(text)

actors = []

# iterate over results
for binding in jso['results']['bindings']:
    # for every column in binding
    for bname,bcontent in binding.items():
        aname = ""
        if bname == "actor_id":
            aid = bcontent['value']
        elif bname == "actor_name":
            aname = bcontent['value']
            actors.append([aid, aname])

if not actors:
    print("No actors found!")
    sys.exit(0)
	
for actor in actors:
    print("%s -> %s" % (actor[0], actor[1]))

aid = int(input("Type the actor id for your selection: "))

sparqlq = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
SELECT ?actname ?mtitle WHERE {
?film movie:actor ?mactor.
?film rdfs:label ?mtitle.
?film movie:actor <http://data.linkedmdb.org/resource/actor/"""+str(aid)+"""> .
?mactor movie:actor_name ?actname.
?mactor movie:actor_actorid ?aid.
FILTER(?aid!="""+str(aid)+""")
}
"""


# params sent to server
params = { 'query': sparqlq }
# create appropriate param string
paramstr = urlencode(params)

# create GET http request object with params appended
req = Request(endpoint+paramstr)
# request specific content type
req.add_header('Accept','application/sparql-results+json')
# dispatch request
page = urlopen(req)
# get results and close
text = page.read().decode('utf-8')
page.close()

# convert to json object
jso = json.loads(text)

coactors = []
# iterate over results
for binding in jso['results']['bindings']:
    # for every column in binding
    for bname,bcontent in binding.items():
        if bname == "actname":
            actname = bcontent['value']
        elif bname == "mtitle":
            mtitle = bcontent['value']
            coactors.append([actname, mtitle])

if not coactors:
    print("There were no co-actors found!")
    sys.exit(0)

print("The co-actors are: ")
for actor in coactors:
    print("   %s in %s" % (actor[0], actor[1]))
