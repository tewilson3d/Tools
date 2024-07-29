######################################
############# IMPORTS ################
######################################
import sys
import json
import contextlib
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

import meta.globals as globals
import meta.classes.mpy_dgnode as mpy_dgnode


######################################
############# DEFINES ################
######################################
MESSAGEARRAY = 'messageArray'
MESSAGE      = 'message'
ENUM         = 'enum'
STRING       = 'string'
BOOL         = 'bool'
INT          = 'int'


######################################
############# CLASSES ################
######################################
class Attr(object):

    def __init__(self, 
                 attrStr, 
                 mayaNodeStr, 
                 value=None, 
                 attrType=None, 
                 lock=False,
                 isLive=False,
                 forceCreate=False,
                 forceSetValue=False,
                 displayName=None, 
                 attrGroup=None, **kws):
        '''
        '''
        # Set rebuild option
        self._type   = attrType
        self._isLive = isLive

        # Initilize Attr
        self._attrName     = attrStr
        self.plugNodeObj = mpy_dgnode.MPyDgNode(mayaNodeStr,
                                                cmds.objectType(mayaNodeStr))
        self._niceName   = displayName
        self._attrGroup  = attrGroup
        createAttr       = True        

        # MDGModifier instanse for connecting
        self.attrMDGModifier = OpenMaya.MDGModifier()        

        if self.plugNodeObj.nodeFn.hasAttribute(self._attrName):

            # If we want to force the creation
            if forceCreate:
                cmds.deleteAttr('{0}.{1}'.format(self.nodeName,
                                                 self._attrName))
            else:
                createAttr = False

        if createAttr:
            self.createAttr(self._attrName, value, self.type, **kws)

            # Initialize the plug
            self.initializePlug()

            # Set the keyable and channelBox states
            if kws.__contains__('keyable'):
                keyable = kws['keyable']
            else:
                keyable = True

            if kws.__contains__('channelBox'):
                channelBox = kws['channelBox']
            else:
                channelBox = False

            self.setKeyable(keyable, channelBox)

            if lock: 
                self.lock            

        else:
            # Initialize the plug
            self.initializePlug()

        # If the type is still none try and set it based on value
        if self._type == None and value:
            self._type = getAttributeTypeFromValue(value)

        # Set the attrGroup if given
        if self._attrGroup:
            self.attrGroup = self._attrGroup

        # Need to insure messageArry are set properly
        elif self.type == 'message':
            if self.mPlug.isArray:
                self._type = 'messageArray'

        if forceSetValue and value:
            self.set(value)

    def initializePlug(self):
        '''
        Initilze our MPlugAttr from self.plugNodeObj

        Args:
            node (string): the parent object of the attribute

        Returns:
            self.mPlug (MPlug)
        '''
        self.mPlug = self.plugNodeObj.plug(self._attrName)

    @property
    def name(self):
        '''
        Return the combined name of the plugNodeObj.name
        and the mplug partialName
        '''
        return '{0}.{1}'.format(self.plugNodeObj.name,
                                self.plug.partialName())

    @property
    def nodeName(self):
        ''' 
        dgNode.name is our custom property 
        '''
        return self.plugNodeObj.name

    @property
    def displayName(self):
        return self._niceName

    @displayName.setter
    def displayName(self, displayName):
        self._niceName = displayName

    @property
    def attrGroup(self):
        return self._attrGroup

    @attrGroup.setter
    def attrGroup(self, attrGroup):
        self._attrGroup = attrGroup

    @property
    def plug(self):
        '''
        Returns the actual MPlug object
        '''
        if self.mPlug.isNull:
            # If the plug is not valid any more, make sure to reset it.
            self.initializePlug()
        return self.mPlug

    def lock(self, valueBool):
        self.plug.isLocked = valueBool

    @property
    def isLocked(self):
        return self.plug.isLocked

    @property
    def live(self):
        return self._isLive

    @live.setter
    def live(self, valueBool):
        '''
        Set whether the attibute can be dynamiclly deleted
        and created

        Args:
            valueBool (bool): 
        Returns:
            None
        '''
        self._isLive = valueBool

    @property
    def get(self):
        '''
        Main function for getAttr

        Args:
            None

        Returns:
            the attribute value
        '''
        # String Attr
        if self.type == 'string':
            stringData = self.plug.asString()
            return self._getStringData(stringData)

        elif self.type == 'double3':
            return cmds.getAttr(self.name)[0]

        elif self.type == 'int':
            return self.plug.asInt()

        elif self.type == 'float':
            return self.plug.asFloat()

        # ???
        else:
            return cmds.getAttr(self.name)

    def set(self, value):
        '''
        Main function for setting attributes

        Args:
            value (void): the new value of the attr
            isLive (bool): rebuilds the attribute and will
                                will create the new attributes
                                based on the value type

        Example:
            None

        Returns:
            None

        '''
        # if attr is locked, unlock
        with self.restoreLockState():

            # check value Type
            valueType = getAttributeTypeFromValue(value)

            # If new attribute type is different, delete the old
            # and create a new attribute from value type
            if self._isLive:
                if not self.type == valueType:
                    # clean up
                    try: self.delete
                    except: pass

                    # create new attr
                    self.createAttr(self._attrName,
                                    value=value, 
                                    attrType=valueType)

                    # re-intialize our plug
                    self.initializePlug()
                    return            

            # string
            if self.type == 'string':

                # Handle lazy attribute types
                if value:
                    if type(value) == str:
                        if value.lower() == 'none':
                            value = None

                self.plug.setString(self._setStringData(value))

            # int
            elif self.type == 'int':
                self.plug.setInt(value)

            # bool
            elif self.type == 'bool':
                self.plug.setBool(value)

            # float
            elif self.type == 'float':
                self.plug.setFloat(value)

            # double3
            elif self.type in ['double3','float3']:
                cmds.setAttr(self.name, value[0], value[1], value[2])

            # doubleArray
            elif self.type == 'doubleArray':
                cmds.setAttr(self.name, value, type='doubleArray')

            # matrix
            elif self.type == 'matrix':
                cmds.setAttr(self.name, value, type='matrix')

            else:
                cmds.setAttr(self.name, value)

        return self

    @property
    def setDefault(self):
        '''
        Sets the attribute to the the defalut value
        '''
        val = cmds.attributeQuery(self._attrName, n=self.nodeName, ld=True)
        if val:
            try:
                self.set(val[0])
            except:
                print('Unable to set {0}'.format(self.name))

        return self

    def connect(self, attrObj):
        '''
        Connect attr does a connectionAttr for like type attributes

        Args:
            attrObj (AttrObj): attribute object type
        '''
        # disconnect if connected
        if attrObj.isConnected:
            attrObj.disconnect

        # Connect
        self.attrMDGModifier.connect(self.plug, attrObj.plug)
        self.attrMDGModifier.doIt()        

    @property
    def isConnected(self):
        """check if plug is connected"""
        return self.plug.isConnected

    @property
    def disconnect(self):
        '''
        Overloading the parent class diconnect to help better
        handle attribute arrays

        Need to figure outto handle it with api-----

        Args:
            None

        Returns:
            None
        '''
        # Incoming
        plug = self.plug.connectedTo(True, False)

        if len(plug):
            self.attrMDGModifier.disconnect(plug[0], self.plug)
            self.attrMDGModifier.doIt()

        # Outgoing
        else:
            plug = self.plug.connectedTo(False, True)
            if len(plug):
                self.attrMDGModifier.disconnect(self.plug, plug[0])
                self.attrMDGModifier.doIt()  

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        '''
        Figure out what type of attribue
        Not sure if this needed..... 
        Args:
            value (void): value type

        Returns:
            Sets the _type value
        '''
        value = getAttributeTypeFromValue(value)
        self._type = value

    @property
    def exists(self):
        return self.plugNodeObj.nodeFn.hasAttribute(self._attrName)

    @property
    def keyable(self):
        return self.plug.isKeyable

    @property
    def delete(self):
        '''
        Delete the attribute from object and cleans itself from memory
        '''
        try:
            self.lock(False)
            cmds.deleteAttr(self.plug.name())
        except:
            print(self._attrName + ' could not be deleted')

    def asMayaString(self):
        '''
        Set value as default maya string value. This is different
        from setValue which uses json to store the data type
        '''
        if self.get == None:
            cmds.setAttr(self.name, '', type='string')
        else:
            cmds.setAttr(self.name, str(self.get), type='string')

        return self

    def setKeyable(self, isKeyable=True, showInChannelBox=False):
        '''
        Atribute channelBox in maya is logically backwards (in my opinion)
        if 'showValueBool' is true the attribute will be visible and can be
        expeclity keyed but will not "auto" keyframed. 

        This nust be used in conjuction with setAttr(keyable) or it will be hidden

        Args:
            isKeyable (bool):
            showValueBool (bool):

        Example:
            to show and not key, isKeyable=False and showValueBool=True
            to show and to key , isKeyable=True and showValueBool=False

        '''
        self.plug.isKeyable = isKeyable
        self.plug.isChannelBox = showInChannelBox

    def createAttr(self, attr, value, attrType, **kws):
        ''' 
        Attribute creation function, this does all the heavy lifting for us

        Document......
        '''
        DataTypeKws = {'string': {'longName':attr, 'dt':'string'}, 
                       'unicode': {'longName':attr, 'dt':'string'}, 
                       'int': {'longName':attr, 'at':'long'}, 
                       'bool': {'longName':attr, 'at':'bool'}, 
                       'float': {'longName':attr, 'at':'double'}, 
                       'double': {'longName':attr, 'at':'double'},
                       'float3': {'longName':attr, 'at':'double3'}, 
                       'double3': {'longName':attr, 'at':'double3'}, 
                       'doubleLinear': {'longName':attr, 'at':'double'},
                       'doubleArray':{'longName':attr, 'dt':'doubleArray'}, 
                       'enum': {'longName':attr, 'at':'enum'}, 
                       'messageArray': {'longName':attr, 'at':'message', 'm':True, 'im':True},
                       'message':{'longName':attr, 'at':'message', 'm':False}}

        #
        # need compound support
        #

        # If enum attribute type insure that enumName was passed
        if attrType and attrType=='enum' and not 'enumName' in kws:
            raise ValueError('enum attrType must be passed with "enumName" keyword in args')

        # If no attrType was specified determine type by value type
        if attrType is None:
            attrType = getAttributeTypeFromValue(value)

        # if enumName exist we need to insure that its in proper string format
        if 'enumName' in kws:
            kws['enumName'] = convertEnumVariableToStr(kws['enumName'])

        # specific attribute that need to be removed from default keys
        removealKey = ['channelBox']
        for rkey in removealKey: 
            if rkey in kws.keys(): 
                kws.pop(rkey)

        # allow to pass all standard maya args
        DataTypeKws[attrType].update(kws)

        # addAttr
        cmds.addAttr(self.nodeName, **DataTypeKws[attrType])

        # set Attribute type
        self._type = attrType

        # Set the attribute value
        if self.type == 'message' or self.type == 'messageArray':
            return

        if self.type =='double3' or self.type =='float3':
            attr1='{0}X'.format(attr)
            attr2='{0}Y'.format(attr)
            attr3='{0}Z'.format(attr)

            for at in [attr1, attr2, attr3]:
                cmds.addAttr(self.nodeName, longName=at, at='double', parent=attr, **kws)

            if value:
                cmds.setAttr('{0}.{1}'.format(self.nodeName, self._attrName), 
                             value[0],
                             value[1],
                             value[2])

            return

        elif self.type =='doubleArray':
            cmds.setAttr('{0}.{1}'.format(self.nodeName, 
                                          self._attrName), [], type='doubleArray')
            return

        elif self.type == 'string':
            cmds.setAttr('{0}.{1}'.format(self.nodeName, 
                                          self._attrName), 
                         self._setStringData(value), type='string')
            return         

        if value:
            cmds.setAttr('{0}.{1}'.format(self.nodeName, 
                                          self._attrName), value)

    def _setStringData(self, data):
        '''
        This is too replace the old cPickle serialize,deserializePickle

        Test the len of the string, anything over 32000 (16bit) gets screwed by the
        Maya attribute template and truncated.

        thanks to MarkJ and Red9 for breakign through this.
        http://markj3d.blogspot.co.uk/2012/11/maya-string-attr-32k-limit.html
        '''
        if data and len(data)>32700:
            cmds.error('{0} Data is too large and cannot be handled by Maya"s attribute template'.format(data))
        return json.dumps(data)

    def _getStringData(self, data):
        ''' Unpack the string json data '''
        # Return none if attr data is empty
        if not data:
            return None

        if type(data) == str:
            strValue = json.loads(str(data))
            if strValue == 'None': 
                return None
            return strValue

        return json.loads(data)

    @contextlib.contextmanager
    def restoreLockState(self):
        '''
        Restore Lock state.

        Args:
            nodeAttrString (str) : node.attr string.
        '''
        try:
            if self.isLocked:
                self.lock(False)
            yield

        finally:
            if self.isLocked:
                self.lock(True)

