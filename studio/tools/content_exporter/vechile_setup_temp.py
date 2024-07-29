import meta.metaFactory as metaFactory
import filepath

a = metaFactory.getMPyNode('|ball')
a_inf_joint = a.skinCluster.influencesWeighted[0]
#if len(a_inf_joint) == 1:
a.addConnection('export_joint', metaFactory.createJointNode(a_inf_joint), 'export_geo')

scene_name = filepath.FilePath(cmds.file(q=1, sn=1))
a.rename(f'{scene_name}_{a.export_joint.get.name}')

a.export_joint.get
 
b = metaFactory.getMPyNode('Root|ball')
b_geo = b.skinCluster[0].geometry
       

setAttr "polyRemesh1.maxEdgeLength" 50;
select -r polySurface5 ;
setAttr "polyRemesh2.maxEdgeLength" 50;

sel = cmds.ls(sl=1)
for s in sel:
    cmds.polyRemesh(s, maxEdgeLength=20, useRelativeValues=1, collapseThreshold=80, smoothStrength=0, tessellateBorders=1, interpolationType=2)
