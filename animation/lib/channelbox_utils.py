######################################
############# IMPORTS ################
######################################
from fstrings import f
import maya.cmds as cmds
import maya_utils as util
import globals as globals


######################################
############# FUNCTIONS ##############
######################################
def set_channel_defaults(nodes=None, keyable=True, userDefine=False, attrs=None):
    ''' dafult: zero out all default keyable channels
        userDefine: zero out all ud keyable channels '''

    if not nodes:
        nodes = cmds.ls(sl=True, fl=True)
    else:
        if type(nodes) is not list:
            nodes = [nodes]

    for node in nodes:

        channelSel = cmds.channelBox('mainChannelBox', q=True, sma=True)
        if channelSel:
            for at in channelSel:
                if cmds.getAttr('%s.%s' % (node, at), keyable=True):
                    util.setDefaultValue(node, at)

            return

        attrs = util.listAttr(node, keyable=keyable, userDefined=userDefine)

        if attrs:
            for at in attrs:

                # do not reset the rotationOrder
                if at == 'rotateOrder':
                    continue

                if cmds.attributeQuery(at, n=node, lc=True):
                    childern = cmds.attributeQuery(at, n=node, lc=True)
                    for childAttr in childern:
                        util.setDefaultValue(node, childAttr)
                else:
                    util.setDefaultValue(node, at)

        # handle ikfk switch shape
        if cmds.objExists(f('{node}.{globals.rig.ikfk_tag_attr}')):
            shapes = cmds.listRelatives(node, s=True)
            for shape in shapes:
                if globals.rig.ikfk_switch_shape in shape:
                    util.setDefaultValue(f('{node}|{shape}'), 'ikBlend')

def delete_channel_keyframes(nodes=None, keyable=True, userDefine=False, attrs=None):
    ''' 
    dafult: deletes channl keyframe if selected
    '''
    if not nodes:
        nodes = cmds.ls(sl=True, fl=True)
    else:
        if type(nodes) is not list:
            nodes = [nodes]

    for node in nodes:

        channelSel = cmds.channelBox('mainChannelBox', q=True, sma=True)
        if channelSel:
            for at in channelSel:
                if cmds.getAttr('%s.%s' % (node, at), keyable=True):
                    cmds.cutKey(node, at=at)

        else:
            attrs = util.listAttr(node, keyable=keyable, userDefined=userDefine)
            if attrs:
                for at in attrs:
                    if cmds.attributeQuery(at, n=node, lc=True):
                        childern = cmds.attributeQuery(at, n=node, lc=True)
                        for childAttr in childern:
                            cmds.cutKey(node, at=childAttr)
                    else:
                        cmds.cutKey(node, at=at)