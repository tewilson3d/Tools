######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import animation.lib.timeSlider as time_slider


######################################
############# FUNCTIONS ##############
######################################
def doCalculateOffset(obj, attribute, animCurve, timeline):
    """ math function """
    if cmds.getAttr(str.join('.',(animCurve, 'output'))) != cmds.getAttr(str.join('.',(obj, attribute))):
        if timeline == 'all':
            keys = cmds.keyframe(animCurve, q=True)
        elif timeline == 'selected':
            keys = time_slider.getSelectedTimeRange()
            
        keyVal = cmds.getAttr(str.join('.',(animCurve, 'output')))
        currentVal = cmds.getAttr(str.join('.',(obj, attribute)))
        offset = currentVal - keyVal
        
        # if scale take keyVal
        if 'scale' in attribute:
            cmds.keyframe(obj, at=attribute, edit=True, o='over', vc=currentVal, t=(keys[0],keys[-1]))
        else:
            cmds.keyframe(obj, at=attribute, edit=True, r=True, o='over', vc=offset, t=(keys[0],keys[-1]))

def doOffset(nodes=None, timeRange='all'):
    '''
    offsets animation curves from current value for selected animLater

    Args:
        nodes (list(str)) : animation controls to offset
        timeRange (str): what timeline to use
            
    Returns:
        None
        
    '''
    if not nodes:
        nodes = cmds.ls(sl=True)
        
    if type(nodes) is not list:
        nodes = [nodes]
        
    for node in nodes:
        # get all keyframes/keyframes from animLayers
        animCurve = []
        animNodes = []
        activeLayer = False
        conType = ['animCurve']
        
        if cmds.animLayer('BaseAnimation', q=1, ex=1):
            activeLayer = cmds.treeView('AnimLayerTabanimLayerEditor',q=True,selectItem=True)[0]
            conType.append('animBlendNodeBase')
        for ct in conType:
            if cmds.listConnections(node, source=True, destination=False, plugs=0, connections=0, scn=True, type=ct):
                animNodes.extend(cmds.listConnections(node, source=True, destination=False, plugs=0, connections=0, scn=True, type=ct))

        for anNode in animNodes:
            if cmds.objectType(anNode, isa='animCurve'):
                animCurve.append(anNode)
            elif cmds.objectType(anNode, isa='animBlendNodeBase'):
                curves = cmds.listConnections(anNode, source=True, scn=True, type='animCurve')
                if activeLayer:
                    if bool([c for c in curves if activeLayer in c]):
                        animCurve.append(c)

        # offset value = current curve value - position,
        # from offset value
        for anCrv in animCurve:
            nodeAttr = cmds.listAttr(node, k=True)
            for attr in nodeAttr:
                inCrv = cmds.listConnections('%s.%s' % (node, attr),
                                             source=True, scn=True, type='animCurve')
                if inCrv and (anCrv in inCrv):
                    doCalculateOffset(node, attr, anCrv, timeRange)