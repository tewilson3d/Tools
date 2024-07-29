######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import maya.mel as mel

import namespace as ns_util
import maya_utils as util


######################################
############# DEFINES ################
######################################
NAME   = 'Name'
WEIGHT = 'Weight'
SOLO   = 'Solo'
MUTE   = 'Mute'

animLayerTypedict = {'additive':'add', 'override':'over'}

######################################
############# CLASSES ################
######################################

class AnimLayer(object):
    '''class for working with Maya anim layers '''
    def __init__(self, layer=None):
        if layer and not cmds.animLayer(layer, q=True, exists=True):
            raise ValueError('Animation Layer %s does not exist' % layer)

        self._name = layer
        self._parent = None
        self._index = -1
        self._blendNodes = None
        self._attributes = {}
        self._blendNodeData = []

    def __str__(self):
        return self.name

    @property
    def animCurves(self):
        ''' returns the anim curves associated with this layer '''
        return cmds.animLayer(self.name, q=True, anc=True)

    @property
    def attributes(self):
        ''' specific attributes on a object to the layer. return [object.attr] list'''
        return cmds.animLayer(self.name, q=True, at=True)

    @attributes.setter
    def attributes(self, attrs=None):
        ''' add [object.attr] to this layer'''
        cmds.animLayer(self.name, e=True, at=attrs)

    @attributes.deleter
    def attributes(self):
        ''' Remove all objects from layer. remove given objects please see removeAttribute '''
        cmds.animLayer(self.name, e=True, raa=True)

    @property
    def children(self):
        ''' Get the list of children layers. return value is a string array '''
        return cmds.animLayer(self.name, q=True, c=True)

    @property
    def index(self):
        ''' index property - it is 1-base index, return 0 = root animlayer, return -1 no index found'''
        if self._index == -1:
            if self.root == self.name:
                self._index = 0
            elif self.parent:
                layers =  cmds.animLayer(self.parent, q=True, c=True)
                if layers:
                    for i,l in enumerate(layers):
                        if l == self.name:
                            self._index = i + 1
                            break
        return self._index

    @property
    def lock(self):
        ''' A locked layer can not receive key. Default is false '''
        return cmds.animLayer(self.name, q=True, l=True)

    @lock.setter
    def lock(self, value=False):
        ''' Set the lock state of the layer. '''
        cmds.animLayer(self.name, e=True, l=value)

    @property
    def mute(self):
        ''' return the mute state of the layer '''
        return cmds.animLayer(self.name, q=True, m=True)

    @mute.setter
    def mute(self, value=False):
        ''' Set the mute state of the specified layer. Default is false '''
        cmds.animLayer(self.name, e=True, m=value)

    @property
    def name(self):
        ''' layer name '''
        return str(self._name)

    def setName(self, name):
        '''set the name of this layer'''
        self._name = name

    @property
    def override(self):
        ''' the overide state of the layer. '''
        return cmds.animLayer(self.name, q=True, o=True)

    @override.setter
    def override(self, value=False):
        ''' Set the overide state of the layer. Default is false '''
        cmds.animLayer(self.name, e=True, o=value)

    @property
    def parent(self):
        ''' the parent of the layer '''
        if not self._parent and self.name != self.root:
            self._parent = cmds.animLayer(self.name, q=True, p=True)
        return self._parent

    def setParent(self, parent=None):
        ''' Set the parent of the layer. Default is the animation layer root. '''
        self._parent = parent
        if parent and isExists(parent):
            cmds.animLayer(self.name, e=True, p=parent)

    @property
    def passthrough(self):
        ''' the passthrough state of the layer '''
        return cmds.animLayer(self.name, q=True, pth=True)

    @passthrough.setter
    def passthrough(self, value=False):
        ''' Set the passthrough state of the layer. Default is true. '''
        cmds.animLayer(self.name, e=True, pth=value)

    @property
    def root(self):
        ''' Return the base layer if it exist '''
        return cmds.animLayer(q=True, r=True)

    @property
    def solo(self):
        ''' the solo state of the layer '''
        return cmds.animLayer(self.name, q=True, s=True)

    @solo.setter
    def solo(self, value=False):
        ''' Set the solo state of the layer. Default is false.'''
        cmds.animLayer(self.name, e=True, s=value)

    @property
    def weight(self):
        ''' the weight of the layer '''
        return cmds.getAttr('%s.weight' % self.name)

    @weight.setter
    def weight(self, value=1.0):
        ''' Set the weight of the layer between 0.0 and 1.0. Default is 1. '''
        cmds.animLayer(self.name, e=True, w=value)

    @property
    def blendNodes(self):
        ''' returns the blend nodes associated with this layer '''
        if self.exists:
            self._blendNodes = cmds.animLayer(self.name, q=True, bld=True)
        return self._blendNodes

    @blendNodes.setter
    def blendNodes(self, blendNodes=None):
        self._blendNodes = blendNodes

    @property
    def blendNodeData(self):
        ''' returns the blend nodes data associated with this layer '''
        if not self._blendNodeData:
            if self.blendNodes:
                self.writeBlendnodeDestinations()
                for bn in self.blendNodes:
                    bnData = getBlendNodeData(bn)
                    if bnData:
                        bnData.layer = self.name
                        self._blendNodeData.append(bnData)
        return self._blendNodeData

    @blendNodeData.setter
    def blendNodeData(self, blendNodeData=None):
        self._blendNodeData = blendNodeData

    def addSelectedObjects(self):
        ''' Adds selected object(s) to the layer. '''
        cmds.animLayer(self.name, q=True, aso=True)

    def getAttr(self,attr):
        ''' return attr value of this layer '''
        value = None
        if cmds.objExists('{0}.{1}'.format(self.name, attr)):
            dataType = cmds.getAttr('.'.join((self.name, attr)), type=True, sl=True)
            if dataType == 'bool':
                value= bool(cmds.getAttr(objAttr, sl=True))
            else:
                value = cmds.getAttr(objAttr, sl=True)
            if type(value) in (list, tuple):
                if len(value) == 1:
                    if type(value[0]) in (list, tuple):
                        value = value[0]
        return value

    def setAttr(self,attr,value):
        ''' set attr value of this layer '''
        util.setAttr(self.name, attr, value, changeAttrType=False)
    
    def create(self, name=None, parent=None):
        ''' create a new anim Layer '''
        if name == None:
            self.name = cmds.animLayer()
        else:
            self.name = cmds.animLayer(name)

        if self.name:
            if parent:
                self.parent = parent

        return self.name

    def copyAnimation(self, layer=None):
        ''' copy animation from specified layer to destination layer, only animation that are on attributes
        layered by both layer that are concerned. '''
        if isExists(layer):
            cmds.animLayer(self.name, ca=layer)
        
    @property
    def exists(self):
        ''' Determine if the specified layer exists., default is checking itself'''
        if self.name:
            return cmds.animLayer(self.name, q=True, ex=True)
        return False

    def moveLayerAfter(self, layer=None):
        ''' Move layer after the specified layer '''
        if isExists(layer):
            cmds.animLayer(self.name, mva=layer)

    def moveLayerBefore(self, layer=None):
        ''' Move layer befor the specified layer '''
        if isExists(layer):
            cmds.animLayer(self.name, mvb=layer)

    def getObjects(self):
        ''' get connected objects '''
        allMembers = self.attributes
        objects = []
        if allMembers:
            objects = list(set([m.split('.')[0] for m in allMembers]))
        return objects

    def removeAttribute(self, objects=None):
        ''' Remove object(s) from layer. '''
        if objects:
            cmds.animLayer(self.name, e=True, ra=objects)

    def writeBlendnodeDestinations(self, value=True):
        ''' writes the destination plugs of the blend nodes that belong to the layer into the blend node.
        This is used for layer import/export purposes and is not for general use. '''
        cmds.animLayer(self.name, e=True, writeBlendnodeDestinations=value)


