import gate, re

@gate.executable
def tokenize(document, outputAS):
    
    p = re.compile('\w+')

    for token in re.finditer(p, document.text):
        outputAS.add(
            token.start(), 
            token.end(), 
            "Token.py2", 
            {"string":token.group(), "rule":"py"})

    return document

if __name__ == "__main__":
    tokenize.start()