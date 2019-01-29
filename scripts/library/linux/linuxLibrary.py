'''
@author:
'''

from __builtin__ import None
from java.lang import String

from library.util import execSshRemote, execSshRemoteUsrPwd

def rshCommand(env, hostname, username, identityFileFullPath, password, _command):
    command = _command
    
    if (String(identityFileFullPath).contains(':') or String(identityFileFullPath).contains('\\') or String(identityFileFullPath).contains('/')) :
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

def setParameterValue(env, servername, username, passwordOrIdFileFullPath, fileVector, grepDetail, targetValue, reloadServerIfRequired=False) : 

    print 'On Server :' + servername + ' applying ->' + targetValue + '<- to file Vector Vector ->' + fileVector + '<- ...'
    try:
            command = "source ~/.bash_profile 2>/dev/null; sed -i -- 's/" + grepDetail + "/" + targetValue + "/g'" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, command)
            
            command = "source ~/.bash_profile 2>/dev/null; grep -ia '"+ grepDetail + "'" + " '" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, command)
    finally:
        None
    
    print 'On Server :' + servername + ' applying ->' + targetValue + '<- to file Vector ->' + fileVector + '<- ...end.'
    return True 
