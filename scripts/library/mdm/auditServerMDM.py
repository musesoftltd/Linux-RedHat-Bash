'''
@author: ...
'''
from library.auditing.auditServerBase import auditServersBaseAudit
from library.auditing.auditingLibrary import auditObjectAtom, auditObjectAtoms


def auditServersMdm(environment, servername, username, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
#     runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################

    auditServersBaseAudit(environment, servername, username, propertiesDict, bApplyRequiredChanges)
    
    auditObjectAtoms.append(auditObjectAtom(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], "MDM JGroups TCP", "/opt/install/infamdm/hub/server/resources/jgroups-tcp.xml", "jgroups.mping.mcast_port", "jgroups.mping.mcast_port", False))
    auditObjectAtoms.append(auditObjectAtom(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], "MDM JGroups UDP", "/opt/install/infamdm/hub/server/resources/jgroups-udp.xml", "jgroups.udp.mcast_port", "jgroups.udp.mcast_port", False))
