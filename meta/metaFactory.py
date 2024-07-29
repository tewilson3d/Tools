######################################
############# IMPORTS ################
######################################
import os
import sys
import inspect
import contextlib

import maya.cmds as cmds

import filepath
import maya_utils as util

# MetaObject Types
import meta.globals as meta_globals
import meta.classes.mpy_dgnode as mpy_dgnode
import meta.classes.mpy_object as mpy_object
import modeling.metaclasses.mesh as mesh
import general.metaclasses.utility as utility
import rigging.metaclasses.rig as rig
import rigging.metaclasses.joint as joint
import rigging.metaclasses.locator as locator
import rigging.metaclasses.skeleton as skeleton
import rigging.metaclasses.skinnode as skinNode
import rigging.metaclasses.skincluster as skinCluster
import rigging.metaclasses.control as rig_control
import rigging.metaclasses.network as network
import studio.tools.content_exporter.metaclasses.mpy_modelexport_object as modelExport


######################################
############# DEFINES ################
######################################
# MayaObject class name and module
MOBJECT_NAME   = 'MayaObject'
MOBJECT_MODULE = 'meta.classes.mpy_object'
MOBJECT_PATH   = filepath.ToolsPath().join(['meta',
                                            'classes',
                                            'mpy_object.py'])

# MetaClass project paths
CLASS_OBJECT_LIST  = []
CORE_TOOLS_PATH    = filepath.ToolsPath()


######################################
#############   TYPES   ##############
######################################
# Core MeteObject Types
MAYAOBJECT        = 'MPyDagNode'
MAYAMETAOBJECT    = 'MPyDgNode'
DGNODE            = 'MPyDgNode'
MESH              = 'Mesh'
TRANSFORM         = 'transform'
JOINT             = 'Joint'
SKELETON          = 'Skeleton'
SKINNODE          = 'SkinNode'
LOCATOR           = 'Locator'
SKINCLUSTER       = 'SkinCluster'

# Common MetaObject Children Type
RIG             = 'Rig'
RIG_EXPORT      = 'RigExportObject'
ANIM_EXPORT     = 'AnimExportObject'
MODEL_EXPORT    = 'ModelExportObject'
CONTAINER_EXPORT  = 'ContainerObject'
CONTAINER_MESH_EXPORT  = 'ContainerMeshObject'


# Rig Components
RIG_COMPONENT   = 'RigComponent'
RIG_SELECTION   = 'Network'

# Rig MetaObject Types
RIG_CONTROL  = 'Control'

# Export Type
MODEL_ASSET = 'ModelAsset'

######################################
############# DECORATORS #############
######################################
@contextlib.contextmanager
def disableDefaultInit():
    '''
    Decorator for disbaling the initialization of an object default attributes
    This is turned off primarly to save initialization time for object creation when
    the object is not going to be imedediatly removed, will save time on any large list
    '''
    mpy_object.INITIALIZE_DEFAULT_ATTRS = False

    try:
        yield
    finally:
        mpy_object.INITIALIZE_DEFAULT_ATTRS = True

def createMetaNodeSelectionSet():
    '''
    Helper function to group all metanodes in the scene in selection set
    Args:
        None
    Sets:
        None
    '''
    badNodes = []
    goodNodes = cmds.ls(type=meta_globals.meta.node_type)
    
    if goodNodes:

        # Create Parent Set
        parentSetGrp = 'MetaNodeTypes'
        if not cmds.objExists(parentSetGrp):
            cmds.sets(n=parentSetGrp)

        for node in goodNodes:
            
            cmds.select(clear=True)
            
            try:
                metaObj = getMPyNode(node)
                objType = metaObj.MetaClassName.get
                objSetName = objType + '_MPyObjects'
                if not cmds.objExists(objSetName):
                    metaset = cmds.sets(n=objSetName)
                    cmds.sets(metaset, include=parentSetGrp)

                cmds.sets(node, include=objSetName)
            except:
                badNodes.append(node)

        for node in badNodes:
            if not cmds.objExists('CorruptMetaNodes'):
                metaset = cmds.sets(n='CorruptMetaNodes')
                cmds.sets(metaset, include=parentSetGrp)
            cmds.sets(node, include='CorruptMetaNodes')

