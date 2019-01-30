'''
Created on 11 Oct 2016

@author: ...
'''

import datetime
import os

from library.linux.linuxLibrary import setParameterValue, getParameterValue, \
    rshCommand
from library.util import mkdir_p, appendToFile, stripQuotes, \
    stripCTRLChars


datetimeSuffix = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H.%M.%S')

global auditFileName
auditFileName =  ''
global reportFileName
reportFileName = ''

# Globals
global currentAuditReportServer
currentAuditReportServer = ""

global currentAuditReportEnvironment
currentAuditReportEnvironment = ""

global globalReportsStarted
globalReportsStarted = False

global auditReportPath
auditReportPath = ''

global strEnvironment
strEnvironment = ''
global strTechnologyType
strTechnologyType =''

# list of audit objects.
auditObjectAtoms = []
auditObjectMolecules = []

def getReportDirectory():
    global globalReportsStarted
    global auditReportPath

    if not(globalReportsStarted):
        globalReportsStarted = True

        try :
            auditReportPath = os.environ['WORKSPACE'] + '/reports/'
            print "Jenkins Environment Workspace Path: " + auditReportPath
        except:
            None

        if (auditReportPath == "") :
            auditReportPath = "../reports/"
            print "Report Path: " + auditReportPath

        mkdir_p(auditReportPath)

    return auditReportPath
 
    print "Generating Reports in: " +  getReportDirectory()
 
def appendToReport(strToAppend):
#     if (reportFileName == '') :
    reportFilename = getReportDirectory() + 'managerial-linux' + '-' + strTechnologyType + '-' + strEnvironment + '-' + datetimeSuffix  + '.csv'
 
    appendToFile(strToAppend, reportFilename)

def appendToAudit(strToAppend):

#     if (auditFileName == '') :
    auditFileName = getReportDirectory() + 'technical-linux' + '-' + strTechnologyType + '-' + strEnvironment + '-' + datetimeSuffix  + '.csv'
 
    appendToFile(strToAppend, auditFileName)

# enables the user to group atoms together as one
class auditObjectMolecule:
    auditTitle = ""
    servername = ''
    auditObjectAtoms = []
    allPassed = True # Assume true and try to disprove
    somePassed = False

    allMustPass = True
    auditResult = ""

    titledAlready = False
    reportedAlready = False

    def __init__(self, auditTitle, servername, bAllMustPass):
        self.auditObjectAtoms = []
        self.allPassed = True # Assume true and try to disprove
        self.auditTitle = auditTitle
        self.servername = servername
        self.allMustPass = bAllMustPass

        # register with the list of molecules
        auditObjectMolecules.append(self)

    def renderIntoReport(self):
        global strEnvironment
        global strTechnologyType

        if not(self.reportedAlready) :
            for auditObjectAtom in self.auditObjectAtoms:
                if (auditObjectAtom.auditPassed == False):
                    self.allPassed = False
                else:
                    self.somePassed = True

            if (self.somePassed == False) :
                self.allPassed = False

            if (self.allPassed):
                appendToReport('...' + ',')
            elif ( (self.somePassed) & (self.allMustPass == False)) :
                appendToReport('...' + ',')
            elif (self.auditResult != ""):
                appendToReport(self.auditResult + ',')
            else:
                appendToReport('ToDo' + ',')

        self.reportedAlready = True

