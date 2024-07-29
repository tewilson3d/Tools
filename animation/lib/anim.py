######################################
############# IMPORTS ################
######################################
import ast
import maya.cmds as cmds
import namespace as ns_util
from decorators import mayaUndoOn
import maya_utils as util

# Componets
import rigging.lib.build.rigUtil as rigUtil
import rigging.globals as globals


######################################
############# DEFINES ################
######################################
RLEFT   = 'rigLeft'
RRIGHT  = 'rigRight'
RCENTER = 'rigCenter'


######################################
############# FUNCTIONS ##############
######################################
def writeAnim(animControls=None):
    ''' Returns a dictonary of animCurve info for given controls '''

    animDict = {} 
    animState = 'anim'
    staticState = 'static'

    if not animControls:
        animControls = cmds.ls(sl=True)
    

    for control in animControls:
   
        # strip namespace
        controlBasename = ns_util.baseName(control)

        animDict[controlBasename] = {animState:{}, staticState:{}}

        #make sure there are keyable attrs on ctrl
        if cmds.listAttr(control, keyable=True, hd=True) is None:
            continue
        
        # determine which are animation values and which are static
        allAttributes = [x.split('.')[-1] for x in cmds.listAttr(control, keyable=True, hd=True)]
        
        if allAttributes:
            for i,attribute in enumerate(allAttributes):
                
                controlAttribute = '%s.%s' % (control, attribute)
                
                animCurveNode = util.listConnections(controlAttribute, 
                                                     source=True, 
                                                     connectionType='animCurve')
                
                # if animcurve exists
                if animCurveNode:

                    animDict[controlBasename][animState][attribute] = {}
                    animCurveNode = animCurveNode[0]
                    
                    # query infinity
                    preInfinity = cmds.getAttr(str.join('.', (animCurveNode, 'preInfinity')))
                    postInfinity = cmds.getAttr(str.join('.', (animCurveNode, 'postInfinity')))
                    weighted = cmds.getAttr(str.join('.', (animCurveNode, 'weightedTangents')))
    
                    animDict[controlBasename][animState][attribute]['preInfinity'] = preInfinity
                    animDict[controlBasename][animState][attribute]['postInfinity'] = postInfinity
                    animDict[controlBasename][animState][attribute]['weighted'] = weighted
    
                    # mirrorAxis
                    #animDict[controlBasename][animState][attribute]['mirrorIndex'] = i
    
                    # query keyframe info
                    keys       = cmds.keyframe(animCurveNode, q=True)
                    values     = cmds.keyframe(animCurveNode, q=True, vc=True)
                    inTang     = cmds.keyTangent(animCurveNode, q=True, itt=True)
                    outTang    = cmds.keyTangent(animCurveNode, q=True, ott=True)                 
                    #tanLock    = cmds.keyTangent(animCurveNode, q=True, lock=True)
                    #weightLock = cmds.keyTangent(animCurveNode, q=True, weightLock=True)
                    #breakDown  = cmds.keyframe(animCurveNode, q=True, breakdown=True)
                    inAngle    = cmds.keyTangent(animCurveNode, q=True, inAngle=True)
                    outAngle   = cmds.keyTangent(animCurveNode, q=True, outAngle=True)
                    #inWeight   = cmds.keyTangent(animCurveNode, q=True, inWeight=True)
                    #outWeight  = cmds.keyTangent(animCurveNode, q=True, outWeight=True)
    
                    animDict[controlBasename][animState][attribute]['keys'] = {}
    
                    # breakdown section needs to be expanded on,
                    # now simpley return true or false
                    #bd = 0 if breakDown == None else 1
    
                    animDict[controlBasename][animState][attribute]['keys']['keyTime'] = keys
                    animDict[controlBasename][animState][attribute]['keys']['keyValue'] = values
                    animDict[controlBasename][animState][attribute]['keys']['inTangent'] = inTang
                    animDict[controlBasename][animState][attribute]['keys']['outTangent'] = outTang
                    #animDict[controlBasename][animState][attribute]['keys']['tangentLock'] = tanLock
                    #animDict[controlBasename][animState][attribute]['keys']['weightLock'] = weightLock		
                    #animDict[controlBasename][animState][attribute]['keys']['breakDown'] = [bd]
                    animDict[controlBasename][animState][attribute]['keys']['inAngle'] = inAngle
                    #animDict[controlBasename][animState][attribute]['keys']['inWeight'] = inWeight
                    animDict[controlBasename][animState][attribute]['keys']['outAngle'] = outAngle
                    #animDict[controlBasename][animState][attribute]['keys']['outWeight'] = outWeight
        
                # store all static values
                else:
                    animDict[controlBasename][staticState][attribute] = cmds.getAttr(controlAttribute)

    return animDict


