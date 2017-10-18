import gate, sys, json, codecs, os, itertools


"""iterate file names in 'documents_json' folder""" 
for fileName in sorted(os.listdir("documents_json")):

  print("loading file:", fileName)
  sys.stdout.flush()
  
  with open("documents_json/"+fileName, 'r', encoding="utf8") as jsonFile:
  
    """read utf8 json file""" 
    line = jsonFile.read().strip()
    #line = codecs.decode(line, "utf8")
    input_json = json.loads(line)
    
    print("json loaded")
    sys.stdout.flush()

    """convert json do gate.Document""" 
    document = gate.Document.load(input_json)
    
    """get all tokens""" 
    tokens = document.annotationSets['treex'].type('Token')
    
    """sort tokens by start offset""" 
    tokensSorted = sorted(tokens, key=lambda token: token.start)
    
    #print(document.text)
    
    print("number of tokens: ", len(tokens))
    
    """print first 10 tokens"""
    for token in itertools.islice(tokensSorted, 10):
      
      """get corresponding string from the document"""
      origStr =  document.text[token.start : token.end]
      
      
      """print token id, string, lemma, tag"""
      outStr = "%s %s %s %s\n" % (token.id, origStr, token.features['lemma'], token.features['tag'])
      sys.stdout.flush()
      sys.stdout.buffer.write(outStr.encode('utf8')) 


  sys.stdout.flush()