# OO based auditing atom - automatically reported on
class auditObjectAtom():
    servername = ""
    username = ""
    password = ""
    identityFileFullPath = ""
 
    auditTitle = ""

    cliVector = ""
    cliProperty = ""
 
    currentValue = ""
    targetValue = ""

    auditPassed = False
    auditResult = ""

    titledAlready = False
    reportedAlready = False

    def __init__(self, servername, username, identityUserOrFileFullPath, password, auditTitle, cliVector, grepTarget, targetValue, bApplyTargetValue):
        self.servername = servername
        self.auditTitle = auditTitle
        self.cliVector = cliVector
        self.cliProperty = str(grepTarget)
        self.targetValue = str(targetValue)

        self.auditPassed = False

        self.returnResult = self.audit(servername, username, identityUserOrFileFullPath, password)
        if ((self.auditPassed == False) & (bApplyTargetValue)):
            self.applyTargetValue()
            self.audit(servername, username, identityUserOrFileFullPath, password)

    def auditWriteAudit(self):
        targetValue = ""
        currentValue = ""

        if (self.auditPassed == True):
            passFailRecord = 'Pass'
        else :
            passFailRecord = 'Fail *'

        if (self.targetValue == "") :
            targetValue = "NotSpecified"
        else :
            targetValue = self.targetValue

        if (self.currentValue == "") :
            currentValue = "Unknown"
        else :
            currentValue = self.currentValue

        appendToAudit('Env:' + strEnvironment + ' : ' + self.servername + ',' + passFailRecord + ',' + self.auditTitle + ',current:"' + currentValue + '",target:"' + targetValue + '"\n')

    def applyTargetValue(self):
        print 'On Server: ' + self.servername + ' Applying : ' + self.auditTitle + '...'
        result = setParameterValue(currentAuditReportEnvironment, self.servername, self.username, self.password, self.cliVector, self.cliProperty, self.targetValue)
        if (result == True) :
            self.auditPassed = result
        else:
            self.auditPassed = False
            self.auditResult = "Unknown"
            print 'Setting value: ' + self.targetValue + ' ' + self.auditTitle + ' for server: ' + self.servername + '...FAILED'

        print 'On Server: ' + self.servername + ' Applying : ' + self.auditTitle + '...end.'

        return self.auditResult

    def audit(self, servername, username, identityFileFullPath, password):
        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...'
        self.currentValue = getParameterValue(currentAuditReportEnvironment, servername, username, identityFileFullPath, password, self.cliVector, self.targetValue)
        self.auditResult = self.currentValue
        print 'Target Value: ' + self.targetValue
        print 'Actual Value: ' + self.currentValue
        # This is a hack because we use \" to set some values
        # But they will come back on read without \", so the compare fails
        # although the values are the same
        if (self.targetValue.isdigit()) :
            if (self.targetValue == self.currentValue):
                print 'Auditing: ' + self.auditTitle + '...Passed.'
                self.auditPassed = True
            else:
                print 'Auditing: ' + self.auditTitle + '...FAILED.'
                self.auditPassed = False
        else :
            if (stripQuotes(self.targetValue) in self.currentValue):
                print 'Auditing: ' + self.auditTitle + '...Passed.'
                self.auditPassed = True
            else:
                print 'Auditing: ' + self.auditTitle + '...FAILED.'
                self.auditPassed = False

        self.auditWriteAudit()

        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...end.'

        print '\n'

    def renderIntoReport(self):
        if not(self.reportedAlready) :
            if (self.auditPassed) :
                appendToReport('...' + ',')
            elif (self.auditResult == 'False') :
                appendToReport(str('ToDo') + ',')
            elif (str(self.auditResult) == 'Unknown') :
                appendToReport("ToDo" + ',')
            else :
                appendToReport('ToDo' + ',')

        self.reportedAlready = True;

class auditObjectAtomCompleteAnAction():
    servername = ""
    username = ""
    password = ""
    identityFileFullPath = ""
 
    auditTitle = ""

    cliVector = ""
    cliProperty = ""
 
    currentValue = ""
    targetValue = ""

    auditPassed = False
    auditResult = ""
    
    command = ""

    titledAlready = False
    reportedAlready = False

    def __init__(self, servername, username, identityUserOrFileFullPath, password, auditTitle, command):
        self.servername = servername
        self.auditTitle = auditTitle
        self.auditPassed = False
        self.command = command
        self.returnResult = self.audit(servername, username, identityUserOrFileFullPath, password)

    def auditWriteAudit(self):
        targetValue = ""
        currentValue = ""

        passFailRecord = 'Success'

        appendToAudit('Env:' + strEnvironment + ' : ' + self.servername + ',' + passFailRecord + ',' + self.auditTitle + ',current:"' + currentValue + '\n')

    def audit(self, servername, username, identityFileFullPath, password):
        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...'
        self.currentValue = rshCommand(currentAuditReportEnvironment, servername, username, identityFileFullPath, password, self.command)
        self.auditResult = self.currentValue
        print 'Actual Value: ' + self.currentValue
        # This is a hack because we use \" to set some values
        # But they will come back on read without \", so the compare fails
        # although the values are the same
        self.auditPassed = True

        self.auditWriteAudit()

        print 'On Server: ' + servername + ' Auditing : ' + self.auditTitle + '...end.'

        print '\n'

    def renderIntoReport(self):
        if (self.currentValue == ''):
            appendToReport("\"" + 'NOP' + '\"' + ',')
        else :
            appendToReport("\"" + stripCTRLChars(self.currentValue) + '\"' + ',')
        self.reportedAlready = True;
        
