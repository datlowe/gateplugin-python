import gate.python.DocumentJsonUtilsForPython
import static groovy.json.JsonOutput.*
import groovy.json.JsonSlurper
import com.fasterxml.jackson.core.JsonFactory;
import com.fasterxml.jackson.core.JsonGenerator;


outputFile = new File(scriptParams.outputFolder + "/" + doc.name + ".json")


JsonFactory factory = new JsonFactory()

outputFile.withOutputStream { out ->

    allAnnotations = [:]

    doc.getAnnotationSetNames().each { annotationSetName ->

        annotationSet = doc.getAnnotations(annotationSetName)

        allAnnotations.putAll(annotationSet.groupBy {
            (annotationSetName ?: '') + ':' + it.type
        })
    }

    JsonGenerator jsonG = factory.createGenerator(out)
    try {
      
      def extraFeatures = [:]
      extraFeatures.put("documentFeatures", doc.getFeatures());
    
      DocumentJsonUtilsForPython.writeDocument(doc, 0, doc.end(), allAnnotations, extraFeatures, 
          null, 'annotationID', jsonG)
    } finally {
        jsonG.close()
    }
}

