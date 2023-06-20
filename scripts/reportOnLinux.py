'''
Created on 11 Oct 2017

@author: ...
'''
import datetime

from library.auditing import auditingLibrary
from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditInitAudit, auditReport
from linuxProperties import linuxPropertiesDict

def completeChecks(env, serverList, propertiesDict, bApplyRequiredChanges):
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    #runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    for servername in serverList :
        auditServersBaseAudit(env, servername, runtimeProperties["username"], propertiesDict, bApplyRequiredChanges)

        auditingLibrary.auditObjectAtoms.append(auditingLibrary.auditObjectAtomCompleteAnActionAuditAction(servername, runtimeProperties["username"], runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'ULimit', 'lsof | wc -l', '1024'))    

        auditReport(env, servername)

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "Base Linux")

completeChecks('preProdServers', ['localhost', '127.0.0.1'], linuxPropertiesDict, bApplyRequiredChanges)

exit()