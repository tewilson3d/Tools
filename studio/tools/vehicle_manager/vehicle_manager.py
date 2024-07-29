######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import maya_utils
import io_utils
import filepath
import rigging.lib.skinning_utils as skin_utils
import rigging.lib.joint_utils as jnt_utils
import meta.metaFactory as metaFactory
#import namespace as ns_util
import material.materialUtilities as matutil


from unreal_tools.utils.globals import ue


######################################
############# DEFINES ################
######################################
SOCKET_JOINT_MES  = 'socket_joint'
SOCKET_JOINT_STR  = 'socket'
RIG_LOC_STR     = 'rig_loc'
PROXY_MESH_STR  = 'proxy_mesh'
LOC_STR         = 'Loc'
MODEL_GRP_STR   = 'Models'
MESH_EXPORT_STR = 'export_meshes'
BIND_POSE_STR   = 'bind_pose'
SKELETON_NS     = 'Skeleton'



######################################
############# CLASSES   ##############
######################################
class Vehicle(object):
    
    export_geo        = []
    jnt_objs          = []
    loc_objs          = []
    mesh_objs         = []
    invalid_mesh_objs = []


######################################
############# FUNCTIONS ##############
######################################
def create_skeleton_locators(vehicle_obj=None, locators=None):
    '''
    Creates the skeleton from selected or existing locators
    '''
    if vehicle_obj is None:
        vehicle_obj = Vehicle()
    
    if locators is None:
        try:
            locators = [cmds.listRelatives(l, f=True, p=True)[0] for l in cmds.ls(type='locator')]
        except:
            cmds.warning('No Locators are in the scene')
    
    for loc in locators:
        # make a loc object
        loc_obj = metaFactory.createLocatorNode(loc)
        vehicle_obj.loc_objs.append(loc_obj)
        
        if not 'Loc_' in loc_obj.shortName:
            loc_obj.rename(f'Loc_{loc_obj.shortName}')
        jnt_obj = metaFactory.createJointNode(loc_obj.shortName.replace('Loc_', ''), create=True)
        
        # add connection to locator and joint
        loc_obj.addConnection(SOCKET_JOINT_MES, jnt_obj, RIG_LOC_STR)
        
        vehicle_obj.jnt_objs.append(jnt_obj)
        
        # make connection to mesh for later skinning
        if loc_obj.children:
            for child in loc_obj.children:
                if child.nodeType == 'transform':
                    jnt_obj.addConnection(MESH_EXPORT_STR,
                                          child,
                                          SOCKET_JOINT_MES,
                                          srcAttrType='messageArray')
    
                    vehicle_obj.export_geo.append(child.name)
    
        # match positions
        maya_utils.matchAlignObjects(loc_obj.name, jnt_obj.name)
    
    # parent 
    
    ## replace parent locator name with joint name #
    #for jnt_obj in vehicle_obj.jnt_objs:
        #if jnt_obj.rig_loc.get:
            #if jnt_obj.rig_loc.get.parent:
                #jnt_obj.setParent(jnt_obj.rig_loc.get.parent.name)

    
    # tag and setup joint reigon and side
    jnt_utils.setJointRegion()
    
    return vehicle_obj

def create_skeleton_meshes(vehicle_obj=None, selected=None, rename=True):
    '''
    Creates the skeleton from selected or existing locators
    '''
    if vehicle_obj is None:
        vehicle_obj = Vehicle()
    
    if selected is None:
        selected = cmds.ls(sl=True, type='transform')
    
    for sel in selected:
        mesh_obj = metaFactory.createMeshExportNode(sel)
        jnt_obj = metaFactory.createJointNode(f'jnt_{mesh_obj.shortName}', 
                                              create=True)
    
        vehicle_obj.jnt_objs.append(jnt_obj)
        vehicle_obj.export_geo.append(mesh_obj.name)
        
        # make connection to mesh for later skinning
        jnt_obj.addConnection(MESH_EXPORT_STR, 
                              mesh_obj, 
                              SOCKET_JOINT_MES,
                              srcAttrType='messageArray')
    
        # be able to export wwith no skeleton in the scene
        mesh_obj.addAttr(SOCKET_JOINT_STR, 
                         value=str(jnt_obj.shortName), 
                         attrType='string')
        mesh_obj.socket.set(jnt_obj.shortName)
        
        # set the rigged attr
        _set_rigged_tag(mesh_obj)

        # match positions
        maya_utils.matchAlignObjects(mesh_obj.name, jnt_obj.name)
    
    return vehicle_obj