class MessageAttr(Attr):
    """class to help deal with passing input (message) connection attributes"""

    def __init__(self, attrStr, mayaNodeStr, value=None, attrType=None, isLive=False, **kws):
        '''


        '''
        self._isLive = isLive
        super(MessageAttr, self).__init__(attrStr,mayaNodeStr,value,attrType,**kws)

        # Type
        if self.plug.isArray:
            self._type = 'messageArray'
        else:
            self._type = 'message'

    @property
    def get(self):
        '''
        Overloads the parent class value property

        ?? Need to figure out how to when we want to handle
        both incoming and ourgoing input attributes

        Args:
            None

        Returns:
            the connected object(s)
        '''
        msgOutputList = []
        if self.plug.isArray:
            for i in range(self.plug.numElements()):
                mplugObj = self.plug.elementByPhysicalIndex(i)
                if not mplugObj.isConnected:
                    continue

                # Incoming
                if mplugObj.isDestination:
                    plug = mplugObj.connectedTo(True, False)

                # Outgoing
                elif mplugObj.isSource:
                    plug = mplugObj.connectedTo(False, True)

                for i in range(len(plug)):
                    msgOutputList.append(self._mObjToName(plug[i].node()))

            return msgOutputList

        else:
            # Incoming
            plug = self.plug.connectedTo(True, False)

            if len(plug):
                return self._mObjToName(plug[0].node())

            # Outgoing
            else:
                plug = self.plug.connectedTo(False, True)
                if len(plug):
                    return self._mObjToName(plug[0].node())

    def _mObjToName(self, mObj):
        '''
        Wrapper for returning the name of an mobject

        Args:
            mobj(MObject): openmaya.mobject
        Returns
            name (str): string name
        '''
        # create an obejct
        if mObj.hasFn(OpenMaya.MFn.kTransform):
            nodeFn = OpenMaya.MFnDagNode(mObj)
            nodeObj = mpy_dgnode.MPyDgNode(nodeFn.fullPathName())
            
        else:
            nodeObj = mpy_dgnode.MPyDgNode(OpenMaya.MFnDependencyNode(mObj).name())

        # Return SkinCluster
        if nodeObj.mObjType == 'kSkinClusterFilter':
            from rigging.metaclasses import skincluster
            return skincluster.SkinCluster(nodeObj.name)

        elif nodeObj.mObjType == 'kAffect':

            if cmds.objectType(nodeObj.name) == globals.meta.skinnode_type:
                from rigging.metaclasses import skinnode
                return skinnode.SkinNode(nodeObj.name)

            elif cmds.objectType(nodeObj.name) == globals.meta.node_type:

                metaClassName = getAttr(nodeObj.name, globals.meta.mclass_name)
                metaClassModule = getAttr(nodeObj.name, globals.meta.mclass_module)

                moduleObj = sys.modules[metaClassModule]
                metaClassObj = getattr(moduleObj, metaClassName)
                return metaClassObj(nodeObj.name)

        # Return a JointObject
        elif nodeObj.mObjType == 'kJoint':
            from rigging.metaclasses import joint
            return joint.Joint(nodeObj.name)

        # Return Transform
        elif nodeObj.mObjType == 'kTransform':
            from modeling.metaclasses import mesh
            return mesh.Transform(nodeObj.name) 

        # Return a generic object
        else:
            return nodeObj

    def set(self, attrObj):
        '''
        Wrapper for connect
        '''
        self.connect(attrObj)

    def connect(self, attrObj):
        '''
        Overloaing the parent setValue to handle 
        input connections specifcially

        Args:
            attrObj (object): Must be type Attr()
            isLive (bool): rebuilds the attribute and will
                                will create the new attributes
                                based on the value type

        Returns:
            None
        '''
        # if attr is locked, unlock
        with self.restoreLockState():

            # If we change our inputAttrPlug type from either
            # message to messageArray or vise versa then
            # we need to re-create the attribute
            reCreate = False
            if self._isLive:

                if self.type == 'message':
                    if self.plug.isArray:
                        reCreate = True

                elif self.type == 'messageArray':
                    if not self.plug.isArray:
                        reCreate = True

                # clean up
                if reCreate:
                    self.delete

                    # create new attr
                    self.createAttr(self._attrName,
                                    value=attrObj.nodeName, 
                                    attrType=self.type)

            # Ensure the destiantion attribute exits
            if attrObj.type != MESSAGE and attrObj.type != MESSAGEARRAY:
                raise ValueError('{0}: Is Wrong Object Type'.format(attrObj.name))

            # Determine if either the conenction type
            if self.plug.isArray:
                outputAttrPlug = self.getNextArrayIndex
            else:
                outputAttrPlug = self.plug

            if attrObj.plug.isArray:
                inputAttrPlug = attrObj.getNextArrayIndex
            else:
                inputAttrPlug = attrObj.plug

            # maybe we need to have some protection here 
            if attrObj.isConnected:
                attrObj.disconnect

            # Connect
            self.attrMDGModifier.connect(outputAttrPlug, inputAttrPlug)
            self.attrMDGModifier.doIt()

    @property
    def getNextArrayIndex(self):
        '''
        Get the next available index in a multiMessage array

        Args:
            source (bool): input coming in
            destination (bool): imput going out

        Returns:
            None
        '''
        ind = self.plug.numElements()

        if ind == 0:
            return self.plug.elementByLogicalIndex(ind)

        ind = self.plug.elementByPhysicalIndex(ind-1).logicalIndex() + 1
        return self.plug.elementByLogicalIndex(ind)

    @property
    def plugArray(self):
        '''
        plugArray returns a list of MPlugs from self.plugNodeObj

        Args:
            None
        Returns:
            plugArray (list[MPlug]): list of MPlug objects
        '''
        return self.plugNodeObj.plugArray(self._attrName)

    @property
    def disconnect(self):
        '''
        Overloading the parent class diconnect to help better
        handle attribute arrays

        Need to figure outto handle it with api-----

        Args:
            None

        Returns:
            None
        '''
        # Meassage Arrary
        if self.type == 'messageArray':

            # Need to handle incoming and outgoign
            for i in range(self.plug.numElements()):
                mplugObj = self.plug.elementByPhysicalIndex(i)
                if not mplugObj.isConnected():
                    continue

                #mplugArray = OpenMaya.MPlugArray()
                plug = mplugObj.connectedTo(False, True)
                for i in range(len(plug)):
                    self.attrMDGModifier.disconnect(mplugObj, plug[i])
                    self.attrMDGModifier.doIt()

        # Message
        else:

            # Incoming
            plug = self.plug.connectedTo(True, False)

            if len(plug):
                self.attrMDGModifier.disconnect(plug[0], self.plug)
                self.attrMDGModifier.doIt()

            # Outgoing
            else:
                plug = self.plug.connectedTo(False, True)
                if len(plug):
                    self.attrMDGModifier.disconnect(self.plug, plug[0])
                    self.attrMDGModifier.doIt()    


