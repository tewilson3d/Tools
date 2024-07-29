######################################
############# IMPORTS ################
######################################
import ast
import maya.cmds as cmds
import maya_utils as rutil
import namespace as ns_util
from decorators import mayaUndoOn
import rigging.lib.build.rigUtil as rigUtil

# Components
import rigging.lib.build.rigUtil as rigUtil
import rigging.globals as globals


######################################
############# DEFINES ################
######################################
# Constents
RLEFT   = 'rigLeft'
RRIGHT  = 'rigRight'
RCENTER = 'rigCenter'

# Character Pose/Anim functions
relativeKey = 'relative'
absoluteKey = 'absolute'
userDefinedKey = 'userDefined'
transKey = 'translate'
rotKey = 'rotate'
scaleKey = 'scale'
worldFKCntrl = 'World_FK'
worldControl = 'worldControl'
worldRootControl = 'worldRootControl'
worldTrans = 'worldTrans'
worldRot = 'worldRot'
parentSpace = globals.rig.parentspace
ikblend = globals.rig.ikfk_blend_attr.keys[0]

######################################
############# FUNCTIONS ##############
######################################

def getPose(controls=None, excludeWorld=False):
    ''' Returns back the given dictonary for the given control '''

    with mayaUndoOn():    
        controlDict = []

        if not type(controls) == list:
            controls = [controls]

        for cntrl in controls:

            poseDict = {}
            poseDict[ns_util.baseName(cntrl)] = {}

            # find keable attrs
            attrs = cmds.listAttr(cntrl, k=True, s=True, sn=True)

            # user definded

            udAttrs = []
            if cmds.objExists('{0}.{1}'.format(cntrl, parentSpace)):
                udAttrs.append(parentSpace) 
            if cmds.objExists('{0}.{1}'.format(cntrl, ikblend)):
                udAttrs.append(ikblend)

            if udAttrs:
                # ignore double3
                udAttrs = [ud for ud in udAttrs if 'double3' != cmds.getAttr(str.join('.', (cntrl, ud)), type=True)]

                poseDict[ns_util.baseName(cntrl)][userDefinedKey] = {}
                poseDict[ns_util.baseName(cntrl)][userDefinedKey] = \
                    dict(zip(udAttrs, 
                             [cmds.getAttr(str.join('.', (cntrl, ud))) for ud in udAttrs if not 'blendParent' in ud])) # set values        

            # relative
            if attrs:
                translate = rutil.util.getTranslate(cntrl)
                rotate = rutil.util.getRotate(cntrl)
                scale = rutil.util.getScale(cntrl)
                poseDict[ns_util.baseName(cntrl)][relativeKey] = {transKey:translate,
                                                                    rotKey:rotate}
                if scale:
                    poseDict[ns_util.baseName(cntrl)][relativeKey] = {scaleKey:scale}            

            # global
            if isWorldControl(cntrl):
                wrldRot = rutil.util.getRotate(cntrl, True)
            else:
                wrldRot = None

            if isWorldControl(cntrl):
                wrldTrans = rutil.util.getTranslate(cntrl, True)
            else:
                wrldTrans = None            

            #wrldScale = rutil.getScale(cntrl)
            if wrldRot and wrldTrans:
                poseDict[ns_util.baseName(cntrl)][absoluteKey] = {rotKey:wrldRot,
                                                                    transKey:wrldTrans}
            else:
                poseDict[ns_util.baseName(cntrl)][absoluteKey] = {}

            controlDict.append(poseDict)

        return controlDict

def isWorldControl(cntrl):
    ''' need to do this better'''
    if cmds.objExists(str.join('.', (cntrl, worldControl))) or \
       cmds.objExists(str.join('.', (cntrl, worldRootControl))) or \
       cmds.objExists(str.join('.', (cntrl, worldTrans))):
        return True
    return False

