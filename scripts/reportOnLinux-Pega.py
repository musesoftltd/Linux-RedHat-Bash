'''
Created on 11 Oct 2017

@author: ...
'''
import datetime

from linuxProperties import linuxPropertiesDict

from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditInitAudit, auditReport
from library.pega.auditServerPega import auditServersPega
from library.auditing import auditingLibrary

def completeChecksPega(env, serverList, propertiesDict, bApplyRequiredChanges):
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    #runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    for servername in serverList :
        auditServersPega(env, servername, runtimeProperties["usernamePega"], propertiesDict, bApplyRequiredChanges)

        auditingLibrary.auditObjectAtoms.append(auditingLibrary.auditObjectAtomCompleteAnAction(servername, runtimeProperties["usernamePega"], runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'JVM Mem Opts', 'source ~/.bash_profile; grep -ia \'Xmx\' \'/opt/jboss/EAP-6.4.0/bin/standalone.conf\''))
    
        auditReport(env, servername)

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "Pega")

completeChecksPega('preProdServersPega', ['127.0.1.1',], linuxPropertiesDict, bApplyRequiredChanges)

exit()