from http.server import BaseHTTPRequestHandler
from .models.request import Request
import json

from urllib import parse

from .constants.methods import POST, GET



class Serv(BaseHTTPRequestHandler):
		
	def __init__(self, urls, *args, **kwargs):

		self.urls = urls
		BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

	
	def process_request(self, method):
		
		self.send_response(200)

		self.send_header('Content-type','text/html')
		self.end_headers()

		params = {}
		data = {}

		try:
			params = dict(parse.parse_qsl(parse.urlsplit(self.path).query))
			data = self.rfile.read(int(self.headers['Content-Length'])).decode()
			data = json.loads(data)
		except:
			pass

		func = self.urls.find(method, self.path)

		if func != None:
			request = Request(params, data)
			response = func(request)
		else:
			response = {
				"status": 0,
				"message": "404 Not Found"
			}

		self.wfile.write(bytes(json.dumps(response), "utf-8"))


	def do_GET(self):

		return self.process_request(GET)

	
	def do_POST(self):
    
		return self.process_request(POST)



	def address_string(self):
		host, port = self.client_address[:2]
		#return socket.getfqdn(host)
		return host