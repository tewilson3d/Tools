import subprocess 
import helix.perforce as perforce
p4 = perforce.PerforceWrapper()
#import P4 as p4

def getP4Status(filePath):
    """
    fills in a dictionary with the filepath and file status as the value
    """
    allFileStatus = {}        
    #return allFileStatus
    returnedDict = p4.status(filePath)        
    for key, value in returnedDict.items():
        for subKey, subValue in value.items():
            if subKey == "sourceStatus":
                if not subValue:
                    allFileStatus[key] = 'Add'
                    continue
                elif not subValue['up_to_date']:
                    allFileStatus[key] = 'needs sync'
                    continue
                elif subValue['otherCheckOut']:
                    allFileStatus[key] = 'otherCheckOut'
                    continue
                elif subValue['checkedOutByMe']:
                    allFileStatus[key] = 'checkedOutByMe'
                    continue
                else:
                    allFileStatus[key] = 'locked'

    return allFileStatus
    
    
def isConnected():
    return p4.connected
    
def fileStatus(filePath):
    #create a full command to pass in to p4
    #first need to check if the file exists in the database. We will get a 'no such file(s)' return if it does not
    p4String = 'p4 files ' + filePath    
    
    #get the status
    returnStatus = p4Return(p4String)
    if not returnStatus:
        return 'Cannot Connect To P4'
    
    #error if it cannot connect to perforce
    if 'Perforce client error' in returnStatus[0]:
        return 'Cannot Connect To P4'
    
    splitBuf = returnStatus[0].split('-')
    
    #if no such file is returned, we will return Add since the file needs to be added to the database
    if 'no such file' in splitBuf[1]:        
        return 'Add'
    
    #if it is in the database, we need to check on the status.. we do this by building a new string
    p4String = 'p4 opened -a ' + filePath
    returnStatus = p4Return(p4String)
    splitBuf = returnStatus[0].split('-')    
    
    if 'not opened' in splitBuf[1]:        
        return 'Locked'
    
    if 'edit' in splitBuf[1]:
        #we need to check to see who has it checked out.. 
        p4String = 'p4 info -s'
        returnStatus = p4Return(p4String)
        nameSplitBuf = returnStatus[0].split(':')        
        userName = nameSplitBuf[1]
        userName = userName.strip()        
        if userName in splitBuf[1]:            
            return 'Checked Out By You'
        else:
            return 'Checked Out By Someone Else'
    
    return

def isCheckedOut(filePath):
    return

def isAdded(filePath):
    p4String = 'p4 files ' + filePath    
    
    #get the status
    returnStatus = p4Return(p4String)
    if not returnStatus:
        return False
    
    #error if it cannot connect to perforce
    if 'Perforce client error' in returnStatus[0]:
        return False
    
    splitBuf = returnStatus[0].split('-')
    
    #if no such file is returned, we will return Add since the file needs to be added to the database
    if 'no such file' in splitBuf[1]:        
        return True
    
    return False

def isLocked(filePath):
    
    #create a full command to pass in to p4
    #first need to check if the file exists in the database. We will get a 'no such file(s)' return if it does not
    p4String = 'p4 files ' + filePath    
    
    #get the status
    returnStatus = p4Return(p4String)
    if not returnStatus:
        return False
    
    #error if it cannot connect to perforce
    if 'Perforce client error' in returnStatus[0]:
        return False
    
    splitBuf = returnStatus[0].split('-')
    
    #if no such file is returned, we will return Add since the file needs to be added to the database
    if 'no such file' in splitBuf[1]:        
        return False
    
    #if it is in the database, we need to check on the status.. we do this by building a new string
    p4String = 'p4 opened -a ' + filePath
    returnStatus = p4Return(p4String)
    splitBuf = returnStatus[0].split('-')    
    
    if 'not opened' in splitBuf[1]:        
        return True
    
    return False

def checkIn(filePath):
    if isAdded(filePath):
        #first add it
        p4String = 'p4 add ' + filePath
        returnStatus = p4Return(p4String)
    
    p4String = 'p4 submit -d "update" ' + filePath
    returnStatus = p4Return(p4String)    
    
def add(filePath):
    #first add it
    p4String = 'p4 add ' + filePath
    returnStatus = p4Return(p4String)
    #then submit it
    p4String = 'p4 submit ' + filePath
    returnStatus = p4Return(p4String)    
    
    
def checkOut(filePath):
    #need to check the status of the p4 files to make sure they are added in first. if they are not, the checkout function adds them in automatically as text files which breaks
    #anything binary.
    fStatus = fileStatus(filePath)            
    #Local File
    if fStatus != 'Add':    
        p4String = 'p4 edit ' + filePath    
        returnStatus = p4Return(p4String)    

def revert(filePath):   
    p4String = 'p4 revert ' + filePath
    returnStatus = p4Return(p4String)    

def p4Return(fileCmd):
    allLines = []
    p = subprocess.Popen(fileCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)    
    for line in p.stdout.readlines(): 
        #print line
        allLines.append(line),
    retval = p.wait()
    
    return allLines