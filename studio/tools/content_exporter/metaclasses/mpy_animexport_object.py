######################################
############# IMPORTS ################
######################################
import filepath
import maya.cmds as cmds
import studio.tools.content_exporter.metaclasses.mpy_rigexport_object as mpy_rig_object

# unreal globals
from unreal_tools.utils.globals import ue

######################################
############# CLASSES ################
######################################
class AnimExportObject(mpy_rig_object.RigExportObject):

    def __init__(self, mayaNodeStr=None):
        super(AnimExportObject, self).__init__(mayaNodeStr)

    def initializeAttrs(self):
        '''
        Args:
            animation_layers (string)
            start_frame (int)
            end_frame (int)

            *** Inherits exportPath from parent ExportMetaObject ***

        Returns:
            None
        '''
        super(AnimExportObject, self).initializeAttrs()

        # Export values to be passed to the exporter
        self.addAttr('export_rig_name', attrType='string', attrGroup='export')
        self.addAttr('export_rig_variant', attrType='string', attrGroup='export')
        self.addAttr('export_clip_name', attrType='string', attrGroup='export')
        self.addAttr('export_start_frame', attrType='int', attrGroup='export')
        self.addAttr('export_end_frame', attrType='int', attrGroup='export')
        self.addAttr('export_namespace', attrType='string', attrGroup='export')
        self.addAttr('rig', attrType='message', attrGroup='export')
        
        # Maya uses
        self.addAttr('export_layers', attrType='string', value=None)

    @property
    def export_path(self):
        '''
        Concatinate the skelmesh exportpath
        '''
        # export path should be constructed with character name vs full scene path
        # i.e path + char anim defined in the rig meta object,
        export_file_path = filepath.FilePath(cmds.file(q=True, sn=True)).dir().join('Export')
        
        # construct the export file name and force to lowercase (animators request)
        export_seq_name_list = [self.export_rig_name.get,
                                self.export_rig_variant.get if self.export_rig_variant.get else None,
                                self.export_clip_name.get]
        
        export_seq_name = '_'.join([x for x in export_seq_name_list if x])#.lower()
        
        return export_file_path.join(f'{ue.sequence}_{export_seq_name}.{self.file_ext}')
    