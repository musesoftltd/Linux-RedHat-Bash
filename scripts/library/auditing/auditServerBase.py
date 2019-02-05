'''
@author: ...
'''
from java.lang import String

from library.auditing.auditingLibrary import auditObjectAtoms, \
    auditObjectAtomCompleteAnAction


def auditServersBaseAudit(environment, servername, username, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
#     runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'Linux Release', 'cat /etc/*release'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'NLS', 'env | grep NLS'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'ORACLE_HOME', 'env | grep ORACLE_HOME'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'NTP Stats', 'ntpstat'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'ULimit OS Limit', 'ulimit -a | grep \'open files\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'ULimit - Java in-use', 'lsof | grep java | wc -l'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'CPU(s)', 'lscpu | grep \'CPU(s):\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'Total RAM', '/usr/bin/vmstat -SM -s | grep \'total\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'OS Default Java Version', '`which java` -version'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["password"], 'JAVA_HOME Java Version', 'env | grep -ia \'JAVA_HOME=\''))


    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################
