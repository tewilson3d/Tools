######################################
############# IMPORTS ################
######################################
from unreal_tools.utils.globals import ue


######################################
############# CLASSES ################
######################################
class Util(object):

    def __init__(self, controlObj):
        '''
        Control Class Object
        Args:
            mayaNodeStr (str): joint name
        Returns:
            None
        '''
        self._parentObj = controlObj
    
    def fix_socket_connection(self):
        '''
        Updates the string attr from the message connections
        this is too try and ensure things can alwasys be exported
        to try and speed up export times with out havign to delcare the objects
        this may not even be nessacry
        '''
        if not self._parentObj.socket.get:
            if self._parentObj.socket_joint.get:
                self._parentObj.socket.set(self._parentObj.socket_joint.get.basename)
        
        else:
            if self._parentObj.socket.get:
                if self._parentObj.socket_joint.get:
                    self._parentObj.addConnection('socket_joint',  
                                                  self._parentObj.socket.get, 
                                                  'export_mesh' ,
                                                  srcAttrType='message',
                                                  desAttrType='messageArray',)
    def update_export_nodes(self):
        '''
        Updates the string attr from the message connections
        this is too try and ensure things can alwasys be exported
        to try and speed up export times with out havign to delcare the objects
        this may not even be nessacry
        '''
        if self._parentObj.export_nodes:
            meshes  = self._parentObj.export_nodes.get
            self._parentObj.export_meshes.set([m.shortName for m in meshes])
    
    def rename(self, is_rigged=True, use_container=True):
    
        if self._parentObj.is_rigged.get is False:
            if self._parentObj.container_name and use_container:
                
                if self._parentObj.is_pomblend.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.container_name.get}_{self._parentObj.shortName}__{ue.pomblend}') 
                elif self._parentObj.is_static.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.container_name.get}_{self._parentObj.shortName}')      
                else:
                    self._parentObj.rename(f'{ue.nanite}_{self._parentObj.container_name.get}_{self._parentObj.shortName}')
            else:
                if self._parentObj.is_pomblend.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.shortName}__{ue.pomblend}')               
                
                elif self._parentObj.is_static.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.shortName}')               
                else:
                    self._parentObj.rename(f'{ue.nanite}_{self._parentObj.shortName}')
        
        else:
            if self._parentObj.container_name and use_container:
                if self._parentObj.is_pomblend.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.container_name.get}__{ue.pomblend}__{self._parentObj.socket.get}')      
                elif self._parentObj.is_static.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.container_name.get}__{self._parentObj.socket.get}')      
                else:
                    self._parentObj.rename(f'{ue.nanite}_{self._parentObj.container_name.get}__{self._parentObj.socket.get}')
            else:
                if self._parentObj.is_pomblend.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.base_name.get}__{ue.pomblend}__{self._parentObj.socket.get}')                               
                elif self._parentObj.is_static.get:
                    self._parentObj.rename(f'{ue.staticmesh}_{self._parentObj.base_name.get}__{self._parentObj.socket.get}')               
                else:
                    self._parentObj.rename(f'{ue.nanite}_{self._parentObj.base_name.get}__{self._parentObj.socket.get}')
    