def __setPose(key, val, absoluteTrans=False, absoluteRot=False,
              mirrRotAxis=[1,1,1], mirrPosAxis=[1,1,1], mirrScaleAxis=[1,1,1], 
              oppKey=None, oppVal=None):
    ''' actual function, requires a dictionary key and value '''

    poseType = absoluteKey if absoluteTrans else relativeKey

    if val.__contains__(userDefinedKey):
        for udKey, udVal in val[userDefinedKey].items():
            if cmds.objExists('{0}.{1}'.format(key, udKey)):
                rutil.util.setAttr('{0}.{1}'.format(key, udKey), udVal)

    for relKey, relVal in val[poseType].items():
        if relVal:
            if relKey == rotKey:
                #if cmds.objExists('{0}.{1}'.format(key, relKey)):
                rutil.util.setRotate(key, valuesIn=[relVal[0]*mirrRotAxis[0], 
                                                       relVal[1]*mirrRotAxis[1], 
                                                       relVal[2]*mirrRotAxis[2]], worldSpace=absoluteRot)

            elif relKey == transKey:
                #if cmds.objExists('{0}.{1}'.format(key, transKey)):
                rutil.util.setTranslate(key, val=[relVal[0]*mirrPosAxis[0], 
                                                     relVal[1]*mirrPosAxis[1], 
                                                     relVal[2]*mirrPosAxis[2]], worldSpace=absoluteTrans)

            else:
                #if cmds.objExists('{0}.{1}'.format(key, udKey)):
                rutil.util.setScale(key, val=[relVal[0], 
                                                 relVal[1], 
                                                 relVal[2]])


def mirror(node, nodeOpposite=None, worldCntrl=False, center=False,
           mirrRotAxis=None, mirrPosAxis=None, mirrScaleAxis=None):
    ''' Mirror function '''
    rot = rutil.util.getRotate(node, worldCntrl)
    pos = rutil.util.getTranslate(node, worldCntrl)
    scale = rutil.util.getScale(node)

    #if center:
    if mirrRotAxis and rot:
        rutil.util.setRotate(node, valuesIn=[rot[0]*mirrRotAxis[0], 
                                                rot[1]*mirrRotAxis[1], 
                                                rot[2]*mirrRotAxis[2]], 
                                      worldSpace=worldCntrl)
    elif rot:
        rutil.util.setRotate(node, valuesIn=rot, worldSpace=worldCntrl)

    if mirrPosAxis and pos:
        rutil.util.setTranslate(node, val=[pos[0]*mirrPosAxis[0], 
                                              pos[1]*mirrPosAxis[1],
                                              pos[2]*mirrPosAxis[2]], 
                                         worldSpace=worldCntrl)
    elif pos:
        rutil.util.setTranslate(node, val=pos, worldSpace=worldCntrl)

    if scale:
        if mirrScaleAxis:
            rutil.util.setScale(node, [scale[0]*mirrScaleAxis[0], 
                                          scale[1]*mirrScaleAxis[1],
                                          scale[2]*mirrScaleAxis[2]])
        else:
            rutil.util.setScale(node, scale)


def setPose(controls, poseInfo, absolute=False, setWorldFk=False, ns=None, *args):
    ''' Sets all keys (cntrls) to the either relative or absolute '''
    with mayaUndoOn():
        poseType = None
        selection = controls

        if not ns:
            raise ValueError('A Namespace needs to ne given')

        for info in poseInfo:
            for key, val in info.items():
                if cmds.objExists(ns_util.apply_namespace(key, ns)):
                    if selection:
                        try:
                            for sel in selection:

                                if ns_util.baseName(sel) == key:
                                    if isWorldControl(sel):
                                        __setPose(ns_util.apply_namespace(key, ns), val,
                                                      absoluteTrans=absolute, absoluteRot=absolute)
                                    else:
                                        __setPose(ns_util.apply_namespace(key, ns), val,
                                                      absoluteTrans=False, absoluteRot=False)                                        

                        except Exception(errorObj):
                            return errorObj

                    else:
                        try:
                            if isWorldControl(sel):
                                __setPose(ns_util.apply_namespace(key, ns), val,
                                          absoluteTrans=absolute, absoluteRot=absolute)
                            else:
                                __setPose(ns_util.apply_namespace(key, ns), val,
                                          absoluteTrans=False, absoluteRot=False)     

                            #__setPose(ns_util.applyNamespace(key, ns), val,
                                        #absoluteTrans=absolute, absoluteRot=absolute)

                        except Exception(errorObj):
                            return errorObj

        return True

