######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya


######################################
############# DEFINES ################
######################################


######################################
############# CLASSES ################
######################################
class MPyDgNode(object):
    """wrapper class that holds MMPyDgNode and makes interfacing with MMPyDgNode easier"""

    def __init__(self, mayaNodeStr, nodeType=None):
        '''
        Return MPyNode Type
        '''
        self._mDagNode    = None
        self._mayaNodeStr = mayaNodeStr if mayaNodeStr != '' else 'Temp'
        self._nodeType    = nodeType
        self._attributes  = {}

        # insure object exists or create it
        if not cmds.objExists(self._mayaNodeStr):
            self.create()
        
        if self._nodeType is None:
            self.getNodeType()

        selList = OpenMaya.MSelectionList()
        selList.add(self._mayaNodeStr)
        self._mObject = selList.getDependNode(0)

        # verify if object is of dag type
        if self._mObject.hasFn(OpenMaya.MFn.kTransform):
            self.nodeFn = OpenMaya.MFnDagNode(self._mObject)
            self._mDagNode = selList.getDagPath(0)

        # handles all other types
        else:
            self.nodeFn = OpenMaya.MFnDependencyNode(self._mObject)

    def getNodeType(self, nodeTypeStrIn=None): 
        '''
        Core method foe dfining the nodeType, used in conjuction with create()
        '''
        if nodeTypeStrIn and self._nodeType is None: self._nodeType = nodeTypeStrIn
        elif self._mayaNodeStr is not None: self._nodeType = cmds.objectType(self._mayaNodeStr)

    @property
    def nodeType(self):
        '''
        Returns the nodeType
        '''
        return self._nodeType
    
    def create(self):
        '''
        This funciton should be handled in the inhertiance
        '''
        self._mayaNodeStr = cmds.createNode(self._nodeType, 
                                            name=f'{self._mayaNodeStr}')

    @property
    def mObject(self):
        ''' 
        Returns the MObject
        '''
        return self._mObject

    @property
    def mPyDgNode(self):
        if hasattr(self.nodeFn, 'fullPathName'):
            return self._mDagNode
        return None

    @property
    def name(self):
        '''
        Returns the str name of the object
        '''
        # here provide the mayaNodeStr name if the nodeFn
        # function set has not been created yet
        if not self.nodeFn:
            return self._mayaNodeStr
        
        # use the MFn function class for the string name
        if hasattr(self.nodeFn, 'fullPathName'):
            return self.nodeFn.fullPathName()
        return self.nodeFn.name()

    @property
    def basename(self):
        '''
        Removes the namespace and pipe of our object

        Args:
            No args for this property

        Returns:
            objectName(str): the clean name of the object
        '''
        ns = self._mDagNode.fullPathName().split(':')
        if len(ns) > 1:
            return ns[-1]
        return ns[0].split('|')[-1]    

    @property
    def namespace(self):
        '''
        Returns the namespace f our object

        Args:
            No args for this property

        Returns:
            namespace(str): the namespace of object
        '''
        ns = self.name.split(':')
        if len(ns) > 1:
            return ns[0].split('|')[-1]
        return ':'

    def strip_namespace(self):
        '''
        Returns the namespace f our object

        Args:
            No args for this property

        Returns:
            namespace(str): the namespace of object
        '''
        ns = self.name.split(':')
        if len(ns) > 1:
            return ns[1:]
    
    def rename(self, newname):
        ''' Name/Rename function 

        Args:
            newName (str): new str name

        Returns:
            None
        '''
        node = OpenMaya.MFnDependencyNode(self._mObject)
        currentname = node.name()
        if newname is not currentname:
            node.setName(newname)
            #cmds.rename(currentname, newname)

    def plug(self, attrStr):
        '''
        Get the plug for the specific attribute dgNode

        Args:
            attrStr (str): attribute string name
        Returns:
            MPlug object
        '''
        return self.nodeFn.findPlug(attrStr, False)

    def plugArray(self, attrStr, outgoing=True, incoming=False):
        '''
        Get the plugarray for the specific attribute dgNode

        Args:
            attrStr (str): attribute string name
        Returns:
            A list of MPlug object(s)
        '''
        plugArrayList = []

        plugArrayObj = self.plug(attrStr)
        for i in range(plugArrayObj.numElements()):
            elemPlug = plugArrayObj.elementByLogicalIndex(i)
            mplugArrayObj = OpenMaya.MPlugArray()
            elemPlug.connectedTo(mplugArrayObj,
                                 outgoing,
                                 incoming)

            for j in range(mplugArrayObj.length()):
                plugArrayList.append(mplugArrayObj[j])

        return plugArrayList

    @property
    def mObjType(self):
        '''
        Returns the object type
        '''
        apiTypeIntToString = {getattr(OpenMaya.MFn, attr): attr for attr in dir(OpenMaya.MFn)}
        return apiTypeIntToString[self.mObject.apiType()]