######################################
############# FUNCTIONS ##############
######################################
def initalizeAllMetaClasses():
    '''
    Base function for loading all metaObjectClass types from classObjectPath, This function 
    walks through all folders and looks for folders specificly named 'metaclasses' and will
    attempt to impor all metaClass objects form existing folders.

    Args:
        None

    Returns:
        None:
    '''
    metaclassFolderPathList = []
    metaclassImportStrList  = []

    for metaObjectImportPath in [CORE_TOOLS_PATH]:
        for folder in filepath.FilePath(metaObjectImportPath).walk(isRecursiveIn=True,
                                                                   isDirOnlyIn=True,
                                                                   doMatchIn=True,
                                                                   matchStringsListIn=['*metaclasses']):

            if 'Docs' not in folder:
                metaclassFolderPathList.append(folder)

                # Remove the art folder
                metaclassImportObj = filepath.FilePath(folder.replace(filepath.FilePath(os.environ['TOOLS_PATH']), ''))

                # Removing the th first period
                metaclassImportObj = filepath.FilePath(str.join('\\', [x for x in metaclassImportObj.stringSplit('\\')[1:]]))

                # Convert to import path
                metaclassImportStrList.append(metaclassImportObj.convertToPythonImport())            

    del CLASS_OBJECT_LIST[:]
    for i,folderPath in enumerate(metaclassFolderPathList):
        classes = folderPath.walk(isRecursiveIn=False, 
                                  isFileOnlyIn=True,
                                  doMatchIn=True,
                                  doIgnoreMatchIn=True,
                                  matchStringsListIn=["*.py"],
                                  ignoreMatchModeStrIn='glob',
                                  ignoreMatchStringsListIn=['*__init__.py'])

        for c in classes:

            moduleName = c.baseName().stringSplit(".")[0]
            module = '{0}{1}'.format(metaclassImportStrList[i], filepath.FilePath(c.replace(folderPath, '')).convertToPythonImport())
            mod = __import__(module, globals(), locals(), ['object'], 0)
            if mod not in CLASS_OBJECT_LIST:
                CLASS_OBJECT_LIST.append(mod)

def getAllMetaClasses(parentMetaClass=None):
    '''
    ?????
    '''
    metaClassSet = set()
    for mod in CLASS_OBJECT_LIST:
        for (_, value) in inspect.getmembers(mod, inspect.isclass):
            if not issubclass(value, mpy_object.MPyDgNode):
                continue
            if parentMetaClass:
                parentClassList = inspect.getmro(value)
                for parentClass in parentClassList:
                    if parentClass.__name__ == parentMetaClass:
                        metaClassSet.add(value)
                        break
            else:
                metaClassSet.add(value)
    return metaClassSet

def _getInstance(instanceType):
    """
    Return a MetaData Class Type

    Args:
        instanceType (str): name of metaObject type

    Returns:
        MetaDataType (obj): The instance of that metaObject type
    """
    for mod in CLASS_OBJECT_LIST:
        for name, obj in inspect.getmembers(mod):
            if name == instanceType:
                return obj('temp_meta_object')

def getObjectListFromSelection(ignoreStoredType=False):
    '''
    Get object list from selected objects

    Args:
        None

    Returns:
        MetaObjList ([MayaObject])
    '''
    selObjList = cmds.ls(sl=True, l=True, an=True)

    if selObjList:
        return [getMPyNode(obj, ignoreStoredType=ignoreStoredType) for obj in selObjList]

def getObjectListFromList(selObjList=None):
    '''
    Return the list of metaObjects list

    Args:
        selObjList (list (st)): list of objects string names
    Returns:
        MetaObjectList(MayaObject): metaObject type
    '''
    if selObjList is None:
        selObjList = cmds.ls(sl=True, l=True)
    if selObjList:
        return [getMPyNode(obj) for obj in selObjList]

def getMPyNodeFromType(mpyNode, metaClassModule, metaClassName):
    '''
    Create a node from given type
    '''
    metaClassName = util.getAttr(mpyNode, meta_globals.meta.mclass_name)
    metaClassModule = util.getAttr(mpyNode, meta_globals.meta.mclass_module)
    
    moduleObj = sys.modules[metaClassModule]
    metaClassObj = getattr(moduleObj, metaClassName)
    return metaClassObj(mpyNode + '_converted')

