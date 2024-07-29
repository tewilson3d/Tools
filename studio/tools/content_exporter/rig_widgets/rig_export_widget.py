######################################
############# IMPORTS ################
######################################
import os
import traceback
import maya.cmds as cmds

from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import loadUiType

import filepath

import rigging.globals as globals
#import rigging.lib.components.createRig as createRig
import meta.metaFactory as metaFactory
import studio.lib.fbxExporter as fbxExporter
import rigging.lib.joint_utils as jnt_utils
import studio.tools.content_exporter.metaclasses.mpy_rigexport_object as rigExportMetaObject

import studio.tools.content_exporter.get_rig_dialog as namespace_dialog


############# DEFINES ################
######################################
######################################
rigWidget_uiPath = filepath.FilePath(__file__).dir().join(__file__.replace('.py', '.ui'))
rigWidget_form_class, rigWidget_base_class = loadUiType(rigWidget_uiPath)

RIG_TYPE = ['None', '1P', '3P']


######################################
############# CLASSES ################
######################################
class RigExportWidget(rigWidget_base_class, rigWidget_form_class): 

    TAB_NAME = 'Rigging'

    def __init__(self, parent=None, skel_export_objs=None):
        super(RigExportWidget, self).__init__(parent)
        self.setupUi(self)
        self.parent_window = parent
        
        # hide the output info window for now
        self.create_rig_frame.setVisible(False)

        # This should not be editable since the paths gets rebuilt during export
        self.export_path_lineedit.setEnabled(False)

        # meta objects, pull rig object from parent 
        self.create_rigmeta_buttton.pressed.connect(self.create_rig_object)
        
        self.get_rig_object()

        if not self.rig_obj:
            self.create_rig_frame.setVisible(True)
            self.export_frame.setVisible(False)
            return

        # Set up listWidgets
        self.skelmesh_listwidget.itemPressed.connect(self.set_do_export_bool)
        self.skelmesh_listwidget.itemSelectionChanged.connect(self.set_do_export_bool)
        self.create_rigmeta_buttton.pressed.connect(self.create_rig_object)
        
        # Skeleton listwidget buttons
        self.add_export_button.pressed.connect(self.add_export_obj)
        self.remove_export_button.pressed.connect(self.delete_export_obj)
        self.export_button.pressed.connect(self.export_skelmesh)
        self.set_export_button_color(None)

        # Rename contextmenu
        self.skelmesh_listwidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.skelmesh_listwidget.customContextMenuRequested.connect(self.export_name_contextmenu)        

        # Geometry listWidget buttons
        self.add_geo_button.pressed.connect(self.add_export_geo)
        self.remove_geo_button.pressed.connect(self.remove_export_geo)
        
        # populate the skelmesh listwidget
        self.set_export_list_widget()
        
        # Update rig metat data information on ui
        self.update_export_name_variant()
        self.rig_name_lineedit.textChanged.connect(self.update_export_name_variant_node)
        self.rig_variant_lineedit.textChanged.connect(self.update_export_name_variant_node)
        
    def update_export_name_variant(self):
        if self.get_selected_export_data():
            export_obj, _ = self.get_selected_export_data()
            self.rig_name_lineedit.setText(export_obj.export_name)
            self.rig_variant_lineedit.setText(export_obj.export_variant)
    
    def update_export_name_variant_node(self):
        rig_name = self.rig_name_lineedit.text()
        rig_variant = self.rig_variant_lineedit.text()

        if self.get_selected_export_data:

            export_obj, item = self.get_selected_export_data()
            export_obj._export_name.set(rig_name)
            export_obj._export_variant.set(rig_variant)            
            export_name = self._get_export_str_name(export_obj)
            
            # Commented out for the same naming issue mentioned above.
            export_obj.rename(f'{export_name}_RigExport_Metanode')
            item.setText(export_name)

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

    def create_rig_object(self):
        '''
        if rig meta data node doesn't exists, create a default one. This is to avoid having to rebuild the rig just to
        create rig metadata 

        Returns
        -------
        Rig(mpy_object.MPyDgNode)
        '''
        root_joint = globals.rig.root_joint
        top_joint = jnt_utils.getHighestLevelJoints(True)
        if not cmds.objExists(root_joint):
            root_joint = top_joint
            
        rig_objs = metaFactory.getMetaObjectsByType(metaFactory.RIG)
        
        if rig_objs:
            self.rig_obj = rig_objs[0]
        else:
            if not rig_objs and cmds.objExists(root_joint):
                self.rig_obj = metaFactory.createRigNode(f'{root_joint}_Rig_Metanode')
        
                sn = cmds.file(q=1, sn=1)
                basename = os.path.basename(sn).split(".")[0].replace("_Rig", "")
                self.rig_obj.rig_name.set(basename)
                self.rig_obj.addConnection(attrStrName='rig_joint',
                                      inputObj=root_joint,
                                      inputAttrStrName='rig_metanode',
                                      srcAttrType='message',
                                      desAttrType='message')

                self.create_rig_frame.setVisible(False)
                self.export_frame.setVisible(True)
                
                self.parent_window.relaunch_window(True)
                
    def get_export_list(self):
        ''' return all export meta objects excluding referenced'''
        return [meta_obj for meta_obj in metaFactory.getMetaObjectsByType(metaFactory.RIG_EXPORT) if not
        cmds.referenceQuery(meta_obj.name, inr=1)]

    def get_selected_export_data(self):
        '''
        Returns the selected skelmesh item
        Args:
            None
        Returns:
            RigExportMetaObj: (RigExportMetaData)
        '''
        items = self.skelmesh_listwidget.selectedItems()
        if items:
            export_obj = items[0].data(QtCore.Qt.UserRole)
            return export_obj, items[0]
        
        return None

    def set_do_export_bool(self):
        ''' 
        Main function to decide what rigExportMeta objects
        get exported.

        Also displays the geometry info for the given skelmesh
        '''
        items = self.skelmesh_listwidget.selectedItems()
        export_list = self.get_export_list()
        
        if items:

            # If a single one is selcted show the
            # geomerty in the geometry_listwidget
            if len(items) == 1:
                export_obj, _ = self.get_selected_export_data()
                export_obj.export.set(True)

                # if items is selected then set export flag
                for rObj in export_list:
                    if rObj.export_name != export_obj.export_name:
                        rObj.export.set(False)

                # Display the geo string names
                self.set_geometry_list_widget(export_obj)
                
                # update the name/variant ui elements
                self.update_export_name_variant()
                self.export_path_lineedit.setText(export_obj.export_path)                  

            # If mult select turn off export flag
            elif len(items) != len(export_list):
                selItemObjs = []
                for item in items:
                    selItemObjs.append(item.data(32))

                for export_obj in export_list:
                    if export_obj not in selItemObjs:
                        export_obj.export.set(False)
                    else:
                        export_obj.export.set(True)

                self.geometry_listwidget.clear()

            else:
                for export_obj in export_list:
                    export_obj.export.set(True)

                self.geometry_listwidget.clear()

        # Clear all data
        else:
            self.geometry_listwidget.clear()
            for rObj in export_list:
                rObj.doExport = False
            
            # update export path textfild
            self.export_path_lineedit.setText('Nothing Selected') 

    def _get_export_str_name(self, export_obj):
        '''
        Returns the export string name from all valid entries
        '''
        export_name_list = [#export_obj.export_type.get,
                            export_obj.export_name,
                            export_obj.export_variant]
        return '_'.join([x for x in export_name_list if x])
        
    def _add_skeleton_item(self, skel_export_obj):
        '''
        Main function for adding the rigExportMeta to
        the skelmesh listWidget
        '''
        # get string name
        export_name = self._get_export_str_name(skel_export_obj)
        
        item = QtWidgets.QListWidgetItem()
        item.setData(QtCore.Qt.UserRole, skel_export_obj)
        item.setText(export_name)
        self.skelmesh_listwidget.addItem(item)

        if skel_export_obj.export.get:
            self.skelmesh_listwidget.setCurrentItem(item)

    def validate_rig_data(self):
        '''
        Validates the skinning and mesh data
        '''
        pass

    def validate_geo(self):
        '''
        Populates the skelmesh obj geometry list
        '''
        selItems = self.skelmesh_listwidget.selectedItems()

        if selItems:
            parentObj = selItems[0].data(32)

            rigObj = parentObj.parent
            rigObj.storeRigGeometry            

            for item in selItems:
                skel_export_obj = item.data(QtCore.Qt.UserRole)
                skel_export_obj.exportGeometry = rigObj.geometry

    def set_export_list_widget(self):
        '''
        Populate the skelmesh_listwidget

        Args:
            None
        Returns:
            None
        '''
        self.skelmesh_listwidget.clear()
        export_objs = self.get_export_list()
        
        # Pull the rigObj and list its children
        if export_objs:
            for export_obj in export_objs:
                self._add_skeleton_item(export_obj)
                
                # update the ui
                self.export_path_lineedit.setText(export_obj.export_path)
                
        # Create rigexport metanode if none exists
        else:
            self.add_export_obj()

    def set_geometry_list_widget(self, skel_export_obj):
        '''
        Displays the geo string names from the metaObj
        Args:
            skel_export_obj (RigExportMetaData):
        Returns:
            None
        '''
        self.geometry_listwidget.clear()

        if skel_export_obj.export_geometry.get:
            for geo in skel_export_obj.export_geometry.get:
                item = QtWidgets.QListWidgetItem()
                item.setText(str(geo))
                if not cmds.objExists(geo):
                    item.setBackground(QtCore.Qt.red)  

                self.geometry_listwidget.addItem(item)

    def add_export_obj(self):
        '''
        Create a new rigEpxortMetaObj aka. 'skelmesh'
        Args:
            None
        Returns:
            None
        '''
        # Get the rig object
        if not self.rig_obj:
            self.get_rig_object()

        if self.rig_obj:
            if self.rig_obj.rig_name.get == None:
                export_obj_neme = self.rig_obj.name
            else:
                export_obj_neme = self.rig_obj.rig_name.get
        
            export_obj = rigExportMetaObject.RigExportObject(f'{export_obj_neme}_RigExport_Metanode')
    
            # Create connection with the rig_obj
            export_obj.addConnection('rig',
                                     self.rig_obj,
                                     'rig_export_nodes',
                                     'message',
                                     'messageArray')
            
            # Set rig export meta data
            self.set_export_meta_data(export_obj)
    
            # add to listwidget
            self._add_skeleton_item(export_obj)

    def set_export_meta_data(self, export_obj):
        '''
        Export meta data
        '''
        if self.rig_obj.rig_joint.get.skinCluster:
            export_obj.export_geometry.set([s.geometry.name for s in self.rig_obj.rig_joint.get.skinCluster])
        else:
            cmds.warning("Can't find skin cluster on %s. Skipped generating export geometry list!"%self.rig_obj.rig_joint.get.name)
    
        # set export names
        export_obj._export_name.set(self.rig_obj.rig_name.get)
        export_obj._export_variant.set(self.rig_obj.rig_variant.get)
        
        # get export str name
        export_name = self._get_export_str_name(export_obj)
        
        # set the meta export object name
        export_obj.rename(f'{export_name}_RigExport_Metanode')
    
    def delete_export_obj(self):
        '''
        Delete all selected skel_export_obj(s)
        '''
        items = self.skelmesh_listwidget.selectedItems()
        if items:
            for item in items:
                rObj = item.data(QtCore.Qt.UserRole)
                cmds.delete(rObj.name)

            self.set_export_list_widget()

    def add_export_geo(self):
        '''
        Add geo to the list
        '''
        export_obj, _ = self.get_selected_export_data()
        export_objGeoList = export_obj.export_geometry.get

        if not export_objGeoList:
            export_objGeoList = []

        selected = cmds.ls(sl=True)

        if selected:
            for sel in selected:
                if export_objGeoList and sel in export_objGeoList:
                    continue
                export_objGeoList.append(sel)

            export_obj.export_geometry.set(export_objGeoList)
            
            # refresh the ui
            self.set_geometry_list_widget(export_obj)

    def remove_export_geo(self):
        '''
        Remove Selected geo objects
        '''
        itemNameList = []
        selected_meshes = cmds.ls(sl=True)
        items = self.geometry_listwidget.selectedItems()
        export_obj, _ = self.get_selected_export_data()
        export_objGeoList = export_obj.export_geometry.get

        if items or selected_meshes:
            if items:
                itemNameList.extend([item.text() for item in items])
                
            if selected_meshes:
                itemNameList.extend(selected_meshes)
            
            export_obj.export_geometry.set(self._remove_geo_items(itemNameList, 
                                                                  export_objGeoList))
            self.set_geometry_list_widget(export_obj)

    def _remove_geo_items(self, selItemList, export_objGeoList):
        '''
        Returns the given list with selItems removed

        Args:
            selItemList (list (str))
            export_objGeoList (List (str))
        Returns:
            export_objGeoList (list (str))
        '''
        for selItem in selItemList:
            for i, name in enumerate(export_objGeoList):
                if selItem == name:
                    export_objGeoList.pop(i)

        return export_objGeoList

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

    def export_skelmesh(self):
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
        
        # reset button color
        self.set_export_button_color(None)
        selItems = self.skelmesh_listwidget.selectedItems()

        if not selItems:
            return

        for item in selItems:
            export_obj = item.data(QtCore.Qt.UserRole)
            if not export_obj.export.get:
                continue

            # Get export object list.
            exportStrList = []
            exportStrList.append(export_obj.export_joint)
            exportStrList.extend([geo for geo in export_obj.export_geometry.get])

            try:
                # Export
                fbxExporter.export(exportStrList, export_obj.export_path.asMayaPath(), saveSourceControl=True)
                self.set_export_button_color(True)

            except Exception(e):
                # Set Button to fail and raise expection
                self.set_export_button_color(False)
                f'Error during export to {export_obj.export_geometry.get,}\n{traceback.format_exc(e)}'