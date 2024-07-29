######################################
############# IMPORTS ################
######################################
import filepath
import maya.cmds as cmds
import studio.tools.content_exporter.metaclasses.mpy_export_object as mpy_export_object

# unreal globals
from unreal_tools.utils.globals import ue

######################################
############# DEFINES ################
######################################



######################################
############# CLASSES ################
######################################
class RigExportObject(mpy_export_object.ExportObject):

    def __init__(self, mayaNodeStr=None):
        super(RigExportObject, self).__init__(mayaNodeStr)

    def initializeAttrs(self):
        '''
        Args:
            Inherits exportPath from parent mpy_export_object ***

        Returns:
            None
        '''
        super(RigExportObject, self).initializeAttrs()
        self.addAttr('export_geometry', attrType='string', attrGroup='export')
        self.addAttr('_export_name', attrType='string', attrGroup='export')
        self.addAttr('_export_variant', attrType='string', attrGroup='export')

    @property
    def export_name(self):
        return self._export_name.get if self._export_name.get else None
    
    @property
    def export_variant(self):
        return self._export_variant.get if self._export_variant.get else None
    
    @property
    def export_joint(self):
        return self.rig.get.rig_joint.get.name
    
    @property
    def export_path(self):
        '''
        Concatinate the skelmesh exportpath
        '''
        export_file_path = filepath.FilePath(cmds.file(q=True, sn=True)).dir().join('Export')
        
        # construct the export file name and force to lowercase (animators request)
        export_skelmesh_name_list = [self.export_name,
                                     self.export_variant if self.export_variant else None]
        
        export_skelmesh_name = '_'.join([x for x in export_skelmesh_name_list if x])#.lower()
        
        return export_file_path.join(f'{ue.skelmesh}_{export_skelmesh_name}.{self.file_ext}')