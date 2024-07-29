######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds

import maya_utils as util
import meta.globals as globals
import meta.classes.attribute as attr_util
import meta.classes.mpy_dgnode as mpy_dgnode


######################################
############# DEFINES ################
######################################
global INITIALIZE_DEFAULT_ATTRS
INITIALIZE_DEFAULT_ATTRS = True


######################################
############# CLASSES ################
######################################
class MPyObject(mpy_dgnode.MPyDgNode):
    """Helper class to make working with Maya DG nodes easier. The class will hold a pointer
     to the data, so name changes and path resolution won't be a problem. It will also
     allow the user to interface with a Maya DG node in a more OOP manner"""

    def __init__(self, mayaNodeStr, nodeType=None):
        '''
        Return MPyObject Type
        '''
        super(MPyObject, self).__init__(mayaNodeStr, nodeType)

        # initialize obj / attrs
        self.initializeObj()

    def __str__(self):
        ''' 
        Using the str override to get the partial name

        Args:
            None

        Returns:
            None
        '''
        return "{0} with Name {1}".format(super(MPyObject, self).__str__(),
                                          self.name)

    def __repr__(self):
        '''
        Using the repr to return the full name

        Args:
            None

        Returns:
            None 
        '''
        return "{0} with Name {1}".format(super(MPyObject, self).__repr__(),
                                          self.name)

    def _metaClassName(self):
        '''
        Meta class name

        Return:
            (str) : name for the meta class.
        '''
        return self.__class__.__name__

    def _metaClassModule(self):
        '''
        Meta class module path.

        Return:
            (str) : meta class model path. 
            like scripts.util.metaclasses.fkControlComponent
        '''
        return self.__module__
    
    @property
    def UUID(self):
        ''' 
        Returns:
            the default maya UUID id
        '''
        return str(cmds.ls(self.name, uuid=1)[0])

    @property
    def shortName(self):
        if self._mDagNode:
            return self.nodeFn.fullPathName().split('|')[-1]
        return self.nodeFn.name()

    def initializeObj(self):
        '''
        Initialize DagNode, this is the core object initialization
        for all objects.

        Currently all base classes hold there own initialization, 
        MPyObject.initializeObj is for objects with simpler needs and
        not full intertance like MPyDagNode and MPyDgNode

        Args:
            mayaNodeStr (Str): the name of the object ot initialize

        Returns:
            self._nodeObj
        '''
        self.initializeAttrs()

    def initializeAttrs(self, keyable=True, userDefined=True, **kws):
        '''
        initializeAttrs needs to be implemented in all subClasses

        Args:
            None

        Returns:
            None
        '''
        global INITIALIZE_DEFAULT_ATTRS

        if INITIALIZE_DEFAULT_ATTRS:
            attr_list = util.listAttr(self.name, 
                                     keyable=keyable,
                                     userDefined=userDefined,
                                     **kws)

            if attr_list:

                for attr_str in attr_list:
                    attrType = cmds.getAttr('{0}.{1}'.format(self.name,
                                                             attr_str),
                                            type=True)
                    
                    self.addAttr(attr_str, attrType=attrType)

    def __getattr__(self, attr):
        '''
        Passing teh attrObj did not work properly...
        need to revisit

        Args:
            attr (str): attribute object type

        Returns:
            the object.value
        '''
        if attr not in self._attributes:
            return False

        return self._attributes[attr]

    def addAttr(self, 
                attrStr, 
                value=None, 
                attrType=None, 
                isLive=False, 
                **kws):
        '''
        Core function for adding attributes

        Args:
            attrStr
            value
            attrType
            att
        Returns:
            None
        '''
        # create the attibute object
        attrObj = attr_util.addAttr(nodeStr=self.name,
                                    attrStr=attrStr,
                                    value=value,
                                    attrType=attrType,
                                    isLive=isLive, 
                                    **kws)
        
        setattr(self, attrStr, attrObj)
        self._attributes[attrStr] = attrObj

        return attrObj

    def addConnection(self, 
                      attrStrName, 
                      inputObj, 
                      inputAttrStrName, 
                      srcAttrType='message',
                      desAttrType='message',
                      connectionIsInput=True):
        '''
        Wrapper for adding message "input" attributes

        Args:
            attrStrName (str): name of new attribute
            inputObj (object): must be a metaObject type
            inputAttrStrName (str): name of connect node attribute
            srcAttrType (type 'message' or 'messageArray'): message attr type for self
            desAttrType (type 'message' or 'messageArray'): message attr type for target node

        Returns:
            creates either a message or messageArray

        '''
        if isinstance(inputObj, str):
            inputObj = MPyObject(inputObj)

        # Create the destination attribute, if type is message re-create the attribute 
        # if its the wrong type
        if hasattr(inputObj, inputAttrStrName):
            if desAttrType == 'message' or desAttrType == 'messageArray': 
                if inputObj.attrType(inputAttrStrName) != desAttrType:
                    inputObj.deleteAttr(inputAttrStrName)
                    inputObj.addAttr(inputAttrStrName, attrType=desAttrType)
        else:
            if desAttrType is None:
                raise Exception('MPyObject connectAttr must be passed a attr type for creation')

            inputObj.addAttr(inputAttrStrName, attrType=desAttrType)                

        # Grab the attrObject
        destAttrObj = inputObj.attribute(inputAttrStrName)

        # Create the atribute, re-create if type mismatch
        if hasattr(self, attrStrName):
            if srcAttrType == 'message' or srcAttrType == 'messageArray': 
                if self.attrType(attrStrName) != srcAttrType:
                    self.deleteAttr(attrStrName)
                    self.addAttr(attrStrName, attrType=srcAttrType)
        else:
            if srcAttrType is None:
                raise Exception('MPyObject connectAttr must be passed a attr type for creation')

            self.addAttr(attrStrName, attrType=srcAttrType) 

        # Grab the object
        attrObj = self.attribute(attrStrName)

        # Connect:
        # i.e childObj.parent --> parentObj.children[index]
        if srcAttrType == 'message' or srcAttrType == 'messageArray':
            if connectionIsInput:
                destAttrObj.set(attrObj)
            else:
                attrObj.set(destAttrObj)
        else:
            attrObj.connect(destAttrObj)

    def deleteAttr(self, attrStr):
        """delete the attribute from the object and class interface"""

        if self._attributes.__contains__(attrStr):
            # delete
            self._attributes[attrStr].lock(False)
            self._attributes[attrStr].delete

            # remove the attribute from the list
            if self._attributes.__contains__(attrStr):
                self._attributes.pop(attrStr)

            # remove the attribute if it exists as an attribute
            if hasattr(self, attrStr):
                delattr(self, attrStr)

    def hasAttr(self, attrStr):
        '''
        Query if attribute obj exists
        Args:
            attrStr (str): attribute string name
        Returns:
            None:
        '''
        if self._attributes.__contains__(attrStr):
            return True
        return False

    def attrType(self, attrStr):
        '''
        Query attribute type
        Args:
            attrStr (str): attribute string name
        Returns:
            None:
        '''
        if self._attributes.__contains__(attrStr):
            return self._attributes[attrStr].type   

    @property
    def attributeValues(self):
        '''
        Returns all attribute objects as a list

        Args:
            None
        Returns:
            Returns a list of attribute objects
        '''
        return self._attributes.values()

    @property
    def attributeNames(self):
        '''
        Returns all attribute objects as a list

        Args:
            None
        Returns:
            Returns a list attribute string names
        '''
        return self._attributes.keys()

    def attribute(self, attrStr):
        '''
        Returns attribute object

        Args:
            attrStr (Str): the name string attribute name
        Returns:
            The attribute given object()
        '''        
        if self._attributes.__contains__(attrStr):
            return self._attributes[attrStr]
        return None

    def getGroupedAttributes(self, groupStr):
        '''
        Returns a list of attrObj(s)

        Args:
            groupStr (str): string name of the group
        Returns:
            list(Attr()): list of attributes objects
        '''
        attrObjOutputList = []
        for attrObj in self._attributes.values():
            if attrObj.attrGroup == groupStr:
                attrObjOutputList.append(attrObj)

        return attrObjOutputList

    #@property
    def isLocked(self):
        cmds.lockNode(self.name, q=True)

    #@property
    def lockNode(self, value=True):
        return cmds.lockNode(self.name, lock=value)

    #@property
    def isReferenced(self):
        return cmds.referenceQuery(self.name, isNodeReferenced=True)

