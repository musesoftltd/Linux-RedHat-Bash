'''
@author:
'''

from __builtin__ import None
from java.lang import String

from library.util import execSshRemote, execSshRemoteUsrPwd

def rshCommand(env, hostname, username, identityFileFullPath, password, _command):
    command = _command
    
    print ('On Server :' + hostname + ' RSH issuing command: >' + _command + '<')
    if (String(identityFileFullPath).contains(':') or String(identityFileFullPath).contains('\\') or String(identityFileFullPath).contains('/')) :
        output = execSshRemote(hostname, username, identityFileFullPath, password, command)
    else :
        output = execSshRemoteUsrPwd(hostname, username, password, command)
        
    print ('On Server :' + hostname + ' RSH Returned: ') + output
          
    return output

def getParameterValue(env, servername, username, idendityFileFullPath, idendityFilePassword, fileVector, grepDetail):

    try:
        print ('On Server :' + servername + ' retrieving ->' + grepDetail + '<- from File Vector ->' + fileVector + '<- ...')

        command = "/bin/grep -ia \'" + grepDetail + "\'" + " \'" + fileVector + "\'"
        currentValue = rshCommand(env, servername, username, idendityFileFullPath, idendityFilePassword, command)
              
        print ('On Server :' + servername + ' retrieving ->' + grepDetail + '<- from File Vector ->' + fileVector + '<- ...end.')

    finally:
        None
    
    return currentValue 

def setParameterValue(env, servername, username, passwordOrIdFileFullPath, password, fileVector, strToFind, targetValue, reloadServerIfRequired=False) : 

    print ('On Server :' + servername + ' applying ->' + targetValue + '<- to ->' + strToFind + '<- at file Vector ->' + fileVector + '<- ...')
    try:
            command = "sed -i -- s/" + strToFind + "/" + targetValue + "/g '" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, password, command)
            
            command = "grep -ia '"+ targetValue + "'" + " '" + fileVector + "'"
            rshCommand(env, servername, username, passwordOrIdFileFullPath, password, command)
    finally:
        None
    
    print ('On Server :' + servername + ' applying ->' + targetValue + '<- to ->' + strToFind + '<- at file Vector ->' + fileVector + '<- ...end.')
    return True 