######################################
############# FUNCTIONS ##############
######################################
def selectAnimLayer(animLayer = ''):
    if not cmds.objExists(animLayer):
        return cmds.warning('Anim Layer does not exists')
    
    # clear the selection of animLayers
    allLayers = cmds.ls(type = 'animLayer')
    for layer in allLayers:
        cmds.animLayer(layer, e = True, preferred = False)
        cmds.animLayer(layer, e = True, selected = False)
    
    # select the specified animLayer 
    cmds.animLayer(animLayer, e = True, preferred = True)
    cmds.animLayer(animLayer, e = True, selected = True)
    
    cmds.dgeval(allLayers) # eval the connections because Maya fails to evaluate animlayer changes properly
    
def getCurrentAnimLayer():
    '''
    Returns active selected animalayer
            
    Args:
        None
            
    Returns:
        None
            
    '''
    layers = cmds.ls(type='animLayer')
    for layer in layers:
        if cmds.animLayer(layer, q=True, sel=True):
            return layer

def getAllAnimLayers():
    """
    Returns all animLayers
        
    Args:
        None
        
    Returns:
        A list of AnimLayer objects
        
    """
    alList = []
    animLayers = cmds.ls(type='animLayer')
    
    if animLayers:
        for layer in animLayers:
            alList.append(AnimLayer(layer))
            
    return alList

def getAllActiveLayers():
    '''
    Gets all the animLayers "not" muted
            
    Args:
        None
            
    Returns:
        activeLayerList (list[AnimLayer Objects]):
            
    '''
    activeLayerList = []
    animLayers = getAllAnimLayers()
    
    if animLayers:
        for layer in animLayers:
            if not layer.mute:
                activeLayerList.append(layer)
    
    return activeLayerList

def muteAllOtherLayers(activeLayerIn):
    """
    Mutes all layers expect the one provided "active"
        
    Args:
        activeLayerIn (list / str): string name of the layer to not mute
        need to handle multiple layers

    Returns:
        None
        
    """
    layerObjs = []

    # mute all anim layers
    allAnimLayerObjs = getAllAnimLayers()
    
    if type(activeLayerIn) != list:
        if not isinstance(activeLayerIn, AnimLayer):
            layerObjs = [AnimLayer(activeLayerIn)]  
        else:
            layerObjs = [activeLayerIn]
    else:
        for layerIn in activeLayerIn:
            if not isinstance(activeLayerIn, AnimLayer):
                layerObjs.append(AnimLayer(layerIn))  
            else:
                layerObjs.append(layerIn)

    # mute all other laters expect root
    muteAllAnimLayers()
    for layerObj in layerObjs:
        layerObj.mute = False
        layerObj.lock = False

def muteAllAnimLayers():
    '''
    Mutes all the animlayers expect for BaseAnimation
    (which should never be locked)

    Args:
        None
    
    Returns:
        None
    ''' 
    allAnimLayerObjs = getAllAnimLayers()
    
    for animLayerObj in allAnimLayerObjs:
        if animLayerObj.name != animLayerObj.root:
            animLayerObj.mute = True
            animLayerObj.lock = True
    
# test