def _get_vehicle_obj(vehicle_obj):
    '''
    Populates the vehicle object dict
    '''
    # need to handle mesh or joint
    if cmds.ls(sl=True, an=True):
        if cmds.ls(sl=True, type='joint'):
            vehicle_obj.jnt_objs = metaFactory.getObjectListFromList(cmds.ls(sl=True, type='joint'))
            for jnt_obj in vehicle_obj.jnt_objs:
                if jnt_obj.export_meshes.get:
                    vehicle_obj.mesh_objs.extend(jnt_obj.export_meshes.get)
        else:
            vehicle_obj.mesh_objs = metaFactory.getObjectListFromList(cmds.ls(sl=True))
    else:
        mesh_shapes = cmds.ls(type='mesh')
        if mesh_shapes:
            objs = metaFactory.getObjectListFromList([cmds.listRelatives(s, 
                                                                         p=True, 
                                                                         type='transform')[0] for s in mesh_shapes])
            for obj in objs:
                if obj.socket_joint:
                    if not obj.is_collision:
                        vehicle_obj.mesh_objs.append(obj)
        else:
            return    
    
def set_export_values(vehicle_obj=None, force_eval=False):
    '''
    This sets up the epxort and rig position values for all meshes
    These values are used when exporting and returning all meshes back to the intial 
    modeling position
    '''
    if vehicle_obj is None:
        vehicle_obj = Vehicle()
        _get_vehicle_obj(vehicle_obj)

    # set the mesh pivot position
    for mesh in vehicle_obj.mesh_objs:
        
        if mesh.socket_joint.get:
            
            # ignore if we have already setup
            if not mesh.bind_pose or force_eval:
                position = cmds.pointPosition(f"{mesh.socket_joint.get.name}.rotatePivot", w=True)
                mesh.util.movePivotLocation(position)
                
                # parent the mesh to joint, freese values,
                # unparent and store world matrix values
                org_parent = None
                if mesh.parent:
                    org_parent = mesh.parent.name
                    
                mesh.setParent(mesh.socket_joint.get.name)
                mesh.util.freezeTransform
                mesh.setParent(org_parent if org_parent else None)
                if not mesh.bind_pose:
                    mesh.addAttr(BIND_POSE_STR, 
                                 attrType='string', 
                                 value=mesh.matrix)
                else:
                    mesh.bind_pose.set(mesh.matrix)
    
        else:
            zero_transform_pivots(mesh)
            mesh.addAttr(BIND_POSE_STR, attrType='string')
            mesh.bind_pose.set(mesh.matrix)

    return vehicle_obj
   
def connect_geometry(rename=False, hide_geo=False):
    '''
    Connects the geometry to the selected joitn, this is a stand alone fucntion
    but this should be handled in create_skeleton
    '''
    jnt_obj = None
    mesh_objs = []
    sel = cmds.ls(sl=1, an=True)
    for s in sel:
        obj = metaFactory.getMPyNode(s)
        if obj.mObjType == 'kTransform':
            mesh_objs.append(metaFactory.createMeshExportNode(obj.name))
        elif obj.mObjType == 'kJoint':
            jnt_obj = obj
    
    if mesh_objs and jnt_obj:
        for mesh in mesh_objs:
            jnt_obj.addConnection(MESH_EXPORT_STR, 
                                  mesh, 
                                  SOCKET_JOINT_MES,
                                  srcAttrType='messageArray')
            
            # be able to export wwith no skeleton in the scene
            mesh.addAttr(SOCKET_JOINT_STR, 
                         value=str(jnt_obj.shortName), 
                         attrType='string')
            _set_rigged_tag(mesh)

            # rename fucntion needed
            # need to tag mesh as nanite or static\
            if rename:
                _rename_export_meshes(mesh)
                
            if hide_geo:
                cmds.hide(mesh.name)
 
def  _rename_export_meshes(mesh, is_rigged=True, use_container=True):
    
    #mesh = metaFactory.createTransformNode(mesh.name)
    
    mesh.export_util.rename(is_rigged, use_container)
    
    #if mesh.is_rigged.get is False:
        #if mesh.container_name and use_container:
            #if mesh.is_static.get:
                #mesh.rename(f'{ue.staticmesh}_{mesh.container_name.get}_{mesh.shortName}')      
            #else:
                #mesh.rename(f'{ue.nanite}_{mesh.container_name.get}_{mesh.shortName}')
        #else:
            #if mesh.is_static.get:
                #mesh.rename(f'{ue.staticmesh}_{mesh.shortName}')               
            #else:
                #mesh.rename(f'{ue.nanite}_{mesh.shortName}')
    
    #else:
        #if mesh.container_name and use_container:
            #if mesh.is_static.get:
                #mesh.rename(f'{ue.staticmesh}_{mesh.container_name.get}__{mesh.socket.get}')      
            #else:
                #mesh.rename(f'{ue.nanite}_{mesh.container_name.get}__{mesh.socket.get}')
        #else:
            #if mesh.is_static.get:
                #mesh.rename(f'{ue.staticmesh}_{mesh.shortName}__{mesh.socket.get}')               
            #else:
                #mesh.rename(f'{ue.nanite}_{mesh.shortName}__{mesh.socket.get}')

