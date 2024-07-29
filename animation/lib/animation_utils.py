######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import rigging.lib.ncurve_utils as curve


######################################
############# CLASSES ################
######################################
def pathAnimation(node, 
                  name=None, 
                  pathCurve=None):
    '''
        @param node, object to be attached
        @param pathCurve, The pathCurve to be attached to
    '''
    # this is to take in count meters unit/ should query
    # this is needed because the motionPath node must be feed
    # a value in centimeters
    divideBy = 100 if cmds.currentUnit(q=True, l=True) == 'm' else 1
    uvParam = (curve.closestPointOnCurve(node, pathCurve) / divideBy)
        
    motionPath = cmds.pathAnimation(node, 
                                    name='%s_%s' % (node, 'MotionPathNode'), 
                                    stu=0, 
                                    etu=1, 
                                    c=pathCurve)
    
    cmds.delete(cmds.listConnections(motionPath, type='animCurveTL')[0])
    cmds.setAttr(motionPath + '.uValue', uvParam)
    
def hideControlCurves():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, e=True, lc=False, nc=False, ha=False)
    
def showControlCurves():
    panel = cmds.getPanel(wf=True)
    cmds.modelEditor(panel, e=True, lc=True, nc=True, ha=True)    