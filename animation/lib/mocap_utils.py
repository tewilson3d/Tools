import maya.cmds as cmds
import maya.mel as mel

def attach(src, target, mo=False):
    rotate_keyable = cmds.getAttr("%s.rotateX" % target, keyable=1)
    translate_keyable = cmds.getAttr("%s.translateX" % target, keyable=1)

    if not rotate_keyable:
        con = cmds.pointConstraint(src, target, mo=mo)[0]
        return con
    if not translate_keyable:
        con = cmds.orientConstraint(src, target, mo=mo)[0]
        return con

    con = cmds.parentConstraint(src, target, mo=mo)[0]
    return con


def detach(transform):
    con = cmds.listConnections("%s.translateX" % transform, type="constraint", s=1, d=0)
    if con:
        cmds.delete(con)


def delete_keys(transform):
    crvs = cmds.listConnections(transform, s=1, d=0, type="animCurve")
    if crvs:
        cmds.delete(crvs)


def attach_to_mocap(mapping_profile, ns, suffix):
    cons = []
    for key, value in mapping_profile.items():
        src = "%s_%s" % (value, suffix)
        target = "%s:%s" % (ns, key)
        delete_keys(target)
        cons.append(attach(src, target))
    return cons


def detach_from_mocap(mapping_profile, ns):
    for key, value in mapping_profile.items():
        target = "%s:%s" % (ns, key)
        detach(target)