def reconnect_geometry():
    
    meshes = metaFactory.getObjectListFromSelection()
    if meshes:
        for mesh in meshes:
            try:
                mesh.addConnection('socket_joint', 
                                   metaFactory.createJointNode(mesh.socket.get), 
                                   'export_meshes' ,
                                   srcAttrType='message',
                                   desAttrType='messageArray',)
            except:
                print(f'{mesh.name}')

def set_mesh_names(container_obj=None, use_container=True):
    
    # fix by container
    if container_obj:
        for mesh in container_obj.export_meshes.get:
            try:
                _rename_export_meshes(mesh)
            except:
                pass
    
    # fix by selection
    else:
        meshes = metaFactory.getObjectListFromSelection()
        if meshes:
            for mesh in meshes:
                
                # store base mesh name
                if mesh.base_name:
                    if not mesh.base_name.get:
                        mesh.addAttr('base_name', attrType='string')
                        mesh.base_name.set(mesh.shortName)
                
                try:
                    if mesh.is_rigged.get:
                        mesh.export_util.rename(True, use_container)
                    else:
                        mesh.export_util.rename(False, use_container)
                    #_rename_export_meshes(mesh, use_container=use_container)
                except:
                    pass

def set_base_name():
    
    meshes = metaFactory.getObjectListFromSelection()
    if meshes:
        for mesh in meshes:
            # store base mesh name
            mesh.addAttr('base_name', attrType='string')
            mesh.base_name.set(mesh.shortName)

def load_skeleton():
    
    # find skeleton fbx file
    container_file = filepath.FilePath(cmds.file(sn=True, q=True))
    skel_files = container_file.dir().walk(isFileOnlyIn=True,
                                           doMatchIn=True,
                                           matchModeStrIn="glob",
                                           matchStringsListIn=['*Skeleton.fbx'])
    
    if skel_files:
        for skel_file in skel_files:
            io_utils.reference_file(skel_file, 'Skeleton')
            break
    
def load_container_file():
    pass

def save_container_files(container_objs=None):
    if container_objs is None:
        container_objs = metaFactory.getMetaObjectsByType(metaFactory.CONTAINER_EXPORT)
    
    if container_objs:
        for container in container_objs:
            folder = filepath.FilePath(cmds.file(q=1,sn=1)).dir()
            io_utils.save_file(folder.join(f'{container.manfacture.get}_{containe.container_namer.get}.ma'),True)
    
def parent_geometry(vehicle_obj=None, parent_str_name=False):
    '''
    Parents/Unparents selected geometry
    '''
    # need to rework grabbing the parent
    if parent_str_name:
        model_obj = metaFactory.createTransformNode(parent_str_name)
    
    if vehicle_obj is None:
        vehicle_obj = Vehicle()
        _get_vehicle_obj(vehicle_obj)    
    
    for mesh in vehicle_obj.mesh_objs:
        if parent_str_name:
            mesh.setParent(model_obj.name)
        else:
            mesh.setParent(mesh.socket_joint.get)
    
    return vehicle_obj

def skin_geometrty(vehicle_obj=None):
    '''
    Skins the objects to there socket joints
    '''
    if vehicle_obj is None:
        vehicle_obj = Vehicle()
        _get_vehicle_obj(vehicle_obj) 
    
    cmds.select(cl=True)
    
    for mesh in vehicle_obj.mesh_objs:
        skin_utils.skinObjects(mesh.name, mesh.socket_joint.get.name)
    
def tag_static_meshes(isStatic=True, isPomblend=False):
    meshes = cmds.ls(sl=True, an=True)
    if meshes:
        with metaFactory.disableDefaultInit():
            for mesh in meshes:
                mesh = metaFactory.createMeshExportNode(mesh)
                if isPomblend:
                    mesh.is_static.set(isStatic)
                    mesh.is_pomblend.set(isPomblend)
                else:
                    mesh.is_static.set(isStatic)
                    
                mesh.is_static.setKeyable(False,True)
                mesh.is_pomblend.setKeyable(False,True)

