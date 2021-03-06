'''
Created on 14 Oct 2016

@author: ...
'''
import errno
import os
import re
from string import split
from threading import Thread
from time import sleep
from tokenize import String

from java.lang import StringBuilder
from java.util import Properties
from com.jcraft.jsch import JSch

scatterGatherThreadPool = []

def addQuotes(stringToAugment):
    newString = stringToAugment

    return "\"" + newString + "\""

def stripQuotes(stringToStrip):
    newString = stringToStrip

    if (stringToStrip.startswith("\"")) and (stringToStrip.endswith("\"")) :
        newString = stringToStrip[1:-1]

    if (stringToStrip.startswith("\'")) and (stringToStrip.endswith("\'")) :
        newString = stringToStrip[1:-1]

    return newString

def stripNonChars(stringToStrip):
    newString = ""

    for char in stringToStrip:
        if (char == '\n'):
            newString = newString + '_'
        elif (char == '\\'):
            newString = newString + '_'
        elif (char == '/'):
            newString = newString + '_'
        elif (char == ' '):
            newString = newString + '_'
        elif (char == '.'):
            newString = newString + '_'
        else :
            newString = newString + char
 
    return newString

    return newString

def stripCTRLChars(stringToStrip):
    newString = ''
 
    for char in stringToStrip:
        if (char == '\n'):
            newString = newString + ' | '
        elif (char == ','):
            newString = newString + ' | '
        else :
            newString = newString + char
 
    return newString

def stripDashChars(stringToStrip):
    newString = ''
 
    for char in stringToStrip:
        if (char == '-'):
            newString = newString + '_'
        if (char == ' '):
            newString = newString + '_'
        else :
            newString = newString + char
 
    return newString
  
def checkThenAddQuotes(stringToCheck):
    newString = stringToCheck

    if (stringToCheck.startswith("\"")) and (stringToCheck.endswith("\"")) :
        return newString

    if (stringToCheck.startswith("\'")) and (stringToCheck.endswith("\'")) :
        return newString

    newString = '"' + newString + '"'
    return newString

def writeToFile(stringToWrite, destFileName):
    f1 = open(destFileName, 'w')
    f1.write(stringToWrite)
    f1.flush()
    f1.close()

def appendToFile(stringToWrite, destFileName):
    f1 = open(destFileName, 'a')
    f1.write(stringToWrite)
    f1.flush()
    f1.close()

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            None
            # raise

def regularExpressionSearch(stringToFindRegularExpression, stringToSearch):

    try:
        found = re.search(stringToFindRegularExpression, stringToSearch).group(1)
    except AttributeError:
        found = ''  # apply your error handling

    return found

def replaceText(sourceString, findText, replaceText):
    # find replace that works better than str.replace()
    sourceEx = sourceString.split(findText)

    newString = ''
    itemCount = 0
    for item in sourceEx:
        itemCount += 1
        if (itemCount == 1) :
            newString = str(item)
        else :
            newString = newString + str(replaceText) + str(item)

    return newString

def sanitizeJDBCCliVector(cliVector):

    dsName = regularExpressionSearch("/subsystem=datasources/data-source=(.*)", cliVector)
    dsXAName = regularExpressionSearch("/subsystem=datasources/xa-data-source=(.*)", cliVector)

    newCliVector = ''
    
    if (dsName != "") :
        actualDSName = dsName
    elif (dsXAName != "") :
        actualDSName = dsXAName

    splitExpression = split(actualDSName, "/", -1)
    newDSNameAndParams = ""
    subExpressionCount = 1
    if (len(splitExpression) > 1) :
        for subExpression in splitExpression :
            if (subExpressionCount == 1) and (str(actualDSName).startswith("jdbc/")) :
                newDSNameAndParams = newDSNameAndParams + subExpression + '\/'
            elif (subExpressionCount < len(splitExpression) -1) :
                newDSNameAndParams = newDSNameAndParams + subExpression + '/'
            else :
                newDSNameAndParams = newDSNameAndParams + subExpression
                    
            subExpressionCount = subExpressionCount + 1

        if (dsName != "") :
            newCliVector = "/subsystem=datasources/data-source=" + newDSNameAndParams
        elif (dsXAName != "") :
            newCliVector = "/subsystem=datasources/xa-data-source=" + newDSNameAndParams

    else :
        newCliVector = cliVector
        
    if not(str(newCliVector)[len(newCliVector)-1] == '/') :
        newCliVector = newCliVector + '/'        

    return newCliVector

def findReplaceIntoNewFile(stringToFind, stringToSet, origFileName, destFileName):
    f1 = open(origFileName, 'r')
    f2 = open(destFileName, 'w')
    for line in f1:
        f2.write(line.replace(stringToFind, stringToSet))
    f1.close()
    f2.close()

