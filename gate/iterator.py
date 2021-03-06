"""Create an interface by which you can listen for GATE documents with an iterator when your
program starts, and have the iterator quit when GATE gets the appropriate signal to say the pipeline has
ended."""

from .document import Document
from .corpus import Corpus
from .gate_exceptions import InvalidOffsetException
import sys, json, codecs

class GateIterator(object):
    def __init__(self):
        self.scriptParams = {}

    def __iter__(self):
        line = sys.stdin.readline().strip()
        while line:
            line = codecs.decode(line, "utf8")

            if line:
                input_line = line
                input_json = json.loads(line)

                if "command" in input_json:
                    if input_json["command"] == "BEGIN_EXECUTION":
                        corpus = Corpus(input_json)
                    elif input_json["command"] == "ABORT_EXECUTION":
                        return
                    elif input_json["command"] == "END_EXECUTION":
                        return
                else:
                    try:
                        document = Document.load(input_json)
                        scriptParams = input_json.get("scriptParams")
                        scriptParams = self.scriptParams if self.scriptParams else {}

                        scriptParams["inputAS"] = document.annotationSets[input_json["inputAS"]]
                        scriptParams["outputAS"] = document.annotationSets[input_json["outputAS"]]

                        inputAS = self.scriptParams["inputAS"]
                        outputAS = self.scriptParams["outputAS"]

                        yield document, scriptParams
                        print(json.dumps(document.logger))
                    except InvalidOffsetException as e:
                        print("InvalidOffsetException prevented reading a document " + e.message, file=sys.stderr)
                        print(json.dumps([]))
                    sys.stdout.flush()

            line = sys.stdin.readline().strip()

def iterate():
    """I can't inherit any of this from ProcessingResource because
        we need to completely change the flow to support iteration"""
    iterator = GateIterator()
    return iterator