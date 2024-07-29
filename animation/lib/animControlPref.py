######################################
############# IMPORTS ################
######################################
import maya.mel as mel
import maya.api.OpenMaya as OpenMaya
import meta.metaFactory as metaFactory

######################################
############# DEFINES ################
######################################
ROTATE = 'setToolTo $gRotate;'
MOVE = 'setToolTo $gMove;'

global manipPrefCallback
manipPrefCallback = None

######################################
############# FUNCTIONS ##############
######################################
def createManipPref(node, pref):
    nodeObj = metaFactory.getMPyNode(node)
    nodeObj.addAttr('manipPref', attrType='string')
    nodeObj.manipPref.set(pref)

def setManipPref(node, pref):
    nodeObj = metaFactory.getMPyNode(node)
    nodeObj.manipPref.set(pref)

def contrlManipPref(*args):
    control = metaFactory.getObjectListFromSelection()
    if control:
        if 'manipPref' in control[0].attributeNames:
            mel.eval(control[0].manipPref.get)

def activatePref_callback():
    """
    Setup the different maya callbacks that the UI need to be refreshed correctly
    """
    global manipPrefCallback
    manipPrefCallback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", contrlManipPref)

def remove_callbacks():
    """
    Remove all callabacks setup by the UI
    """
    global manipPrefCallback
    try:
        if manipPrefCallback:
            OpenMaya.MEventMessage.removeCallback(manipPrefCallback)
    except:
        pass