class MPyDagNode(MPyObject):

    def __init__(self, mayaNodeStr, nodeType=globals.MetaCostants.mclass_transform):
        super(MPyDagNode, self).__init__(mayaNodeStr, nodeType)

    def initializeAttrs(self, keyable=True, userDefined=True, ):
        ''' 
        Initialize the base meta attributes
        '''
        # kws passed in the arg for child object to overrirde
        super(MPyDagNode, self).initializeAttrs(keyable, userDefined)

        # global for ignore
        global INITIALIZE_DEFAULT_ATTRS

        # default transform attributes
        if INITIALIZE_DEFAULT_ATTRS:
            self.addAttr('translate', attrType='double3')
            self.addAttr('rotate', attrType='double3')
            self.addAttr('scale' , attrType='double3')
            self.addAttr('rotateOrder', attrType='enum', 
                         enumName=str(cmds.attributeQuery('rotateOrder', 
                                                          node=self.name, 
                                                          listEnum=True)[0]))
    
    @property
    def nodeType(self):
        if self.shape:
            if self.mObjType == 'kLocator':
                return 'locator'
            return globals.MetaCostants.mclass_transform
        return None
    
    @property
    def parent(self):
        '''
        Returns the current parent if one
        exists, 

        Args:
            None
        Returns:
            (object): mayaObject type or None
        '''
        parent = cmds.listRelatives(self.name, parent=True)
        if parent:
            return MPyDagNode(parent[0])

        return None

    def setParent(self, newParent=None):
        '''
        Add Docs.....

        Args:
            None

        Returns:
            None

        '''
        if newParent is None:
            cmds.parent(self.name, world=True)
            
        if not isinstance(newParent, MPyDagNode):
            newParent = mpy_dgnode.MPyDgNode(newParent, globals.MetaCostants.mclass_transform)
        
        #else:
        #if isinstance(newParent, MPyObject):
            if self.parent:
                if self.parent.name != newParent.name:
                    cmds.parent(self.name, newParent.name)
            else:
                cmds.parent(self.name, newParent.name)
        
        elif isinstance(newParent, str):
            if self.parent:
                if self.parent.name != newParent:
                    cmds.parent(self.name, newParent)
            else:
                cmds.parent(self.name, newParent)                

        return self

    @property
    def children(self):
        '''
        Returns the children

        Args:
            None
        Returns:
            (object): mayaObject type or None
        '''
        children = cmds.listRelatives(self.name, 
                                      children=True, 
                                      fullPath=True,
                                      shapes=False)
        if children:
            return [MPyDagNode(c) for c in children if not cmds.objectType(c, i='locator')]

        return None

    @property
    def shape(self):
        children = cmds.listRelatives(self.name, 
                                      children=True, 
                                      fullPath=True,
                                      shapes=True,
                                      noIntermediate=True)
        if children:
            return children[0]

        return None
    
    #@property
    def hide(self):
        cmds.hide(self.name)
        print('I am being hidden')

    #@property
    def unhide(self):
        cmds.showHidden(self.name)
    
    @property
    def matrix(self, worldSpace=True):
        """
        Get the matrix for `transform`
        """
        return cmds.xform(self.name, q=True, ws=worldSpace, m=True)
    
    def setMatrix(self, matrix):
        """
        Set the matrix on `transform`
        """
        cmds.xform(self.name, ws=True, m=matrix)    