def getMPyNode(mayaNodeStrName, ignoreStoredType=False):
    '''
    Get the metaclass instance from maya node.

    Args:
        node (str): maya node string name

    Return: 
        subclass of (:py:class:MetaObject)
    '''
    if ignoreStoredType is False:

        # if the inital type fails try again
        try:
            if cmds.objExists('{0}.{1}'.format(mayaNodeStrName, meta_globals.meta.mclass_name)):
                metaClassName = util.getAttr(mayaNodeStrName, meta_globals.meta.mclass_name)
                metaClassModule = util.getAttr(mayaNodeStrName, meta_globals.meta.mclass_module)

                if not metaClassModule in sys.modules:
                    return _getObjectFromType(mayaNodeStrName)

                moduleObj = sys.modules[metaClassModule]
                metaClassObj = getattr(moduleObj, metaClassName)
                return metaClassObj(mayaNodeStrName)
        except:
            getMPyNode(mayaNodeStrName, True)

    return _getObjectFromType(mayaNodeStrName)

def _getObjectFromType(mayaNodeStrName):
    ''' 
    Private function to help getMPyNode,
    this will help address all future refactors and
    missing sys modules

    Args:
        mayaNodeStrName (str): str name of the object
    Returns:
        objectType (object):
    '''
    # Return skinSaveNode
    if cmds.objectType(mayaNodeStrName, i=meta_globals.meta.skinnode_type):
        return skinNode.SkinNode(mayaNodeStrName)
    
    # create an obejct
    with disableDefaultInit():
        nodeObj = mpy_dgnode.MPyDgNode(mayaNodeStrName)

    # Return SkinCluster
    if nodeObj.mObjType == 'kSkinClusterFilter':
        return skinCluster.SkinCluster(nodeObj.name)
    
    # Return a JointObject
    if nodeObj.mObjType == 'kJoint':
        return joint.Joint(nodeObj.name)

    # Return Transform
    if nodeObj.mObjType == 'kTransform':
        if cmds.listRelatives(nodeObj.name, s=True, c=True, f=True):
            if cmds.objectType(cmds.listRelatives(nodeObj.name, s=True, c=True, f=True)[0], i='locator'):
                return locator.Locator(nodeObj.name)
        
        return mesh.Transform(nodeObj.name) 
    
    # Return a generic object
    return mpy_object.MPyObject(nodeObj.name, 
                                cmds.objectType(nodeObj.name))

def getMetaObjectsByType(metaClassTypeStr, isObjectRoot=False):
    '''
    List all the metaNodes that are instantiated from a certain mType

    Args:
        metaClassType (str): mtype to match, use defines from the top,
        or pass in a the full class name.

    Returns:
        ([MetaClass]) : a list of the given MetaClass
    '''
    metaNodes = []
    metaClassObjectList = []
    metaClassObjects = cmds.ls(type=[meta_globals.meta.node_type, 
                                     meta_globals.meta.skinnode_type])

    # Return object from type
    if isObjectRoot is False:
        
        for node in metaClassObjects:
            attrToCheck = f'{node}.{meta_globals.meta.mclass_name}'
            if not cmds.objExists(attrToCheck):
                continue
            if cmds.getAttr(attrToCheck) == '"' + metaClassTypeStr + '"':
                metaNodes.append(node)
    
        return [getMPyNode(m) for m in metaNodes]  
    
    if metaClassObjects:
    
        # create our temp object to comapre against
        tempMetaObj = _getInstance(metaClassTypeStr)
    
        for mcObject in metaClassObjects:
            # create object from metaClassObjectList
            mcObjectClass = getMPyNode(mcObject)
    
            if mcObjectClass:
                if issubclass(mcObjectClass.__class__, tempMetaObj.__class__):
                    metaClassObjectList.append(mcObjectClass)
    
        # delete the tempMetaObj
        cmds.delete(tempMetaObj.name)
    
        return metaClassObjectList

def getMPyDgNode(objectInstanceStrIn):
    """
    Create a `mpy_object.MPyDgNode` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node

    Returns:
        (obj): `mpy_object.MPyDgNode` Instance of `objectInstanceStrIn`
    """
    return mpy_dgnode.MPyDgNode(objectInstanceStrIn)

def getSkeletonObject(objectInstanceStrIn):
    '''
    Returns a skeleton object
    Args:
        objectINstanceStrIn (str): root joint string name
    Returns:
        Skeleton(object)
    '''
    return skeleton.Skeleton(objectInstanceStrIn)

def createSkinNode(objectInstanceStrIn):
    '''
    Return a SkinNode object from node
    '''
    return skinNode.SkinNode(objectInstanceStrIn)

