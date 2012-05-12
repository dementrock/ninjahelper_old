from ninjahelper import app
from index import *

@app.before_request
def add_uri():
	from flask import request
	uri = request.path
	if request.query_string: uri += "?" + request.query_string
	request.uri = uri