class EnumAttr(Attr):
    """class to help deal with passing input (message) connection attributes"""

    def __init__(self, attrStr, mayaNodeStr, value=None, attrType=None, isLive=False, **kws):
        '''
        MPlug::elementByLogicalIndex()
        indexPlug = myPlug.elementByLogicalIndex(9)
        indexPlug.setValue(20.0)
        attrName[8]@

        '''
        self._isLive = isLive
        self._preserve = False
        super(EnumAttr, self).__init__(attrStr,mayaNodeStr,value,attrType,**kws)

    @property
    def get(self):
        '''
        Overloads the parent class value property
        '''
        return self.plug.asShort()

    def set(self, value, *args):
        '''
        Overloaing the parent setValue to handle 
        input connections specifcially

        Args:
            value (void): the attribute value
        Returns:
            None
        '''
        # if attr is locked, unlock
        with self.restoreLockState():

            # check value Type
            attrType = self.type

            if self._isLive:
                # pull enumName from *args

                # clean up
                self.delete

                # create new attr
                self.createAttr(self._attrName, 
                                attrType=attrType,
                                value=value)
                return            

            # need to handle the rotateorder very specifically
            # TO DO --- smarter way maybe.
            if self._attrName == 'rotateOrder':

                if type(value) is int:
                    value = self.getIndexAsStr(value)

                # ensure the value is type str
                cmds.xform(self.nodeName, rotateOrder=value, preserve=self._preserve)

            else:
                # set the value despite the what is paseed
                # either index or string value
                if type(value) is str:
                    enums = cmds.attributeQuery(self._attrName, 
                                                node=self.nodeName, 
                                                listEnum=True)[0].split(':')
                    value = enums.index(str(value))

                # esnure value is type int
                self.plug.setShort(value)

        return self

    @property
    def preserve(self):
        ''' 
        This is is soley for maya rotateOrder enum, prevering is crucile
        '''
        self._preserve = True
        return self._preserve

    @property
    def getStr(self):
        """
        Query Maya Enum Values

        Args:
            None

        Keyword Args:
            node (obj): Node To Query
            attr (str): Enum Attribute Name

        Returns:
            (str): Enum Values as int or string??
        """
        enumIndex = self.get
        currentEnumList = self.getStrList
        return currentEnumList[enumIndex]   

    @property
    def getStrList(self):
        """
        Query Maya Enum Values

        Args:
            None

        Keyword Args:
            node (obj): Node To Query
            attr (str): Enum Attribute Name

        Returns:
            (list): Enum Values as int or string??
        """
        return cmds.attributeQuery(self._attrName, 
                                   node=self.nodeName, 
                                   le=True)[0].split(":")

    @property
    def getIndex(self):
        '''
        Returns the current Enum Index value
        '''
        return cmds.getAttr(self.name)

    def getIndexAsStr(self, enumIndex):
        '''
        Find the str value from index
        '''
        currentEnumList = self.getStrList
        return currentEnumList[enumIndex]  


