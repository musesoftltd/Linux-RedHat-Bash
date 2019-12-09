'''
Created on 10 May 2019

@author: ...
'''

import csv
from sets import Set
from string import lowercase, uppercase

from library.util import appendToFile, writeToFile, stripCTRLChars, stripNonChars


class hostEntry:
    hostname = ""
    environment = ""
    type = ""
    ipAddr = ""
    def __init__(self, hostname, environment, type):
        self.hostname = hostname
        self.environment = environment
        self.type = type

# importSatIntoInventoryMultiEnvironmentExcluding(csvFile, inventoryPythonOutputFile, columnOfHostnames, columnOfServerType, columnOfEnvironments, excludesList)(
def importSatIntoInventoryMultiEnvironmentExcluding(csvFile, inventoryPythonOutputFile, columnOfHostnames, columnOfServerType, columnOfEnvironments, excludesList):
    # init file
    writeToFile("\n", inventoryPythonOutputFile)

    hostEntries = Set()
    allHosts = Set()
    allEnvironments = Set()
    allServerTypes = Set()
    with open(csvFile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        appendToFile("allHosts = [\n", inventoryPythonOutputFile)
        rowCount = 0

        for row in csvReader:
            if (rowCount > 0) : # ignore title row..
                excludeThis = False
                if (excludesList.count > 0) : # if we have to consider and excludes list
                    for excludeEntry in excludesList:
                        for columnEntry in row :
                            if (str(excludeEntry).lower() in columnEntry) :
                                excludeThis = True
                                break

                            if (str(excludeEntry).upper() in columnEntry) :
                                excludeThis = True
                                break

                    if (not excludeThis) : # if not excluded
                        if len(row) >= columnOfHostnames and len(row) >= columnOfEnvironments and len(row) >= columnOfServerType :
                            print 'Row:' + str(rowCount) + ', ' +  row[columnOfHostnames] + ', ' + row[columnOfEnvironments] + ', ' + row[columnOfServerType]
                            #print row[columnOfHostnames], row[columnOfEnvironments], (row[columnOfServerType])


                            hostname = str(row[columnOfHostnames])
                            environment = stripNonChars(str(row[columnOfEnvironments]))
                            serverType = stripNonChars(str(row[columnOfServerType]))

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
            appendToFile('env_' + anEnvironment + '_Type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
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

# importSatIntoInventoryMultiEnvironmentIncluding(csvFile, inventoryPythonOutputFile, columnOfHostnames, columnOfServerType, columnOfEnvironments, includesList)(
def importSatIntoInventoryMultiEnvironmentIncluding(csvFile, inventoryPythonOutputFile, columnOfHostnames, columnOfServerType, columnOfEnvironments, includesList):
    # init file
    writeToFile("\n", inventoryPythonOutputFile)

    hostEntries = Set()
    allHosts = Set()
    allEnvironments = Set()
    allServerTypes = Set()
    with open(csvFile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)

        appendToFile("allHosts = [\n", inventoryPythonOutputFile)
        rowCount = 0

        for row in csvReader:
            if (rowCount > 0) :
                includeThis = False
                if (includesList.count > 0) : # if we have to consider and excludes list
                    for includeEntry in includesList:
                        for columnEntry in row :
                            if (str(includeEntry).lower() in columnEntry) :
                                includeThis = True
                                break

                            if (str(includeEntry).upper() in columnEntry) :
                                includeThis = True
                                break

                    if (includeThis) : # if not included
                        if len(row) >= columnOfHostnames and len(row) >= columnOfEnvironments and len(row) >= columnOfServerType :
                            print 'Row:' + str(rowCount) + ', ' +  row[columnOfHostnames] + ', ' + row[columnOfEnvironments] + ', ' + row[columnOfServerType]
                            #print row[columnOfHostnames], row[columnOfEnvironments], (row[columnOfServerType])


                            hostname = str(row[columnOfHostnames])
                            environment = stripNonChars(str(row[columnOfEnvironments]))
                            serverType = stripNonChars(str(row[columnOfServerType]))

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
            appendToFile('env_' + anEnvironment + '_Type_' + aServerType + ' = [\n', inventoryPythonOutputFile)
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