def __applyAnim(node, attribute, keyDict={}, mirrorValue=1, timeOffset=0, namespace=None):
    ''' Main function '''
    #attributeNode = '%s_%s' % (node, attribute)
    attributeName = '%s.%s' % (node, attribute)

    # iterate through based on how many keys there are
    for i in range(len(keyDict['keys']['keyTime'])):

        time = keyDict['keys']['keyTime'][i] + timeOffset
        value = keyDict['keys']['keyValue'][i] * mirrorValue # if mirror
        intang = keyDict['keys']['inTangent'][i]
        outtang = keyDict['keys']['outTangent'][i]
        #tlock = keyDict['keys']['tangentLock'][i]
        #wlock = keyDict['keys']['weightLock'][i]
        #breakdown = keyDict['keys']['breakDown'][0]
        inangle = keyDict['keys']['inAngle'][i]
        outangle = keyDict['keys']['outAngle'][i]
        #inweight = keyDict['keys']['inWeight'][i]
        #outweight = keyDict['keys']['outWeight'][i]

        tlock     = True
        wlock     = True
        inweight  = 1.0
        outweight = 1.0
        breakdown = 0
        
        cmds.setKeyframe(attributeName, time=time, v=value, bd=breakdown)
        cmds.keyTangent(attributeName, lock=tlock, time=(time, time))
        # added the '' option, so now it's "['fixed', '']" as we're getting empty curve type values
        # for some reason. Need to look into why this is happening and fix. This is a bandaid. 
        if intang not in ['fixed', ''] and outtang not in ['fixed', '']:
            cmds.keyTangent(attributeName, edit=True, time=(time,time), absolute=True,
                            inTangentType=intang, outTangentType=outtang)

        if intang not in ['fixed', ''] and outtang not in ['fixed', '']:
            cmds.keyTangent(attributeName, edit=True, time=(time,time), absolute=True, 
                            inAngle=inangle, inWeight=inweight,
                            inTangentType=intang, outTangentType=outtang)

        if intang not in ['fixed', ''] and outtang not in ['fixed', '']:
            cmds.keyTangent(attributeName, edit=True, time=(time,time), absolute=True, 
                            outAngle=outangle, inWeight=inweight,
                            inTangentType=intang, outTangentType=outtang)

        if intang not in ['fixed', ''] and outtang not in ['fixed', '']:
            cmds.keyTangent(attributeName, edit=True, time=(time,time), absolute=True, 
                            inAngle=inangle, outAngle=outangle, 
                            inWeight=inweight, outWeight=outweight,
                            inTangentType=intang, outTangentType=outtang)

        #cmds.setAttr(str.join('.', (attributeName, 'preInfinity')), keyDict['preInfinity'])
        #cmds.setAttr(str.join('.', (attributeName, 'postInfinity')), keyDict['postInfinity'])


