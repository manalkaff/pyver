import json, threading
from functools import partial
from socketserver import ThreadingMixIn
from http.server import HTTPServer
from .handler import Serv
from PySide2.QtCore import QThread

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

	def log_message(self, format, *args):
		pass
 
 
class QThreadedHTTPServer(QThread, ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""
	def __init__(self, server_address, RequestHandlerClass):
		HTTPServer.__init__(self, server_address, RequestHandlerClass)
		QThread.__init__(self)

	def run(self):
		self.serve_forever()

	def stop(self):
		self.shutdown()
		self.quit()


	def log_message(self, format, *args):
		pass

class ThreadedServer:
    
	def __init__(self, urls,  host, port):

		self.host = host
		self.port = port

		self.handler = partial(Serv, urls)
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



class QThreadedServer(QThread):
	def __init__(self, urls, host, port):
		QThread.__init__(self)
        
		self.host = host
		self.port = port

		self.handler = partial(Serv, urls)
		self.httpd = QThreadedHTTPServer((self.host, self.port), self.handler)
		self.serveractive = False

	def run(self):
		if not self.httpd.isRunning():
			self.httpd.start()
			self.serveractive = True
			return True
		else:
			return False

	def stop(self):
		if self.serveractive:
			self.httpd.stop()
			self.serveractive = False
			self.quit()