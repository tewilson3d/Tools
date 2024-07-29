######################################
############# IMPORTS ################
######################################
import traceback
import maya.cmds as cmds

from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import loadUiType

import filepath

import meta.metaFactory as metaFactory
import studio.lib.fbxExporter as fbxExporter
import studio.tools.vehicle_manager.vehicle_manager as veh_mang
import studio.tools.content_exporter.metaclasses.mpy_modelexport_object as modelExportMetaObject

import studio.tools.content_exporter.get_rig_dialog as namespace_dialog
import studio.tools.content_exporter.get_rig_dialog as contaier_dialog



############# DEFINES ################
######################################
######################################
modelWidget_uiPath = filepath.FilePath(__file__).dir().join(__file__.replace('.py', '.ui'))
modelWidget_form_class, modelWidget_base_class = loadUiType(modelWidget_uiPath)

JSON_EXPORT_NAME = 'ExportMapping.json'


######################################
############# CLASSES ################
######################################
class ModelExportWidget(modelWidget_base_class, modelWidget_form_class): 

    TAB_NAME = 'Vehicles'

    def __init__(self, parent=None, container_objs=None):
        super(ModelExportWidget, self).__init__(parent)
        self.setupUi(self)
        
        self.get_rig_object()
        
        # Populate export list
        self.populate_container_widgets()

        # Set connections
        self.add_group_button.clicked.connect(self.add_container_node)
        self.remove_group_button.clicked.connect(self.delete_container_obj)

        self.add_geo_button.pressed.connect(self.add_export_meshes)
        self.remove_geo_button.pressed.connect(self.remove_export_meshes)

        self.container_listWidget.itemChanged.connect(self.set_selectedContainer_exportNodes)
        self.container_listWidget.clicked.connect(self.set_selectedContainer_exportNodes)

        # util buttons
        parent.setupEventHandlers(self)
        
        self.export_button.pressed.connect(self.export_mesh)

    def EVENT_import_skeleton_button_clicked(self):
        ''' reference the skeleton fbx '''
        veh_mang.load_skeleton()
    
    def EVENT_save_container_button_clicked(self):
        pass    
    
    def EVENT_tag_static_button_clicked(self):
        veh_mang.tag_static_meshes()
        
    def EVENT_tag_not_static_button_clicked(self):
        veh_mang.tag_static_meshes(False)
        
    def EVENT_tag_pomblend_button_clicked(self):
        veh_mang.tag_static_meshes(True, True)
        
    def EVENT_tag_box_collision_button_clicked(self):
        veh_mang.tag_collison_meshes(True, False)
        
    def EVENT_tag_custom_collision_button_clicked(self):
        veh_mang.tag_collison_meshes(False, True)        
        
    def EVENT_is_rigged_button_clicked(self):
        veh_mang.tag_rigged_meshes(True) 
        
    def EVENT_isnot_rigged_button_clicked(self):
        veh_mang.tag_rigged_meshes(False)         
    
    def EVENT_connect_mesh_button_clicked(self):
        veh_mang.connect_geometry()
        
    def EVENT_connect_mesh_hide_button_clicked(self):
        veh_mang.connect_geometry(False, True)        
        
    def EVENT_reconnect_mesh_button_clicked(self):
        veh_mang.reconnect_geometry()
    
    def EVENT_set_export_values_button_clicked(self):
        veh_mang.set_export_values(None, True)
        
    def EVENT_set_base_name_clicked(self):
        veh_mang.set_export_values(None, True)
        
    def EVENT_fix_export_names_button_clicked(self):
        items = self.container_listWidget.selectedItems()
        if items:
            for item in items:
                container_obj = item.data(QtCore.Qt.UserRole)        
                veh_mang.set_mesh_names(container_obj)

    def item_changed(self):
        for x in range(self.export_node_listwidget.count()):
            item = self.export_node_listwidget.item(x)
            container_obj = item.data(QtCore.Qt.UserRole)
            container_obj.export_model.set(item.text())
            container_obj.rename(item.text())
            cmds.select(container_obj.name, r=1)
            cmds.select(cl=1)

    def export_name_contextmenu(self, point):
        ''' Adds context menu for right click signals '''
        seqMenu = QtWidgets.QMenu(self)

        renameAction = QtWidgets.QAction('Select Geometry', self)
        renameAction.triggered.connect(self.select_export_geometry)

        seqMenu.addAction(renameAction)
        seqMenu.exec_(self.export_node_listwidget.mapToGlobal(point))

    def populate_container_widgets(self):
        '''
        Populate the export_node_listwidget

        Args:
            None
        Returns:
            None
        '''
        self.container_listWidget.clear()
        container_objs = self.get_contaner_list()
        self.set_container_listWidget(container_objs)

    def update_rig_metadata_node(self):
        rig_name = self.rig_name_lineedit.text()
        rig_variant = self.rig_variant_lineedit.text()

        self.rig_obj.rig_name.set(rig_name)
        self.rig_obj.rig_variant.set(rig_variant)
        # TODO: Causes AETemplate error for some reason. Investiage later.
        self.rig_obj.rename(f'{rig_name}_Rig_Metanode')

        for x in range(self.skelmesh_listwidget.count()):
            item = self.skelmesh_listwidget.item(x)
            export_obj = item.data(QtCore.Qt.UserRole)
            export_name = self._get_export_str_name(export_obj)

            # Commented out for the same naming issue mentioned above.
            export_obj.rename(f'{export_name}_RigExport_Metanode')
            item.setText(export_name)  

    def set_json_export_path(self):
        rig_file_path = filepath.ExportPath(cmds.file(q=True, sn=True)).dir()  
        self.json_path_lineedit.setText(f'{rig_file_path.join(self.rig_obj.rig_name.get)}_{JSON_EXPORT_NAME}')

    @property
    def get_rig_name(self):
        if self.rig_obj:
            rig_obj_name = [self.rig_obj.rig_name.get, self.rig_obj.rig_variant.get]
            return '_'.join([x for x in rig_obj_name if x])#.lower()
    
    def get_rig_object(self):
        '''
        determine which rig object to use when mutliple exist. Exclude referenced rig objects
        '''
        rig_objs = [rig_obj for rig_obj in metaFactory.getMetaObjectsByType(metaFactory.RIG) if not
                    cmds.referenceQuery(rig_obj.name, inr=1)]

        if rig_objs:
            if len(rig_objs) > 1:
                rig_name = namespace_dialog.RigDialog([' ']+[x.rig_name.get for x in rig_objs],
                                                      parent=self)
                result = rig_name.exec_()
        
                if result and rig_objs:
                    for rig_obj in rig_objs:
                        if rig_obj.rig_name.get == rig_name.rig_combobox.currentText():
                            self.rig_obj = rig_obj
                            break
            
            else:
                self.rig_obj = rig_objs[0]
                
        else:
            self.rig_obj = None
                
    def get_export_list(self):
        ''' return all export meta objects '''
        return metaFactory.getMetaObjectsByType(metaFactory.CONTAINER_MESH_EXPORT)

    def get_contaner_list(self):
        ''' return all export meta objects '''
        return metaFactory.getMetaObjectsByType(metaFactory.CONTAINER_EXPORT)

    def delete_container_obj(self):
        '''
        Delete all selected skel_container_obj(s)
        '''
        items = self.container_listWidget.selectedItems()
        if items:
            for item in items:
                container_obj = item.data(QtCore.Qt.UserRole)
                cmds.delete(container_obj.name)

            self.populate_container_widgets()

    def add_container_node(self):
        '''
        Create a new rigEpxortMetaObj aka. 'skelmesh'
        Args:
            None
        Returns:
            None
        '''
        # need to add name popup widget
        contaier_grp = cmds.ls(sl=True, type='transform')
        if contaier_grp:
            contaier_grp = contaier_grp[0]
            
        container_name = contaier_grp if contaier_grp else 'Temp'
        container = contaier_dialog.RigDialog(text_name=container_name,
                                              parent=self)
        result = container.exec_()

        if result:
            container_name = f'{container.name_lineedit.text()}'
        else:
            return

        # Use scene name for default value
        container_obj = modelExportMetaObject.ContainerObject(f'{container_name}')
        container_obj.rig_name.set(self.get_rig_name)
        container_obj.container_name.set(container.name_lineedit.text())
        self.set_container_listWidget(container_obj)

        # add grp export mesh objects
        if contaier_grp:
            container_obj.addConnection('export_group_node',
                                        contaier_grp, 
                                        'container',
                                        srcAttrType='message',
                                        desAttrType='message')
            
            with metaFactory.disableDefaultInit(): 
                export_meshs = [metaFactory.createMeshExportNode(m) for m in cmds.listRelatives(contaier_grp, 
                                                                                                c=True, 
                                                                                                type='transform', 
                                                                                                f=True)]
           
            self.add_export_meshes(container_obj, [m.shortName for m in export_meshs])

    def add_export_meshes(self, container_obj=None, selected=None):
        '''
        Add geo to the list
        '''
        if container_obj is None:
            if self.container_listWidget.selectedItems():
                container_obj = self.container_listWidget.selectedItems()[0].data(QtCore.Qt.UserRole)

        if selected is None:
            selected = [cur for cur in cmds.ls(sl=True, type="transform")]
            
        if selected:
            
            with metaFactory.disableDefaultInit():
                selected = [metaFactory.createMeshExportNode(s).name for s in selected]
                
            # set the message connections and str value
            for mesh in list(set(selected)):
                
                # Get current to ensure there are no dups
                meshes = container_obj.export_nodes.get
                if mesh not in [m.basename for m in meshes]:
                    container_obj.addConnection('export_nodes', 
                                                mesh, 
                                                'container',
                                                srcAttrType='messageArray',
                                                desAttrType='message')
                    
                if container_obj.export_group_node:
                    mesh_parent = cmds.listRelatives(mesh, p=True, type='transform')
                    if mesh_parent:
                        container_obj.addConnection('export_group_node', 
                                                    mesh_parent[0], 
                                                    'container',
                                                    srcAttrType='message',
                                                    desAttrType='message')                    

            container_obj.util.update_export_nodes()

            # refresh the ui
            self.export_node_listwidget.clear()
            self.set_export_listWidget(container_obj.export_meshes.get)

    def set_selectedContainer_exportNodes(self):
        '''
        Displays the export string names from the export nodes
        Args:
        Returns:☺
            None
        '''
        items = self.container_listWidget.selectedItems()
        if items:
            self.export_node_listwidget.clear()

            obj = items[0].data(QtCore.Qt.UserRole)
            export_nodes = obj.export_meshes.get
            if export_nodes:
                for node in export_nodes:
                    item = QtWidgets.QListWidgetItem()
                    item.setText(str(node))
                    if not cmds.objExists(node):
                        item.setBackground(QtCore.Qt.red)

                    self.export_node_listwidget.addItem(item) 

    def set_export_listWidget(self, export_meshs):
        '''
        Main function for adding the rigExportMeta to
        the skelmesh listWidget
        '''
        if export_meshs:
          
            self.export_node_listwidget.clear()

            for mesh in export_meshs:
                item = QtWidgets.QListWidgetItem()
                item.setData(QtCore.Qt.UserRole, str(mesh))
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                item.setText(str(mesh))

                self.export_node_listwidget.addItem(item)

    def set_container_listWidget(self, container_objs):
        '''
        Main function for adding the rigExportMeta to
        the skelmesh listWidget
        '''
        if container_objs:

            if not isinstance(container_objs, list):
                container_objs = [container_objs]

            for obj in container_objs:
                #for mesh in container_obj.export_meshes.get:
                item = QtWidgets.QListWidgetItem()
                item.setText(obj.container_name.get)
                item.setData(QtCore.Qt.UserRole, obj)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                self.container_listWidget.addItem(item)

    def remove_export_meshes(self):
        '''
        Remove Selected geo objects
        '''
        itemNameList = []
        items = self.export_node_listwidget.selectedItems()
        container_obj = self.get_selected_container_item()
        export_node_lsit = container_obj.export_nodes.get

        if items:

            export_meshes = container_obj.export_meshes.get

            for item in items:
                mesh = items.data(QtCore.Qt.UserRole)

                export_meshes.pop(mesh)
                meshes = [cur for cur in export_node_lsit if cur not in itemNameList]
                container_obj.export_meshes.set(meshes)

    def remove_export_meshes(self):
        '''
        Remove Selected geo objects
        '''
        items = self.export_node_listwidget.selectedItems()
        container_obj = self.get_selected_container_item()
        export_meshes = container_obj.export_meshes.get


        if items:

            for item in items:
    
                mesh = item.text()
                export_meshes.remove(mesh)
                container_obj.export_meshes.set(export_meshes)
                
            self.set_export_listWidget(export_meshes)

    def get_selected_container_item(self):
        return self.container_listWidget.currentItem().data(QtCore.Qt.UserRole)

    def get_selected_export_item(self):
        return self.export_node_listwidget.currentItem().data(QtCore.Qt.UserRole)    

    def select_export_geometry(self):
        # select the geo from the export node
        export_node = self.get_selected_export_item()
        cmds.select(export_node.export_geometry.get, r=1)

    def export_mesh(self):
        '''
        Main export function, walks through all AnimExportMetaNodes
        and deteremines if they export.

        Will checkout, ToDo , add files to the changelist where the
        source files live.

        Args:
            None
        Returns:
            None
        '''
        # clean any blinddta
        blinddata = cmds.ls(type='blindDataTemplate')
        if blinddata:
            cmds.delete(blinddata)
            
        # reset button color
        self.set_export_button_color(None)
        selItems = self.container_listWidget.selectedItems()

        if not selItems:
            return

        for item in selItems:
            container_obj = item.data(QtCore.Qt.UserRole)

            # Get export object list.
            if container_obj.export_meshes.get:

                # iterate through
                #if geomerty list is selected:
                export_meshes = []
                items = self.export_node_listwidget.selectedItems()
                if items:
                    for item in items:
                        m = item.text()
                        export_meshes.append(metaFactory.createMeshExportNode(m))
                
                else:
                    export_meshes = container_obj.export_nodes.get
            
                if export_meshes:
                    for mesh in export_meshes:

                        # zero out the mesh transform
                        export_file_path = container_obj.export_path.join([f'{mesh.shortName}.{container_obj.file_ext}']).asMayaPath()

                        try:
                            # zero out the mesh values to zero
                            mesh.util.setDefaultValues()
                            if mesh.is_rigged.get:
                                mesh.rotate.set([-90,0,0]) #big stupid hack
                            
                            # Export
                            fbxExporter.export(mesh.name,
                                               export_file_path,
                                               saveSourceControl=True)
                            
                        except Exception(e):
                            # Set Button to fail and raise expection
                            self.set_export_button_color(False)
                            print(f'Error during export to {x}\n{y}',
                                  x=container_obj.export_meshes.get,
                                  y=traceback.format_exc(e))
                            
                        finally:
                            # set the mesh back to bind pose
                            mesh.setMatrix(mesh.bind_pose.get)
                            
                            
        self.set_export_button_color(True)

    def set_export_button_color(self, successfull):
        '''
        Colors the export wigdet to communictae result
        '''
        if successfull is None:
            self.export_button.setStyleSheet("text-align: center; color: black; font: bold 14px; background-color: rgb(0,174,220);")
        elif successfull:
            self.export_button.setStyleSheet("text-align: center; color: white; font: bold 14px; background-color: rgb(98,150,39);")
        else:
            self.export_button.setStyleSheet("text-align: center; color: white; font: bold 14px; background-color: rgb(237,28,36);")