def readAnim(controls, animDict={}, namespace=None, timeOffset=0, applyStatic=True, preserveAnimation=True):
    ''' Import animation '''

    if not namespace:
        raise ValueError('A Namespace needs to be given')
        
    # set the namespace to character active namespace this is to handle
    # an apparent bug with 2014 not appling the characters namespace to 
    # animNodes.
    currentNamespace = ns_util.current()
    ns_util.set_namespace(namespace)

    with mayaUndoOn():
        for node in controls:
            
            # get the object animation data
            attributeNames = animDict[ns_util.baseName(node)]

            for attribute,keyInfo in attributeNames['anim'].items():
                # cut anycurrent keyframes; possible option
                if not preserveAnimation:
                    cmds.cutKey(node, 
                                time=(":",), 
                                attribute=util.split('_')[-1], 
                                option='keys')
                
                # create all keys
                if cmds.objExists('{0}.{1}'.format(node, attribute)):
                    __applyAnim(node, 
                                attribute, 
                                keyInfo, 
                                namespace=namespace,
                                timeOffset=timeOffset)
        
            if applyStatic:
                for attribute,value in attributeNames['static'].items():
                    # check type of attr to avoid errors on string attrs
                    try:
                        attrType = cmds.getAttr('{0}.{1}'.format(node, attribute),type=True)
                        # for some reason hand component curl and spread attributes are breaking this tool - needs to be looked into. 
                        if attribute not in [u'curl', u'spread'] and attrType != 'string':
                            cmds.setAttr('{0}.{1}'.format(node, attribute), value)
                    except:
                        pass
                        
        ns_util.set_namespace(currentNamespace)


def mirrorAnim(animDict=None, cntrls=None, namespace=':', offset=None):
    ''' Mirror animation, default namespace given if not provided '''

    with mayaUndoOn():
        # Set the namespace so that all animNode type will be properly
        # named for appling animation
        ns_util.set_namespace(namespace)
        
        # get all of out animation controls
        cntrls = cmds.ls(sl=True)
        if not cntrls:
            cntrls = rigUtil.getControllers(namespace=namespace, exclude=False)
    
        # save the animation
        if not animDict:
            animDict = writeAnim(cntrls)
    
        # iterate through all given controls
        for cntrl in cntrls:
            node = cntrl
    
            # determine how to mirror based on regioinTag
            region = rigUtil.getControlTagRegion(node)
            if region == RLEFT:
                nodeOpp = node.replace('L_', 'R_')
            elif region == RRIGHT:
                nodeOpp = node.replace('R_', 'L_')
            elif region == RCENTER:
                nodeOpp = node
            else:
                nodeOpp = None
    
            if nodeOpp and cmds.objExists(nodeOpp):
                for attribute,keyInfo in animDict[ns_util.baseName(cntrl)]['anim'].items():
                # build mirror list
                
                    # cuts keys
                    cmds.cutKey(nodeOpp, time=(":",), attribute=attribute, option='keys')  
                    
                    if cmds.objExists('{0}.{1}'.format(node, globals.rig.mirror_attr)):
                    #if cmds.attriobbuteQuery(rglobals.ATTR_MIRROR_AXIS_STR, n=node, exists=True):
                        axisValues = cmds.attributeQuery(globals.rig.mirror_attr, 
                                                         node=node, 
                                                         listEnum=True)[0].split(':')
                        mirrorRot = [ast.literal_eval(n) for n in axisValues[0].split(' ')]
                        mirrorPos = [ast.literal_eval(n) for n in axisValues[1].split(' ')]
                        
                        if mirrorRot[0] != None:
                
                            attributeIndex = {'translateX':mirrorPos[0],
                                              'translateY':mirrorPos[1],
                                              'translateZ':mirrorPos[2],
                                              'rotateX':mirrorRot[0],
                                              'rotateY':mirrorRot[1],
                                              'rotateZ':mirrorRot[2],
                                              'scaleX':1,'scaleY':1,'scaleZ':1,}
                            
                            # apply the animation
                            if attribute in attributeIndex:
                                __applyAnim(nodeOpp, 
                                            attribute, 
                                            keyInfo, 
                                            mirrorValue=attributeIndex[attribute],
                                            timeOffset=offset)
    
                    else:
                        __applyAnim(nodeOpp, 
                                    attribute, 
                                    keyInfo,
                                    timeOffset=offset)
                        
        ns_util.set_namespace()