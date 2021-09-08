from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib import parse
import json, threading
from functools import partial
from .constants.methods import POST, GET



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""


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
			response = func(params, data)
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


class ThreadedServer:
    
	def __init__(self, host, port):

		self.host = host
		self.port = port

		self.handler = partial(Serv, self.terminal)
		self.httpd = ThreadedHTTPServer((self.host, self.port), self.handler)
		self.serveractive = False
		self.server_thread = threading.Thread(target=self.httpd.serve_forever)



	def startserver(self):
		
		if not self.server_thread.is_alive():
			self.serveractive = True
			self.server_thread.start()
			return True
		else:
			return False

	def stopserver(self):

		if self.serveractive:
			self.httpd.shutdown()
			self.httpd.server_close()
			self.server_thread._stop()
			self.serveractive = False
			return True
		else:
			return False