def findReplaceIntoSameFile(stringToFind, stringToSet, fileName):
    # Read in the file
    filedata = None
    with open(fileName, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace(stringToFind, stringToSet)

    # Write the file out again
    with open(fileName, 'w') as file:
        file.write(filedata)

def scatterThread(strThreadPoolId, targetMethod, args=None):
    thread = Thread(target=targetMethod, args=args)
    scatterGatherThreadPool.append(dict({strThreadPoolId: thread}))
    
    thread.start() 

def gatherThreads(strThreadPoolId):
    
    localThreadsList = []
    
    for threadDictEntry in scatterGatherThreadPool: 
        if (dict(threadDictEntry).get(strThreadPoolId) != None):
            localThreadsList.append(threadDictEntry.get(strThreadPoolId))
            
    # Wait for all threads to complete
    for t in localThreadsList:
        t.join()

def execSshRemote(hostname, username, identityFileFullPath, identityPassword, commandsSemiColonSeperated, sessionTimeoutSecs = 0, waitForOutput = True):
    _hostname = hostname
    _username = username
    _identityPassword = identityPassword
    _command = commandsSemiColonSeperated
 
    jsch = JSch()
    jsch.addIdentity(identityFileFullPath, _identityPassword)
 
    session = jsch.getSession(_username, _hostname, 22)
    config = Properties()
    config.put("StrictHostKeyChecking", "no")
    config.put("GSSAPIAuthentication", "no")
    config.put("UnknownHostVerification", "no")
    config.put("PreferredAuthentications", "publickey");
    session.setConfig(config);
 
    if (sessionTimeoutSecs > 0) : session.setTimeout(sessionTimeoutSecs * 10)

    print 'Logging into Remote SSH Shell key Auth...'    
 
    try:
        if (sessionTimeoutSecs > 0) :
            session.connect(sessionTimeoutSecs * 1000)
        else:
            session.connect()            
    except:
        return 'None'
 
    channel = session.openChannel("exec")
    channel.setCommand('source ~/.bash_profile 2>/dev/null; ' + _command)
 
    outputBuffer = String();

    stdin = channel.getInputStream();
    stdinExt = channel.getExtInputStream();
 
    channel.connect(sessionTimeoutSecs * 1000);
 
    if(waitForOutput == True):
        while (1) :
            n = stdin.read()
            if n == -1:
                break
            if (chr(n) == '\n'):
                outputBuffer.append('|')
            elif (chr(n) == '\r'):
                outputBuffer.append('|')
            else :
                outputBuffer.append(chr(n))
    
        while (1) :
            n = stdinExt.read()
            if n == -1:
                break
            if (chr(n) == '\n'):
                outputBuffer.append('|')
            elif (chr(n) == '\r'):
                outputBuffer.append('|')
            else :
                outputBuffer.append(chr(n))
    else :
        sleep(sessionTimeoutSecs)
                        
    print "Command on: " + hostname + " : " + _command
    print "\toutput: " + outputBuffer.toString()
    
    channel.disconnect()
    session.disconnect()
    
    del channel    
    del session    
    
    return outputBuffer.toString()

def execSshRemoteUsrPwd(hostname, username, password, commandsSemiColonSeperated, sessionTimeoutSecs = 0, waitForOutput = True):
    _hostname = hostname
    _username = username 
    _password = password
    _command = commandsSemiColonSeperated
    
    jsch = JSch()
    
    session = jsch.getSession(_username, _hostname, 22)
    session.setPassword(_password);
    config = Properties()
    config.put("StrictHostKeyChecking", "no")
    config.put("GSSAPIAuthentication", "no")
    config.put("UnknownHostVerification", "no")
    #config.put("PreferredAuthentications", "publickey");
    session.setConfig(config);
    
    if (sessionTimeoutSecs > 0) : session.setTimeout(sessionTimeoutSecs * 10)

    print 'Logging into Remote SSH Shell u/p Auth...'
    
    try:
        if (sessionTimeoutSecs > 0) :
            session.connect(sessionTimeoutSecs * 1000)
        else:
            session.connect()            
    except:
        return 'None'
    
    channel = session.openChannel("exec")
    channel.setCommand('source ~/.bash_profile 2>/dev/null; ' + _command)
    
    outputBuffer = String();
    
    stdin = channel.getInputStream();
    stdinExt = channel.getExtInputStream();
    
    channel.connect(sessionTimeoutSecs * 1000);
            
    if(waitForOutput == True):
        while (1) :
            n = stdin.read()
            if n == -1:
                break
            if (chr(n) == '\n'):
                outputBuffer.append('|')
            elif (chr(n) == '\r'):
                outputBuffer.append('|')
            else :
                outputBuffer.append(chr(n))
        
        while (1) :
            n = stdinExt.read()
            if n == -1:
                break
            if (chr(n) == '\n'):
                outputBuffer.append('|')
            elif (chr(n) == '\r'):
                outputBuffer.append('|')
            else :
                outputBuffer.append(chr(n))
 
    else :
        sleep(sessionTimeoutSecs)
        
    print "Command on: " + hostname + " : " + _command
    print "\toutput: " + outputBuffer.toString()

    channel.disconnect()
    session.disconnect()

    del channel
    del session    
        
    return outputBuffer.toString()
