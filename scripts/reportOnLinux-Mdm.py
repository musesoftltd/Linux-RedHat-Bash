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
        auditServersMdm(env, servername, runtimeProperties["hostUsername"], propertiesDict, bApplyRequiredChanges)
    
        auditReport(env, servername)

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "MDM")

completeChecksMdm('PreProd1ServersMdm', ['localhost', '127.0.0.1'], linuxPropertiesDict, bApplyRequiredChanges)

exit()