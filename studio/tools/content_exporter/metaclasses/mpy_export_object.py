######################################
############# IMPORTS ################
######################################
import filepath
import maya.cmds as cmds
import meta.classes.mpy_object as mpy_object

######################################
############# CONSTANT ###############
######################################
EXPORT_FILE_EXT = 'fbx'
NANITE_FOLDER = 'Nanite'
STATIC_FOLDER = 'Static'

######################################
############# CLASSES ################
######################################
class ExportObject(mpy_object.MPyDgNode):

    def __init__(self, mayaNodeStr=None):
        super(ExportObject, self).__init__(mayaNodeStr)
        self.file_ext = EXPORT_FILE_EXT

    def initializeAttrs(self):
        '''
        ExportMetaObject initializeAttrs additions added to 
        MetaObject.initializeAttrs

        Args:
            exportPath (string): for specific path (Not need now)

        Returns:
            None
        '''
        super(ExportObject, self).initializeAttrs()
        
        # Rig object, for now message attr
        self.addAttr('rig', attrType='message', attrGroup='export')
        
        # Gets exported bool
        self.addAttr('export', attrType='bool', value=True, attrGroup='export')
        
        
        # unreal stuff

    @property
    def export_name(self):
        return self.rig.get.rig_name.get if self.rig.get else None
    
    @property
    def export_variant(self):
        return self.rig.get.rig_variant.get if self.rig.get else None

    @property
    def export_path(self):
        '''
        Concatinate the skelmesh exportpath
        '''
        return filepath.FilePath(cmds.file(q=True, sn=True)).dir().join('Export')
    
    def get_attr_by_group(self, attrGrpStr='export'):
        attrs = []
        for attr in self._attributes:
            if self.attrGroup.get == attrGrpStr:
                attrs.append(self._attributes[attr])
                
            if attrs:
                return attrs