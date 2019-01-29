'''
Created on 11 Oct 2017

@author: ...
'''
import datetime

from linuxProperties import linuxPropertiesDict

from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditInitAudit, auditReport
from library.pega.auditServerPega import auditServersPega

def completeChecksPega(env, serverList, propertiesDict, bApplyRequiredChanges):
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
    #runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    for servername in serverList :
        auditServersPega(env, servername, runtimeProperties["hostUsername"], propertiesDict, bApplyRequiredChanges)
    
        auditReport(env, servername)
# 
# appendToFile("\n", destFileName)
# 
# completeChecksPega('prodServersPega', prodServersPega, 'mxm366UP')

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "Pega")

completeChecksPega('preProdServersPega', ['localhost', '127.0.0.1'], linuxPropertiesDict, bApplyRequiredChanges)

exit()