######################################
############# FUNCTIONS ##############
######################################
def getAttributeTypeFromValue(val):
    '''
    Validate the value type to deteremine the appropriate attribute type.
    This helper function is to mainly support attribute creating when only 
    a value is given.
    '''
    if issubclass(type(val), str):
        return 'string'
    if issubclass(type(val), bool):
        return 'bool'
    if issubclass(type(val), int):
        return 'int'
    if issubclass(type(val), float):
        return 'float'
    if issubclass(type(val), dict):
        return 'string'
    if issubclass(type(val), list):
        return 'string'
    if issubclass(type(val), tuple):
        return 'string'

def addAttr(nodeStr,
            attrStr,
            value=None,
            attrType=None,
            isLive=True, 
            **kws):
    ''' 
    Wrapper function for adding attributes, uses Attr() and cleans object instance
    Still working through the use cases

    Args:
        nodeStr
        attr
        value
        attrType
        isLive
        forceCreate <- kws

        Standard Maya args:
            hidden
            minVal
            maxVal
            default
            keyable
            channelBox
            hasMinMax
            enumName <- must be passed for EnumAttr

    Examples:
        None

    Returns:
        Attribute Object
    '''
    if attrType == None and value:
        attrType = getAttributeTypeFromValue(value)

    elif attrType is None and value is None:
        if cmds.objExists('{0}.{1}'.format(nodeStr,attrStr)):
            attrType = cmds.getAttr('{0}.{1}'.format(nodeStr,
                                                     attrStr),
                                    type=True)

    if attrType == 'message' or attrType == 'messageArray':
        return MessageAttr(attrStr=attrStr,
                           mayaNodeStr=nodeStr,
                           value=value,
                           attrType=attrType,
                           isLive=isLive,
                           **kws)
    elif attrType == 'enum':
        return EnumAttr(attrStr=attrStr,
                        mayaNodeStr=nodeStr,
                        value=value,
                        attrType=attrType,
                        isLive=isLive,
                        **kws)
    else:
        return Attr(attrStr=attrStr,
                    mayaNodeStr=nodeStr,
                    value=value,
                    attrType=attrType,
                    isLive=isLive,
                    **kws)       

def getAttr(mayaNodeStrName, attrStrName):
    '''
    Wrapper for Attr.getAttr() or SubClass of
    '''
    atType = cmds.getAttr('{0}.{1}'.format(mayaNodeStrName,
                                           attrStrName),
                          type=True)

    if atType == 'message':
        plugObject = MessageAttr(attrStrName, 
                                 mayaNodeStrName,
                                 attrType=atType)
    elif atType == 'enum':
        plugObject = EnumAttr(attrStrName, 
                              mayaNodeStrName,
                              attrType=atType)        
    else:
        plugObject = Attr(attrStrName, 
                          mayaNodeStrName,
                          attrType=atType)

    return plugObject.get

def convertEnumVariableToStr(enumNameValues):
    ''' Returns the enumNameValues as a 'string:string' '''

    # List type
    if type(enumNameValues) == list:
        enumNameStr = '{0}:'.format(enumNameValues[0])
        for enumName in enumNameValues[1:]:
            enumNameStr += '{0}:'.format(enumName)
        return enumNameStr

    # Dict type
    elif type(enumNameValues) == dict:
        enumNameStr = ':'
        for k,v in enumNameValues.items():
            enumNameStr += '{0}:'.format(v)
        return enumNameStr

    else:
        return enumNameValues