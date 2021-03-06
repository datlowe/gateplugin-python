"""Utilities to work with a GATE instance from within Python"""
import os, json, sys, urllib.request, urllib.parse, urllib.error
from .document import Document
from contextlib import contextmanager
from subprocess import Popen, PIPE

class Gate(object):
	def __init__(self, jarLocation = None):
		self.jarLocation = jarLocation
		if self.jarLocation == None:
			self.jarLocation = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			self.jarLocation = os.path.join(self.jarLocation, "gateplugin-python.jar")
			
	def start(self):
		self.gateProcess = Popen(["java", "-cp",
			os.environ['CLASSPATH']+":"+self.jarLocation, 
			"gate.python.PythonGATEInstance"], stdout=PIPE, stdin=PIPE)

	def stop(self):
		self.gateProcess.terminate()

	def __enter__(self):
		self.start()
		return self

	def __exit__(self, type, value, traceback):
		self.stop()

	def readResponse(self):
		response = self.gateProcess.stdout.readline().strip()

		while not response:
			response = self.gateProcess.stdout.readline().strip()

		try:
			return json.loads(response)
		except ValueError:
			print(response, file=sys.stderr)
			raise Exception(response)

	def load(self, document):
		return self.loadURL("file:///"+urllib.parse.quote(os.path.abspath(document)))

	def loadURL(self, document):
		command = {
			"command": "LOAD_DOCUMENT", 
			"targetURL": document
		}
		print(json.dumps(command), file=self.gateProcess.stdin)

		return Document.load(self.readResponse(), src=document)


	def save(self, document, output):
		return self.saveURL(document, "file:///"+urllib.parse.quote(os.path.abspath(output)))

	def saveURL(self, document, output):
		command = {
			"command": "SAVE_DOCUMENT", 
			"targetURL": document.src,
			"outputURL": output, 
			"documentCommands": document.logger
		}

		print(json.dumps(command), file=self.gateProcess.stdin)

		return Document.load(self.readResponse(), src=output)
