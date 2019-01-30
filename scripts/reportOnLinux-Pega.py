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

from environmentProperties.PreProd.inventory import serversMdm as preProdServersMdm
from environmentProperties.PreProd.inventory import serversPega as preProdServersPega
from environmentProperties.brt.inventory import serversMdm as brtServersMdm
from environmentProperties.brt.inventory import serversPega as brtServersPega
from environmentProperties.prodSupport.inventory import serversMdm as prodSupportServersMdm
from environmentProperties.prodSupport.inventory import serversPega as prodSupportServersPega
from environmentProperties.rsit01.inventory import serversMdm as rsit01ServersMdm
from environmentProperties.rsit01.inventory import serversPega as rsit01ServersPega
from environmentProperties.rsit02.inventory import serversMdm as rsit02ServersMdm
from environmentProperties.rsit02.inventory import serversPega as rsit02ServersPega
from environmentProperties.rsit03.inventory import serversMdm as rsit03ServersMdm
from environmentProperties.rsit03.inventory import serversPega as rsit03ServersPega
from environmentProperties.rsit04.inventory import serversMdm as rsit04ServersMdm
from environmentProperties.rsit04.inventory import serversPega as rsit04ServersPega
from environmentProperties.rsit05.inventory import serversMdm as rsit05ServersMdm
from environmentProperties.rsit05.inventory import serversPega as rsit05ServersPega
from environmentProperties.rsit06.inventory import serversMdm as rsit06ServersMdm
from environmentProperties.rsit06.inventory import serversPega as rsit06ServersPega
from environmentProperties.rsit07.inventory import serversMdm as rsit07ServersMdm
from environmentProperties.rsit07.inventory import serversPega as rsit07ServersPega
from environmentProperties.rsit08.inventory import serversMdm as rsit08ServersMdm
from environmentProperties.rsit08.inventory import serversPega as rsit08ServersPega
from environmentProperties.rsit09.inventory import serversMdm as rsit09ServersMdm
from environmentProperties.rsit09.inventory import serversPega as rsit09ServersPega
from environmentProperties.rsit10.inventory import serversMdm as rsit10ServersMdm
from environmentProperties.rsit10.inventory import serversPega as rsit10ServersPega
from environmentProperties.rsit11.inventory import serversMdm as rsit11ServersMdm
from environmentProperties.rsit11.inventory import serversPega as rsit11ServersPega
from environmentProperties.rsit12.inventory import serversMdm as rsit12ServersMdm
from environmentProperties.rsit12.inventory import serversPega as rsit12ServersPega
from environmentProperties.rsit13.inventory import serversMdm as rsit13ServersMdm
from environmentProperties.rsit13.inventory import serversPega as rsit13ServersPega
from environmentProperties.rsit14.inventory import serversMdm as rsit14ServersMdm
from environmentProperties.rsit14.inventory import serversPega as rsit14ServersPega
from environmentProperties.rsit15.inventory import serversMdm as rsit15ServersMdm
from environmentProperties.rsit15.inventory import serversPega as rsit15ServersPega
from environmentProperties.training.inventory import serversMdm as trainingServersMdm
from environmentProperties.training.inventory import serversPega as trainingServersPega
from environmentProperties.uat.inventory import serversMdm as uatServersMdm
from environmentProperties.uat.inventory import serversPega as uatServersPega
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
        auditServersPega(env, servername, runtimeProperties["username"], propertiesDict, bApplyRequiredChanges)

        auditingLibrary.auditObjectAtoms.append(auditingLibrary.auditObjectAtomCompleteAnAction(servername, runtimeProperties["username"], runtimeProperties["identityFileFullPath"], runtimeProperties["identityFilePassword"], 'JVM Mem Opts', 'source ~/.bash_profile; grep -ia \'Xmx\' \'/opt/jboss/EAP-6.4.0/bin/standalone.conf\''))
    
        auditReport(env, servername)

bApplyRequiredChanges = False

auditInitAudit("PreProd Servers", "Pega")

completeChecksPega('preProdServersPega', ['localhost', '127.0.0.1'], linuxPropertiesDict, bApplyRequiredChanges)

exit()