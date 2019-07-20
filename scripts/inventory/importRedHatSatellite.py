# e.g. pullHostnamesIntoInventoryMultiEnvironment('./mySat6Export.csv', 'pyInventoryAllSat6.py', 1, 7, 6, ['myExclude1', 'myExclude2'])        
import csv
from sets import Set

from library.util import writeToFile, appendToFile, stripDashChars

class hostEntry:
    hostname = ""
    environment = ""
    type = ""
    def __init__(self, hostname, environment, serverType):
        self.hostname = hostname
        self.environment = environment
        self.type = serverType 

# e.g. pullSatteliteExportIntoInventoryMultiEnvironment('./mySatExport.csv', 'pyInventory.py', 1, 7, 6, ['myExclude1', 'myExclude2'])    
def pullSatelliteExportIntoInventoryMultiEnvironment(csvInputFile, inventoryPythonOutputFile, columnOfHostnames, columnOfEnvironments, columnOfServerType, excludesList):
    # init file
    writeToFile("\n", inventoryPythonOutputFile)
    
    hostEntries = Set()
    allHosts = Set()
    allEnvironments = Set()
    allServerTypes = Set()
    with open(csvInputFile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        
        appendToFile("allHosts = [\n", inventoryPythonOutputFile)
        rowCount = 0
        
        for row in csvReader:
            if rowCount > 0 :
                print row[columnOfHostnames], row[columnOfEnvironments], (row[columnOfServerType])
    
                hostname = str(row[columnOfHostnames])
                environment = stripDashChars(str(row[columnOfEnvironments]))
                serverType = stripDashChars(str(row[columnOfServerType]))
                    
                excludeThis = False
                if (excludesList) :
                    for entry in excludesList:
                        if ((str(entry).lower() in hostname) or (str(entry).lower() in environment) or (str(entry).lower() in serverType)) :
                            excludeThis = True
    
                        if ((str(entry).upper() in hostname) or (str(entry).upper() in environment) or (str(entry).upper() in serverType)) :
                            excludeThis = True
                    
                    if (excludeThis == False):
                        aHostEntry = hostEntry(hostname, environment, serverType)
                        hostEntries.add(aHostEntry)
                        allHosts.add(hostname)
                        allServerTypes.add(serverType)
                        
                        if not(environment in allEnvironments) : allEnvironments.add(environment)
                        appendToFile('\t"' + hostname + '",\n', inventoryPythonOutputFile)
                    
                else:
                    if not(environment in allEnvironments) : allEnvironments.add(environment)        
                    appendToFile('\t"' + hostname + '",\n', inventoryPythonOutputFile)
                        
            rowCount = rowCount +1
    
        appendToFile("\n]\n\n", inventoryPythonOutputFile)

        # all environments
        appendToFile('allEnvironments = [\n', inventoryPythonOutputFile)
        for anEnvironment in allEnvironments :
            print 'environment: ' + anEnvironment
            appendToFile('\t"' + anEnvironment + '",\n', inventoryPythonOutputFile)        
            
        appendToFile("\n]\n\n", inventoryPythonOutputFile)
            
    
    # hosts in an environment...        
    for anEnvironment in allEnvironments :
        print 'Environment: ' + anEnvironment
        appendToFile('env_' + anEnvironment + ' = [\n', inventoryPythonOutputFile)
        for aHostEntry in hostEntries :
            if (anEnvironment in aHostEntry.environment):
                print 'Environment: ' + anEnvironment + ' host: ' + aHostEntry.hostname    
                
                appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
        
        appendToFile("\n]\n\n", inventoryPythonOutputFile)
    
    # hosts in their environment by type...
    for anEnvironment in allEnvironments :
        for aServerType in allServerTypes :
            print 'server type: ' + aServerType
            appendToFile('env_' + anEnvironment + '_type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
            for aHostEntry in hostEntries :
                if (aServerType in aHostEntry.type) and (anEnvironment in aHostEntry.environment):
                    print 'Environment: ' + anEnvironment + ' host: ' + aHostEntry.hostname    
                    
                    appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
            
            appendToFile("\n]\n\n", inventoryPythonOutputFile)
        
    # hosts by type
    for aServerType in allServerTypes :
        print 'server type: ' + aServerType
        appendToFile('type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
        for aHostEntry in hostEntries :
            if (aServerType in aHostEntry.type):
                print 'Environment: ' + anEnvironment + ' host: ' + aHostEntry.hostname    
                
                appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
        
        appendToFile("\n]\n\n", inventoryPythonOutputFile)

# e.g. pullHostnamesIntoInventorySingleEnvironment('./mySatExport.csv', 'pyInventory.py', 1, 6, ['myExclude1', 'myExclude2'])    
def pullSatelliteExportIntoInventorySingleEnvironment(csvInputFile, inventoryPythonOutputFile, columnOfHostnames, columnOfServerType):
    # init file
    writeToFile("\n", inventoryPythonOutputFile)
    
    hostEntries = Set()
    allHosts = Set()
    allEnvironments = Set()
    allServerTypes = Set()
    with open(csvInputFile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        
        appendToFile("allHosts = [\n", inventoryPythonOutputFile)
        rowCount = 0
        for row in csvReader:
            if rowCount > 0 :
                print row[columnOfHostnames], stripDashChars(row[columnOfServerType])
    
                hostname = str(row[columnOfHostnames])
                serverType = str(row[columnOfServerType])
    
                aHostEntry = hostEntry(hostname, "", serverType)
                hostEntries.add(aHostEntry)
                allHosts.add(hostname)
                allServerTypes.add(serverType)
                    
                appendToFile('\t"' + hostname + '",\n', inventoryPythonOutputFile)

            rowCount = rowCount +1
    
        appendToFile("\n]\n\n", inventoryPythonOutputFile)

    # all environments
    appendToFile('allEnvironments = [\n', inventoryPythonOutputFile)
    for anEnvironment in allEnvironments :
        print 'environment: ' + anEnvironment
        appendToFile('\t"' + anEnvironment + '",\n', inventoryPythonOutputFile)        
        
            
    # hosts in an environment...
    for anEnvironment in allEnvironments :
        print 'Environment: ' + anEnvironment
        appendToFile('env_' + anEnvironment + ' = [\n', inventoryPythonOutputFile)
        for aHostEntry in hostEntries :
            if (anEnvironment in aHostEntry.environment):
                print 'Environment: ' + anEnvironment + ' host: ' + aHostEntry.hostname    
                
                appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
        
        appendToFile("\n]\n\n", inventoryPythonOutputFile)
    
    # hosts in their environment by type...
    for anEnvironment in allEnvironments :
        for aServerType in allServerTypes :
            print 'server type: ' + aServerType
            appendToFile('env_' + anEnvironment + '_type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
            for aHostEntry in hostEntries :
                if (aServerType in aHostEntry.type) and (anEnvironment in aHostEntry.environment):
                    print 'Environment: ' + anEnvironment + ' host: ' + aHostEntry.hostname    
                    
                    appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
            
            appendToFile("\n]\n\n", inventoryPythonOutputFile)
        

    # hosts by type
    for aServerType in allServerTypes :
        print 'server type: ' + aServerType
        appendToFile('type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
        for aHostEntry in hostEntries :
            if (aServerType in aHostEntry.type):
                print 'Environment: ' + "" + ' host: ' + aHostEntry.hostname    
                
                appendToFile('\t"' + aHostEntry.hostname + '",\n', inventoryPythonOutputFile)
        
        appendToFile("\n]\n\n", inventoryPythonOutputFile)        
