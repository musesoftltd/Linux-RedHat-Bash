'''
@author: ...
'''
from library.auditing.auditingLibrary import auditObjectAtoms, \
    auditObjectAtomCompleteAnAction


def auditServersBaseAudit(environment, servername, username, propertiesDict, bApplyRequiredChanges) :
    # merge global propertiesDict into dict - deliberately overwriting local with global dict all values
    runtimeProperties = dict()
#     runtimeProperties.update(globalDictionary)
    runtimeProperties.update(propertiesDict)

    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'RedHat Release', 'cat /etc/redhat-release'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'NLS', 'source ~/.bash_profile 2>/dev/null; env | grep NLS'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'ORACLE_HOME', 'source ~/.bash_profile 2>/dev/null; env | grep ORACLE_HOME'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'Trace Route Farn', 'traceroute farsc3-ntp'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'Trace Route Bas', 'traceroute vulsc3-ntp'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'NTP Stats', 'ntpstat'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'Default Java', '/usr/sbin/lsof | grep java | wc -l'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'ULimit OS Limit', 'ulimit -a | grep \'open files\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'ULimit - Java in-use', '/usr/sbin/lsof | grep java | wc -l'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'CPU(s)', '/usr/bin/lscpu | grep \'CPU(s):\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'Total RAM', '/usr/bin/vmstat -SM -s | grep \'total\''))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'OS Default Java Version', '`which java` -version'))
    auditObjectAtoms.append(auditObjectAtomCompleteAnAction(servername, username, runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'JAVA_HOME Java Version', '/bin/bash set | grep -ia \'JAVA_HOME=\''))


    ##############################################################
    # OO based auditing atoms - automatically reported on...
    ##############################################################
