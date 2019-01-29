'''
@author: ...
'''
from library.auditing.auditServerBase import auditServersBaseAudit


def auditServersPega(environment, servername, username, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
#     runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################

    auditServersBaseAudit(environment, servername, username, propertiesDict, bApplyRequiredChanges)
    