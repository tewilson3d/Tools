######################################
############# IMPORTS ################
######################################
import ast
import maya.cmds as cmds
import maya_utils as util
import namespace as ns_util
from decorators import mayaUndoOn

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
ikblend = globals.rig.ikfk_blend_attr

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
                translate = util.getTranslate(cntrl)
                rotate = util.getRotate(cntrl)
                scale = util.getScale(cntrl)
                poseDict[ns_util.baseName(cntrl)][relativeKey] = {transKey:translate,
                                                                    rotKey:rotate}
                if scale:
                    poseDict[ns_util.baseName(cntrl)][relativeKey].update({scaleKey:scale})        

            # global
            if isWorldControl(cntrl):
                wrldRot = util.getRotate(cntrl, True)
            else:
                wrldRot = None

            if isWorldControl(cntrl):
                wrldTrans = util.getTranslate(cntrl, True)
            else:
                wrldTrans = None            

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

def _setPose(key, val, absoluteTrans=False, absoluteRot=False,
             mirrRotAxis=[1,1,1], mirrPosAxis=[1,1,1], mirrScaleAxis=[1,1,1], 
             oppKey=None, oppVal=None):
    ''' actual function, requires a dictionary key and value '''

    poseType = relativeKey

    if val.__contains__(userDefinedKey):
        for udKey, udVal in val[userDefinedKey].items():
            if cmds.objExists('{0}.{1}'.format(key, udKey)):
                util.setAttr(key, udKey, udVal)

    for relKey, relVal in val[poseType].items():
        if relVal:
            if relKey == rotKey:
                util.setRotate(key, valuesIn=[relVal[0]*mirrRotAxis[0], 
                                              relVal[1]*mirrRotAxis[1], 
                                              relVal[2]*mirrRotAxis[2]], worldSpace=absoluteRot)

            elif relKey == transKey:
                util.setTranslate(key, val=[relVal[0]*mirrPosAxis[0], 
                                            relVal[1]*mirrPosAxis[1], 
                                            relVal[2]*mirrPosAxis[2]], worldSpace=absoluteTrans)

            else:
                util.setScale(key, val=[relVal[0], 
                                        relVal[1], 
                                        relVal[2]])


def mirror(node, nodeOpposite=None, worldCntrl=False, center=False,
           mirrRotAxis=None, mirrPosAxis=None, mirrScaleAxis=None):
    ''' Mirror function '''
    rot = util.getRotate(node, worldCntrl)
    pos = util.getTranslate(node, worldCntrl)
    scale = util.getScale(node)

    #if center:
    if mirrRotAxis and rot:
        util.setRotate(node, 
                       valuesIn=[rot[0]*mirrRotAxis[0], 
                                 rot[1]*mirrRotAxis[1], 
                                 rot[2]*mirrRotAxis[2]], 
                       worldSpace=worldCntrl)
    elif rot:
        util.setRotate(node, valuesIn=rot, worldSpace=worldCntrl)

    if mirrPosAxis and pos:
        util.setTranslate(node, 
                          val=[pos[0]*mirrPosAxis[0], 
                               pos[1]*mirrPosAxis[1],
                               pos[2]*mirrPosAxis[2]], 
                          worldSpace=worldCntrl)
    elif pos:
        util.setTranslate(node, val=pos, worldSpace=worldCntrl)

    if scale:
        if mirrScaleAxis:
            util.setScale(node, 
                          [scale[0]*mirrScaleAxis[0], 
                           scale[1]*mirrScaleAxis[1],
                           scale[2]*mirrScaleAxis[2]])
        else:
            util.setScale(node, scale)


def setPose(controls, poseInfo, absolute=False, setWorldFk=False, ns=None, *args):
    ''' Sets all keys (cntrls) to the either relative or absolute '''
    with mayaUndoOn():
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
                                        _setPose(ns_util.apply_namespace(key, ns), val,
                                                      absoluteTrans=absolute, absoluteRot=absolute)
                                    else:
                                        _setPose(ns_util.apply_namespace(key, ns), val,
                                                      absoluteTrans=False, absoluteRot=False)                                        

                        except Exception(errorObj):
                            return errorObj

                    else:
                        try:
                            if isWorldControl(sel):
                                _setPose(ns_util.apply_namespace(key, ns), val,
                                          absoluteTrans=absolute, absoluteRot=absolute)
                            else:
                                _setPose(ns_util.apply_namespace(key, ns), val,
                                          absoluteTrans=False, absoluteRot=False)     

                        except Exception(errorObj):
                            return errorObj

        return True

def mirrorPose(selectedControls=False, swap=False, ns=None,
               excludeWorldCntrl=True, retainState=True, poseDict=None, *args):
    ''' Mirror Pose '''

    with mayaUndoOn(): 

        # get all of our animation controls
        if selectedControls:
            cntrls = cmds.ls(sl=True)
            
            # pull namespace from control is ns is none
            ns = ns_util.get_namespace(cntrls[0])
        
        else:
            cntrls = rigUtil.getControllers(namespace=ns,
                                           select=False,
                                           exclude=False,
                                           excludeWorldControl=excludeWorldCntrl)
    
        # create a pose from all animation controls
        allCntrls = rigUtil.getControllers(namespace=ns,
                                           select=False,
                                           exclude=False,
                                           excludeWorldControl=excludeWorldCntrl)


        if not poseDict:
            poseDict = getPose(allCntrls, excludeWorld=excludeWorldCntrl)

        for cntrl in cntrls:

            # world control
            worldCntrl = True if cmds.objExists(str.join('.', (cntrl, globals.rig.world_tag[1]))) else False
            worldTrans = True if cmds.objExists(str.join('.', (cntrl, globals.rig.mirror_tag[1]))) else False
            worldRot = True if cmds.objExists(str.join('.', (cntrl, globals.rig.mirror_tag[2]))) else False

            mirrorRot = None
            mirrorPos = None
            
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
            
            # exit out if mirror value is none, should add a bool 'canmirror'
            if mirrorRot == None:
                continue
            
            # all none tagged controls should be skipped until a better solution
            region = rigUtil.getControlTagRegion(cntrl)
            if region == RLEFT:
                cntrlOpp = cntrl.replace(globals.rig.left_affix, 
                                         globals.rig.right_affix)
            elif region == RRIGHT:
                cntrlOpp = cntrl.replace(globals.rig.right_affix,
                                         globals.rig.left_affix)
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
                                            if swap is False:
                                                _setPose(cntrlOpp, 
                                                          pose[pkey],
                                                          #absoluteTrans=worldCntrl,
                                                          #absoluteRot=worldRot, 
                                                          mirrRotAxis=mirrorRot, 
                                                          mirrPosAxis=mirrorPos,
                                                          oppKey=cntrl,
                                                          oppVal=oppval)
                                            else:
                                                _setPose(cntrl, 
                                                          oppval,
                                                          absoluteTrans=worldTrans,
                                                          absoluteRot=worldRot, 
                                                          mirrRotAxis=mirrorRot, 
                                                          mirrPosAxis=mirrorPos,
                                                          oppKey=cntrlOpp,
                                                          oppVal=pose[pkey])