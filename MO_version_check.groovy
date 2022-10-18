import com.bosch.blueworx.lws.api.interfaces.*
import java.util.regex.Pattern

def catalog = lwsapi.getLwsCatalog(workUnitPath)
def manager = catalog.getManager()
def criteria = new SearchCriteria()
def rootParent = new SearchCriteria()
criteria.addClass("BC_MO")
criteria.setName(Pattern.compile("Mo"))

println "--------------------------"
def result = catalog.findByCriteria(catalog.getRootArtifact(), criteria)
def result_parent = catalog.findByCriteria(catalog.getRootArtifact(), rootParent)
println "folder: " + result[0].getParent()
def newCatalog =  result[0].getCatalog()

def afterde = catalog.findByCriteria(catalog.getRootArtifact(), criteria)

println "Mo_version:"  + afterde[0].getVariantName()
println "Mo_Revision:"  + afterde[0].getRevision()