def tag_dfm_meshes():
    meshes = cmds.ls(sl=True, an=True)
    if meshes:
        with metaFactory.disableDefaultInit():
            for mesh in meshes:
                mesh = metaFactory.createMeshExportNode(mesh)
                mesh.is_dfm.set(True)

def _set_rigged_tag(obj):
    ''' main function for setting is_rigged '''
    obj.is_rigged.set(True)
    obj.is_rigged.setKeyable(False,True)   
    
def tag_rigged_meshes(is_rigged=True):
    '''
    Tag and set pivot points
    '''
    selected = cmds.ls(sl=True)
    if selected:
        meshes = [metaFactory.createMeshExportNode(m) for m in selected]
        
        for mesh in meshes:
            if is_rigged:
                _set_rigged_tag(mesh)
    
            else:
                zero_transform_pivots(mesh)
                
                # clean up socket attributes
                if mesh.socket:
                    mesh.socket.delete
                if mesh.socket_joint:
                    mesh.socket_joint.delete
    
def tag_collison_meshes(box=True, custom=False):
    '''
    Tag and rename all collision objects
    '''
    sel = cmds.ls(sl=True)
    for s in sel:
        col = cmds.listRelatives(s, c=True, type='transform', f=True)
        if col:
            for c in col:
                col_obj = metaFactory.createMeshExportNode(c)
                if box:
                    col_obj.rename(f'{ue.boxproxies}_{s}_00')
                elif custom:
                    col_obj.rename(f'{ue.customproxies}_{s}_00')
                col_obj.is_collision.set(True)

def zero_transform_pivots(mesh_obj):
    mesh_obj.util.movePivotLocation([0,0,0])
    mesh_obj.util.freezeTransform
    
def _create_model_group():
    return metaFactory.createTransformNode('Model')

def group_geonmerty(container_obj):
    '''
    Group the geomerty
    '''
    geo_grp = _create_model_group()
    container_obj.export_group_node.get.setParent(geo_grp)

def fix_materials(materials=None):
    if materials is None:
        materials = cmds.ls(sl=1)
    nodes = matutil.getMeshesAndFacesFromMaterials(materials)
    cmds.select(nodes, r=1)
    shading_engine = matutil.getShadingEnginesFromMaterials([materials[0]])
    cmds.sets(nodes, e=True, forceElement=shading_engine[0])
    
    
## Connect by skin cluster
#mesh_objs = []
#invalid_mesh_objs = []

#sel = cmds.ls(sl=True)
#if sel:
    #mesh_objs = [metaFactory.createTransformNode(s) for s in sel]
#else:
    #return cmds.error('No meshes were selected')

#for mesh in mesh_objs:
    #socket_jnts = mesh.skinCluster.influencesWeighted
    #if socket_jnts:
        #if len(socket_jnts) > 1:
            #invalid_mesh_objs.append(mesh.name)
            #continue
        #else:
            #mesh.addConnection('socket_joint', socket_jnts[0], PROXY_MESH_STR, desAttrType='messageArray')
            #mesh.addAttr(MESH_SOCKET_STR, value=str(socket_jnts[0]), attrType='string')
            
            
            
## export socket connections
#sel = mf.getObjectListFromSelection()
#for s in sel:
    #if not s.socket_joint:
        #print(s)
    #else:
        #s.addAttr('socket', value=s.socket_joint.get.basename, attrType='string')
        #s.socket.set(s.socket_joint.get.basename)
        
#sel = mf.getObjectListFromSelection()
#for s in sel:
    #s.socket.set(s.socket.get.replace('L_', 'R_'))

#sel = mf.getObjectListFromSelection()
#for s in sel:  
    #s.addConnection('socket_joint', s.socket.get, 'export_meshes' ,srcAttrType='message',desAttrType='messageArray',)
    
#sel = mf.getObjectListFromSelection()
#for s in sel:
    #cmds.skinCluster(s.socket.get,s.name,skinMethod=0,maximumInfluences=4,normalizeWeights=True,toSelectedBones=True)    
    
    
    #sel = mf.getObjectListFromSelection()
    #for s in sel:
        #jname = s.socket.get
        #jname = jname.split('|')[-1]
        #s.socket.set(jname)
        #s.addConnection('socket_joint',  s.socket.get, 'export_meshes' ,srcAttrType='message',desAttrType='messageArray',)    