def mirrorPose(selectedControls=False, swap=False, ns=None,
               excludeWorldCntrl=True, retainState=True, poseDict=None, *args):
    ''' Mirror Pose '''

    with mayaUndoOn(): 
        # create a pose from all animation controls
        allCntrls = rigUtil.getControllers(namespace=ns,
                                                      select=False,
                                                      exclude=False,
                                                      excludeWorldControl=excludeWorldCntrl)

        # get all of out animation controls
        if selectedControls:
            cntrls = cmds.ls(sl=True)

            if not cntrls and allCntrls:
                cntrls = allCntrls

        else:
            cntrls = allCntrls  

        if not poseDict:
            poseDict = getPose(allCntrls, excludeWorld=excludeWorldCntrl)

        for cntrl in cntrls:

            # world control
            worldCntrl = True if cmds.objExists(str.join('.', (cntrl, globals.rig.world_tag[0]))) else False
            worldTrans = True if cmds.objExists(str.join('.', (cntrl, globals.rig.mirror_tag[0]))) else False
            worldRot = True if cmds.objExists(str.join('.', (cntrl, globals.rig.mirror_tag[1]))) else False

            # find the mirror values
            if not cmds.objExists(str.join('.', (cntrl, 'rigNone'))):
                if cmds.objExists(str.join('.', (cntrl, globals.rig.mirror_attr))):
                    axisValues = cmds.attributeQuery(globals.rig.mirror_attr, 
                                                     node=cntrl, listEnum=True)[0].split(':')
                    mirrorRot = [ast.literal_eval(n) for n in axisValues[0].split(' ')]
                    mirrorPos = [ast.literal_eval(n) for n in axisValues[1].split(' ')]
                    mirrorScale = [1, 1, 1]

                    if mirrorRot[0] == None:
                        mirrorRot = None
                    if mirrorPos[0] == None:
                        mirrorPos = None

            # all none tagged controls should be skipped until a better solution
            region = rigUtil.RigUtil().getControlTagRegion(cntrl)
            if region == RLEFT:
                cntrlOpp = cntrl.replace('L_', 'R_')
            elif region == RRIGHT:
                cntrlOpp = cntrl.replace('R_', 'L_')
            elif region == RCENTER:
                cntrlOpp = cntrl
            else:
                cntrlOpp = None

            if cntrlOpp:   
                if region == RCENTER:
                    mirror(cntrlOpp, mirrRotAxis=mirrorRot, worldCntrl=worldCntrl,
                           mirrPosAxis=mirrorPos, mirrScaleAxis=mirrorScale)

                else:
                    for pose in poseDict:
                        for pkey, pval in pose.items():
                            if pkey == ns_util.baseName(cntrl):
                                for i in range(len(poseDict)):
                                    for oppkey, oppval in poseDict[i].items():
                                        if oppkey == ns_util.baseName(cntrlOpp):
                                            __setPose(cntrlOpp, 
                                                      pose[pkey],
                                                      absoluteTrans=worldTrans,
                                                      absoluteRot=worldRot, 
                                                      mirrRotAxis=mirrorRot, 
                                                      mirrPosAxis=mirrorPos,
                                                      oppKey=cntrl,
                                                      oppVal=oppval)
                                            if swap:
                                                __setPose(cntrl, 
                                                          oppval,
                                                          absoluteTrans=worldTrans,
                                                          absoluteRot=worldRot, 
                                                          mirrRotAxis=mirrorRot, 
                                                          mirrPosAxis=mirrorPos,
                                                          oppKey=cntrlOpp,
                                                          oppVal=pose[pkey])