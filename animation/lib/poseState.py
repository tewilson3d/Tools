######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds

# tools
import rigging.globals as rig_globals
import rigging.lib.build.rigUtil as rigUtil
import animation.tools.snapParentSpace.snapParentSpace as snapParent
import animation.tools.ikFkSwitch.snapIkFk as snapIk


######################################
############# DEFINES ################
######################################
parentSpaceAttr=rig_globals.rig.parentspace
ikfk_blend_attr= rig_globals.rig.ikfk_blend_attr.keys[0]


######################################
############# FUNCTIONS ##############
######################################
def getState(controls=None, namespace=None):
    ''' Creates a dictonary of keyframes and control states '''

    controlState = {}

    if not namespace:
        raise ValueError('Namespace must be given')

    if not controls:
        controls = rigUtil.getControllers(namespace=namespace)
    else:
        if type(controls) != list:
            controls = [controls]

    # iterate through all controls
    if controls:
        for control in controls:
            controlState[control] = {}
            for attr in [parentSpaceAttr, ikfk_blend_attr]:
                if cmds.objExists('{0}.{1}'.format(control, attr)):
                    controlState[control].update({attr : cmds.getAttr(str.join('.', (control, attr)))})

        return controlState

    return None

def __setState(control, attr, value):
    ''' DoIt function switchs the Controller '''

    if attr == parentSpaceAttr:
        snapParent.switch(control, 
                          value=value)

    elif attr == ikfk_blend_attr:
        mode = 'FK'
        if value == 1:
            mode = 'IK'
        snapIk.apply(control, mode=mode)

def setState(controlState={}, animation=None, smartBake=False):
    ''' Restores controls back to the given state provided: 
        stateDict: needs to be given getCurrentSate's result,
        animation: if given restores states for their respected keyframes,
        smartBake: preform smartbake '''

    for (keyItem, keyValue) in controlState.items():
        for (attr, attrValue) in keyValue.items():
            __setState(keyItem, attr, attrValue)

def setDefaultState(controlState={}, psAttr=parentSpaceAttr):
    ''' Sets all ParentSpace to default '''
    for (keyItem, keyValue) in controlState.items():
        for attr, attrValue in keyValue.items():
            if attr == psAttr:
                __setState(keyItem, psAttr, 0)