class MPyDgNode(MPyObject):
    '''
    MPyDgNode helper class to make working Maya DG nodes specificlly handling dgnodes.
    This class will hold a pointer to the oject and gives easy functions for handling the object
    It will also allow the user to interface with a Maya DG node in a more OOP manner"

    One thing to note here is inherting dierctly from MPyObject.py was desired but having
    multiple places where we have double inhertaince is a bit scary. So I am creating some dupilcate 
    code to save on pain of debugging.
    '''
    def __init__(self, mayaNodeStr, nodeType=globals.meta.node_type):

        '''
        Create a metanode if one does not exists, we need to preform this operation
        before the class super when we merged adn simplfiyied this class and parent
        class
        '''
        super(MPyDgNode, self).__init__(mayaNodeStr, nodeType)

    def create(self):
        nodeStrName = f'{self._mayaNodeStr}'
        if not cmds.objExists(nodeStrName):
            self._mayaNodeStr = cmds.createNode(self._nodeType, 
                                                name=nodeStrName)
        else:
            self._mayaNodeStr = nodeStrName

    def initializeAttrs(self):
        '''
        Subclassed from MPyObject
        '''
        super(MPyDgNode, self).initializeAttrs(keyable=False)

        # Set the evaluation to 'HasNoEffect'
        self.addAttr('nodeState', attrType='int', value=1, forceSetValue=True)

        self.addAttr(globals.meta.mclass_name, 
                     value=self._metaClassName(), 
                     attrType='string').set(self._metaClassName()).lock(True)

        self.addAttr(globals.meta.mclass_module, 
                     value=self._metaClassModule(), 
                     attrType='string').set(self._metaClassModule()).lock(True)    

    def addChildren(self, childObjList, childAttrStr=None, parentAttrStr=None):
        '''
        Connects all given children
        Args:
            childObjList (list(MayaMetaObject)): must be MetaObject object type

        Example:
        '''
        pAttr = parentAttrStr if parentAttrStr else globals.meta.mclass_parent
        cAttr = childAttrStr if childAttrStr else globals.meta.mclass_children

        for child in childObjList:
            self.addChild(child, 
                          childAttrStr=cAttr,
                          parentAttrStr=pAttr)

    def addChild(self, childObj, 
                 childAttrStr=globals.meta.mclass_children,
                 parentAttrStr=globals.meta.mclass_parent):
        '''
        Connects self.children[next index] to the given childObj
        Connect from childMetaNode.parent --> parentMetaNode.children[index]
        This follows the flow fo how maya handles connection attributes
        Args:
            childObj (object(MayaMetaObject)): must be MetaObject object type

            childAttrStr (str): attr name on self
            parentAttrStr (str): attr name on parent meta node

        Returns:
            None
        '''
        self.addConnection(attrStrName=childAttrStr,
                           inputObj=childObj,
                           inputAttrStrName=parentAttrStr,
                           srcAttrType='messageArray',
                           desAttrType='message')

    def removeChildren(self, childrenToRemove, parentAttrStr=globals.meta.mclass_parent):
        '''
        Removes children.
        Args:
            childrenToRemove (list(MetaObject)) : child that needs to be removed.
        '''
        for child in childrenToRemove:
            self.removeChild(child, parentAttrStr)

    def removeChild(self, childToRemove, parentAttrStr=globals.meta.mclass_parent):
        '''
        Remove Child from its parent.
        If we delete a child in the middle of the array, 
        make sure we remove it and reconnect the rest so that they are in a consistant order.

        Args:
            childToRemove (MetaObject) : child that needs to be removed.
        '''
        children = self.children

        if children:
            if childToRemove.name in [c.name for c in children]:
                for i, child in enumerate(children):
                    if child.name == childToRemove.name:
                        children.remove(child)
                        break
        else:
            return

        util.disconnectAttr('{0}.{1}'.format(childToRemove.name, 
                                             parentAttrStr))

    def insertChild(self, child, index):
        '''
        Insert Child into index.

        Args:
            child (MetaObject) : child to be inserted into the children.
            index (int)          : index for child to be inserted into
        '''
        children = self.children
        if index < len(children):
            self.clearChildren()
            children.insert(index, child.name)

            for i, child in enumerate(children):
                self.addConnection('{0}[{1}]'.format(globals.meta.mclass_children,
                                                     i),
                                   child,
                                   globals.meta.mclass_parent,
                                   'messageArray',
                                   'message')
        else:
            self.addChild(child)

    def clearChildren(self, childAttrStr=globals.meta.mclass_children):
        '''
        Breaks the conenctions for self.children

        Args:
            None

        Returns:
            None
        '''
        self.attribute[childAttrStr].diconnect()

    def setParent(self, parentMetaObj, 
                  parentAttrStr=globals.meta.mclass_parent, 
                  childAttrStr=globals.meta.mclass_children):
        '''
        Overloading from DGObject, 
        Connects self.name.parent with parentMetaObj.children
        The connection is outgoing and not incoming.

        Args:
            parentMetaObj (metaObject):
            parentAttrStr (str): attr name of attribute on the parent meta node
            childAttrStr  (str): attr name on self

        Returns:
            None
        '''
        self.addConnection(attrStrName=parentAttrStr,
                           inputObj=parentMetaObj,
                           inputAttrStrName=childAttrStr,
                           srcAttrType='message',
                           desAttrType='messageArray',
                           connectionIsInput=False)

    def disconnectAllAttrPlugs(self, attr, deleteSourcePlug=True, deleteDestPlug=True):
        '''
        from a given attr on the object disconnect any current connections and
        clean up the plugs by deleting the existing attributes
        '''
        for attr in self._attributes.values():
            if isinstance(attr, util.MessageAttr):
                self.attribute(attr).disconnect