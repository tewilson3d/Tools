######################################
############# IMPORTS ################
######################################
import filepath
import maya.cmds as cmds

import meta.globals as globals
import studio.tools.content_exporter.metaclasses.util.mpy_modelexport_util as modelexport_util
import studio.tools.content_exporter.metaclasses.mpy_export_object as mpy_export_object
import studio.tools.content_exporter.metaclasses.util.mpy_modelexport_util as model_export_util
import modeling.metaclasses.mesh as mesh

from unreal_tools.utils.globals import ue

######################################
############# CLASSES ################s
######################################
class ContainerObject(mpy_export_object.ExportObject):

    def __init__(self, mayaNodeStr=None):
        super(ContainerObject, self).__init__(mayaNodeStr)
        self.util = modelexport_util.Util(self)
    
    def initializeAttrs(self):
        '''
        Args:
            Inherits exportPath from parent mpy_export_object ***

        Returns:
            None
        '''
        super(ContainerObject, self).initializeAttrs()
        self.addAttr('container_name', attrType='string')
        self.addAttr('export_nodes', attrType='messageArray')
        self.addAttr('export_meshes', attrType='string')
        self.addAttr('rig_name', attrType='string')
        self.addAttr('export_group_node', attrType='message')
        self.addAttr('manfacture', attrType='string')

        self.export.set(False)
    
    def get_group_node(self):
        return list(set([ContainterMeshObject(m) for m in cmds.listRelatives(m, p=True, type='transform') for m in self.export_meshes.grt]))
    #@property
    #def json_path(self):
        #return filepath.ExportPath(cmds.file(q=True, sn=True)).dir().join(f'{self.container_name.get}_{JSON_EXPORT_NAME}')
    
    @property
    def export_path(self):
        return filepath.FilePath(cmds.file(q=True, sn=True)).dir().join(['Export', 
                                                                           f'{self.container_name.get}'])
    
class ContainterMeshObject(mesh.Transform):

    def __init__(self, mayaNodeStr=None, nodeType='transform'):
        super(ContainterMeshObject, self).__init__(mayaNodeStr, nodeType)
        self.export_util = model_export_util.Util(self)

    def initializeAttrs(self):
        '''
        Args:
            Inherits exportPath from parent mpy_export_object ***

        Returns:
            None
        '''  
        super(ContainterMeshObject, self).initializeAttrs()
        
        self.addAttr(globals.meta.mclass_name, 
                     value=self._metaClassName(), 
                     attrType='string').set(self._metaClassName()).lock(True)

        self.addAttr(globals.meta.mclass_module, 
                     value=self._metaClassModule(), 
                     attrType='string').set(self._metaClassModule()).lock(True)
        
        self.addAttr('is_rigged', attrType='bool', value=False, channelBox=True, keyable=False)
        self.addAttr('is_static', attrType='bool', value=False, channelBox=True, keyable=False)
        self.addAttr('is_pomblend', attrType='bool', value=False, channelBox=True, keyable=False)
        self.addAttr('is_dfm', attrType='bool', value=False, channelBox=True, keyable=False)
        self.addAttr('is_collision', attrType='bool', value=False, channelBox=True, keyable=False)
        self.addAttr('base_name', attrType='string')
        
        
        self.addAttr('socket', attrType='string', value=False, channelBox=False, keyable=False)
        self.addAttr('socket_joint', attrType='message')