def createMetaNode(objectInstanceStrIn='temp_meta_obj'):
    """
    Create a `mpy_object.MayaObject` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node, 'temp' if nothing is passed

    Returns:
        (obj): `mpy_object.MayaObject` Instance of `objectInstanceStrIn`
    """
    return mpy_object.MPyDgNode(objectInstanceStrIn, meta_globals.meta.node_type)

def createTransformNode(objectInstanceStrIn='temp_transform_obj', nodeTypeStrIn='transform'):
    """
    Create a `mpy_object.MayaObject` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node, 'temp' if nothing is passed

    Returns:
        (obj): `mpy_object.MayaObject` Instance of `objectInstanceStrIn`
    """
    return mesh.Transform(objectInstanceStrIn, nodeType=nodeTypeStrIn)

def createJointNode(objectInstanceStrIn='temp_joint_obj', create=False):
    """
    Create a `mpy_object.MayaObject` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node, 'temp' if nothing is passed

    Returns:
        (obj): `mpy_object.MayaObject` Instance of `objectInstanceStrIn`
    """
    return joint.Joint(objectInstanceStrIn, create=create)

def createMeshExportNode(objectInstanceStrIn='temp_joint_obj'):
    """
    Create a `mpy_object.MayaObject` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node, 'temp' if nothing is passed

    Returns:
        (obj): `mpy_object.MayaObject` Instance of `objectInstanceStrIn`
    """
    return modelExport.ContainterMeshObject(objectInstanceStrIn)

def createLocatorNode(objectInstanceStrIn='temp_transform_obj'):
    """
    Create a `mpy_object.MayaObject` instance from `objectInstanceStrIn`

    Args:
        objectInstanceStrIn (str): Full Path of node, 'temp' if nothing is passed

    Returns:
        (obj): `mpy_object.MayaObject` Instance of `objectInstanceStrIn`
    """
    return locator.Locator(objectInstanceStrIn)

def createNetworkNode(objectInstanceStrIn):
    '''
    Returns a rig control object
    Args:
        objectINstanceStrIn (str): root joint string name
    Returns:
        RigComponent(object)
    '''
    return network.Network(objectInstanceStrIn)

def createRigControlNode(objectInstanceStrIn):
    '''
    Returns a rig control object
    Args:
        objectINstanceStrIn (str): root joint string name
    Returns:
        RigComponent(object)
    '''
    return rig_control.Control(objectInstanceStrIn)

def createUtilityNode(objectInstanceStrIn, nodeTypeStrIn):
    '''
    Returns a utility object node
    Args:
        objectINstanceStrIn (str): root joint string name
        nodeTypeStrIn (str): node type
    Returns:
        RigComponent(object)
    '''
    return utility.Utility(objectInstanceStrIn, nodeType=nodeTypeStrIn)

def createRigNode(objectInstanceStrIn=None):
    '''
    Returns a rig control object
    Args:
        objectINstanceStrIn (str): root joint string name
    Returns:
        RigComponent(object)
    '''
    if objectInstanceStrIn is None:
        rigObjs = getMetaObjectsByType(RIG)
    else:
        return rig.Rig(objectInstanceStrIn)

    return rigObjs[0]

def removeAllMetaData(obj):
    '''
    Removes all meta custom attrs
    '''
    mObj = getMPyNode(obj)
    attrs = mObj.attributeNames
    if attrs:
        for attr in attrs:
            try:
                #mObj.deleteAttr(attr)
                cmds.setAttr(f'{obj}.{attr}', lock=0)
                cmds.deleteAttr(obj, at=attr)
            except:
                print(f'{attr} could not be deleted \n')

def removeAllMetaNodes():
    '''
    Remvoes all metanode types in the scene
    '''
    metanodes = cmds.ls(type=meta_globals.meta.node_type)
    if metanodes:
        for mnode in metanodes:
            cmds.delete(mnode)

def removeBadMetaNodes():
    '''
    Remove all old metaNodes or corrupt objects:
    Args:
        None
    Returns:
        None
    '''
    metanodes = cmds.ls(type=meta_globals.meta.node_type)
    if metanodes:
        for mnode in metanodes:
            try: getMPyNode(mnode)
            except: cmds.delete(mnode)


######################################
############### MAIN #################
######################################
'''
Walk through all folders to find all 'metaclasses' folder for import
'''
initalizeAllMetaClasses()