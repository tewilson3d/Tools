#
#

######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import maya_utils as util

from 


animCurveType = ['animCurve', 'animCurveUT', 'animCurveUU', 
                 'animCurveUA', 'animCurveTT', 'animCurveTU', 
                 'animCurveUL', 'animCurveTA', 'animCurveTL']

animLayerBlendNodes = ['animBlendNodeAdditiveScale',
                       'animBlendNodeAdditiveDL',
                       'animBlendNodeAdditiveRotation']


class Keyframe(object):
        
    @staticmethod
    def getKeyframes(nodes):
        ''' 
            @param nodes, a list of controls
            @returns keyFrames, a dictonary of keyframes times and there values
        '''
        keyFrames = []
        curveNodes = []
        if type(nodes) != list:
            nodes = [nodes]
            
        for node in nodes:
            curveNodes.extend(Keyframe.getAnimCurvesNodes(node))
        
        for node in curveNodes:
            keyFrames.extend(cmds.keyframe(node, q=True))
        
        return sorted(list(set(keyFrames)))
    
    @staticmethod
    def getAnimCurvesNodes(node, activeLayer=False):
        ''' Returns all animCurves '''
        animCurves = []
        tempConnType= util.listConnections(node, 
                                              source=True, 
                                              allConnections=True)
        
        for conn in tempConnType:
            for curveType in animCurveType:
                if cmds.objectType(conn, i=curveType):
                    animCurves.append(conn)
        
        return animCurves
    
    @staticmethod
    def getAnimLayerBlendNodes(node, activeLayer=False):
        ''' Returns all animation layer blend nodes '''
        blendNodes = []
        tempConnType = util.listConnections(node, 
                                               source=True, 
                                               allConnections=True)
        
        for conn in tempConnType:
            for blendNode in animLayerBlendNodes:
                if cmds.objectType(conn, i=blendNode):
                    blendNodes.append(conn)
                    
        return blendNodes
    
    @staticmethod
    def keyframeAmplitudeAdjust(value, pivot):
        '''
        Adjust amplitude of animation curve keyframes based on previous or following keyframe value.
        If a keyframe does not exist on the current frame, make one.
    
        Args:
            value (float) - amount to scale keyframe values by
            pivot (string) - 'previous', scale towards previous keyframe
                           - 'following', scale towards following frame
    
        '''
                
        anims = cmds.keyframe(q=True, name=True) 
        
        if not anims:
            cmds.warning('No keyframes on selected nodes.')
            return
        
        hasSelection = bool(cmds.keyframe(q=True, sl=True, vc=True))
        targetFrame = cmds.currentTime(q=True)
    
        for anim in anims:
            allVals = cmds.keyframe(anim, q=True, vc=True)
    
            # Determine which keyframes to modify
            if hasSelection:
                values = cmds.keyframe(anim, q=True, sl=True, vc=True)
                selIndices = cmds.keyframe(anim, q=True, sl=True, iv=True)
                selTimes = cmds.keyframe(anim, q=True, sl=True, tc=True)
                
            else:
                selTimes = [targetFrame]
    
                # Insert keyframe if it doesn't exist
                if targetFrame not in cmds.keyframe(anim, q=True, tc=True):
                    cmds.setKeyframe(anim, insert=True, t=targetFrame)
    
                index = cmds.keyframe(anim, q=True, tc=True).index(targetFrame)
                selIndices = [index]
                values = [cmds.keyframe(anim, q=True, vc=True)[index]]
       
            # Scale towards previous or following keyframe
            if pivot == 'previous':
                if selIndices[0] > 0:
                    mid = allVals[selIndices[0]-1]
                else:
                    mid = allVals[0]
    
            elif pivot == 'following':
                if len(allVals) - 1 == selIndices[-1]:
                    mid = allVals[-1]
                else:
                    mid = allVals[selIndices[-1]+1]
            else:
                pass
            
            # Scale keyframe values
            cmds.scaleKey(anim, vp=mid, vs=value, iub=True, t=(selTimes[0], selTimes[-1]))    