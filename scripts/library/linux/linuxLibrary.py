'''
@author:
'''

from __builtin__ import None
from java.lang import String

from library.util import execSshRemote, execSshRemoteUsrPwd

def rshCommand(env, hostname, username, identityFileFullPath, password, _command):
    command = _command
    
    if (String(identityFileFullPath).contains(':') or String(identityFileFullPath).contains('\\') or String(identityFileFullPath).contains('/')) :
        print 'On Server :' + hostname + ' RSH issuing command: >' + _command + '<'
        output = execSshRemote(hostname, username, identityFileFullPath, password, command)
    else :
        output = execSshRemoteUsrPwd(hostname, username, password, command)
        
    print 'On Server :' + hostname + ' RSH Returned: ' + output
          
    return output

def getParameterValue(env, servername, username, idendityFileFullPath, idendityFilePassword, fileVector, grepDetail):

    try:
        print 'On Server :' + servername + ' retrieving ->' + grepDetail + '<- from File Vector ->' + fileVector + '<- ...'

        command = "/bin/grep -ia \'" + grepDetail + "\'" + " \'" + fileVector + "\'"
        currentValue = rshCommand(env, servername, username, idendityFileFullPath, idendityFilePassword, command)
              
        print 'On Server :' + servername + ' retrieving ->' + grepDetail + '<- from File Vector ->' + fileVector + '<- ...end.'

    finally:
        None
    
    return currentValue 

def setParameterValue(env, servername, username, passwordOrIdFileFullPath, fileVector, strToFind, targetValue, reloadServerIfRequired=False) : 

    print 'On Server :' + servername + ' applying ->' + targetValue + '<- to ' + strToFind + ' at file Vector Vector ->' + fileVector + '<- ...'
    try:
            command = "sed -i -- 's/" + strToFind + "/" + targetValue + "/g'" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, command)
            
            command = "grep -ia '"+ targetValue + "'" + " '" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, command)
    finally:
        None
    
    print 'On Server :' + servername + ' applying ->' + targetValue + '<- to ' + strToFind + ' at file Vector Vector ->' + fileVector + '<- ...end.'
    return True 
