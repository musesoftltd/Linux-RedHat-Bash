'''
Created on 11 Oct 2017

@author: ...
'''
import datetime

from linuxProperties import linuxPropertiesDict

from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditInitAudit, auditReport
from library.mdm.auditServerMDM import auditServersMdm

def completeChecksMdm(env, serverList, propertiesDict, bApplyRequiredChanges):
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    #runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    for servername in serverList :
        auditServersMdm(env, servername, runtimeProperties["usernameMdm"], propertiesDict, bApplyRequiredChanges)
    
        auditingLibrary.auditObjectAtoms.append(auditingLibrary.auditObjectAtomCompleteAnAction(servername, runtimeProperties["usernameMdm"], runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'JVM Mem Opts', 'source ~/.bash_profile; grep -ia \'Xmx\' \'/opt/install/EAP-6.4.0/bin/standalone.conf\''))
    
        auditReport(env, servername)

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "MDM")

completeChecksMdm('PreProd1ServersMdm', ['localhost', '127.0.0.1'], linuxPropertiesDict, bApplyRequiredChanges)

exit()