def auditInitAudit(environment, technologyType):
    global strEnvironment
    global strTechnologyType

    strEnvironment = environment
    strTechnologyType = technologyType

    appendToAudit('Server, Test Result, Test' + '\n')

    appendToReport('Muse,https://urldefense.proofpoint.com/v2/url?u=https-3A__sourceforge.net_projects_museproject_&d=DwIGAg&c=7HXQkpfw9RhjnklpS1w2AQ&r=XsB2ya1EgJmj_cY8EXjosQwrOHNISxyT2N7bmLSzDII&m=VydaG-Z4GOoJ2zRpJv0fbTerT1Bl2fdoinV8E8Bcszo&s=h4ehOUF8Qrv-3Crvrg9FRFNBwZ374Dwlxkk60h8hYgg&e= ' + '\n')
    appendToReport('Linux Audit' + '\n')

def auditWriteAudit(server, auditText, bAuditPassed):
    passFailRecord = ""

    if (bAuditPassed == True):
        passFailRecord = 'Pass'
    else :
        passFailRecord = 'Fail *'

    appendToAudit(server + ',' + passFailRecord + ',\'' + auditText + '\'\n')

def auditReport(environment, currentServerName):
    global currentAuditReportServer
    global currentAuditReportEnvironment
    global reportFirstRow
    global strEnvironment
    global strTechnologyType

    print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...'

    ############################################################################
    # HEADING of Report...
    ############################################################################
    if (currentAuditReportEnvironment != environment) :
        currentAuditReportEnvironment = environment

        appendToReport("\nEnv: " + environment + "\n")

        appendToReport('Server' + ',')

        for auditObjectAtom in auditObjectAtoms :
            if not(auditObjectAtom.titledAlready):
                if (auditObjectAtom.servername == currentServerName) :
                    appendToReport(auditObjectAtom.auditTitle + ',')
                    auditObjectAtom.titledAlready = True

        for auditObjectMolecule in auditObjectMolecules:
            if not(auditObjectMolecule.titledAlready):
                if (auditObjectMolecule.servername == currentServerName) :
                    appendToReport('\'' + auditObjectMolecule.auditTitle + '\'' + ',')
                    auditObjectMolecule.titledAlready = True

                # only update the environemnt has changed on successful reporting of something
                # from at leaat one server.

        appendToReport('\n')

    ############################################################################

    ############################################################################
    # Data ROW of Report...
    ############################################################################
    appendToReport(currentServerName + ',')

    for auditObjectAtom in auditObjectAtoms:
        if not(auditObjectAtom.reportedAlready):
            if (auditObjectAtom.servername == currentServerName):
                auditObjectAtom.renderIntoReport()
                auditObjectAtom.reportedAlready = True;

    for auditObjectMolecule in auditObjectMolecules:
        if not(auditObjectMolecule.reportedAlready):
            if (auditObjectMolecule.servername == currentServerName):
                auditObjectMolecule.renderIntoReport()
                auditObjectMolecule.reportedAlready = True;

    appendToReport('\n')
 
    currentAuditReportServer = currentServerName
    currentAuditReportEnvironment = environment
 
    print 'auditReport for server : ' + currentServerName + ' in environment : ' + environment + '...end.'
