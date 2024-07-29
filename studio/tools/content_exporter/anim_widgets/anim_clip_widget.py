######################################
############# IMPORTS ################
######################################
from functools import partial

import maya.cmds as cmds

from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtGui
from pyside.qt_wrapper import QtWidgets

import filepath
import animation.lib.timeSlider as time_slider
import animation.lib.animLayer as animLayer
import meta.metaFactory as metaFactory

import studio.tools.content_exporter.get_rig_dialog as namespace_dialog


######################################
############# DEFINES ################
######################################
icon_path = filepath.FilePath(__file__).dir().dir().join('icons')
TO_EXPORT = icon_path.join('checkedIcon.bmp')
NOT_EXPORT = icon_path.join('uncheckedIcon.bmp')


######################################
############# CLASSES ################
######################################
class PushButton(QtWidgets.QPushButton):

    def __init__(self, parent=None, size=None):
        super(PushButton, self).__init__(parent)
        self.showMenu = False
        self.pButtonMenu = QtWidgets.QMenu()
        self.setStyleSheet("text-align: center; color: white; font: bold 14px;")

        # Set min and max size
        self.setMaximumHeight(40)
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)

    def addContextMenu(self, contextMenu):
        self.showMenu = True
        self.pButtonMenu = contextMenu

class SpinBox(QtWidgets.QSpinBox):

    def __init__(self, parent=None, size=None):
        super(SpinBox, self).__init__(parent)
        self.setMaximum(10000)
        self.setMinimum(0)

        # Set min and max size
        self.setMaximumHeight(40)
        self.setMinimumWidth(size)
        self.setMaximumWidth(size)
        self.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

class Icon(QtGui.QIcon):

    def __init__(self, iconFile, parent=None):
        super(Icon, self).__init__(parent)
        self.addFile(iconFile)

class AnimClipBox(QtWidgets.QWidget):

    def __init__(self, animExportMetaObj, parent=None, fill_data=False):
        '''
        Args:
            file_data(bool): populates the anim export obj properties
        '''
        super(AnimClipBox, self).__init__(parent)

        # define meta object
        self.animExportObj = animExportMetaObj
    
        # set the parent
        self.parent_window = parent

        # create buttons
        self.do_export_button     = PushButton(size=50)
        self.rig_namespace_button = PushButton(size=85)
        self.clip_name_lineedit   = QtWidgets.QLineEdit()
        self.anim_layer_button    = PushButton(size=100) 
        self.start_frame_spinebox = SpinBox(size=50)
        self.end_frame_spinbox    = SpinBox(size=50)
        self.loop_button          = PushButton(size=50)

        # set rig meta object
        self._rig = None
        self.set_rig_data(self.animExportObj)
        
        # if no rig is found  show hoting
        # should show A dialog here future
        if self._rig is None:
            return
        
        # if the the clip is new ppoluate default data
        if fill_data or self.animExportObj.export_rig_name.get == None:
            self.set_clip_data()        
        
        # button popup menu items
        self.exportButtonMenu = QtWidgets.QMenu()
        self.anim_layer_buttonMenu = QtWidgets.QMenu()

        # layout that supports the button and visiblity
        self.anim_clip_boxLayout = QtWidgets.QHBoxLayout()
        self.vMain_boxlayout = QtWidgets.QVBoxLayout(self)

        # clip boxlayout
        self.anim_clip_boxLayout.setSpacing(0)
        self.anim_clip_boxLayout.setContentsMargins(0,0,0,0)

        # set the icons - move this to its own
        self.checkedIcon   = Icon(TO_EXPORT)
        self.uncheckedIcon = Icon(NOT_EXPORT)

        # set button variables        
        self.vMain_boxlayout.setSpacing(0)
        self.vMain_boxlayout.setContentsMargins(0,0,0,0)

        # do export button
        self.do_export_button.setIcon(self.checkedIcon)
        # signal
        self.do_export_button.pressed.connect(partial(self.toggle_export_button, 
                                                      self.do_export_button, 'export'))

        self.rig_namespace_button.setText(self.get_namespace())
        # signal
        self.rig_namespace_button.pressed.connect(lambda : self.set_rig_data())

        # clip name textfield
        self.clip_name_lineedit.setMaximumWidth(320)
        self.clip_name_lineedit.setMinimumWidth(320)
        self.clip_name_lineedit.setMinimumHeight(30)
        self.clip_name_lineedit.setAlignment(QtCore.Qt.AlignCenter)
        self.clip_name_lineedit.setStyleSheet("color: white; font: bold 14px;")
        self.clip_name_lineedit.setText(self.animExportObj.export_clip_name.get)
        # signal
        self.clip_name_lineedit.textChanged.connect(self.set_clip_name)

        # animlayer button
        self.set_animlayer_button_color()
        # signal
        self.anim_layer_button.pressed.connect(self.set_active_animlayers)

        # start frame spinbox
        self.start_frame_spinebox.setValue(self.animExportObj.export_start_frame.get)
        # signal
        self.start_frame_spinebox.valueChanged.connect(self.set_start_frame)

        # end frame spinbox
        self.end_frame_spinbox.setValue(self.animExportObj.export_end_frame.get)
        # signal
        self.end_frame_spinbox.valueChanged.connect(self.set_end_frame) 

        # looping checkbox
        self.loop_button.setIcon(self.uncheckedIcon)        

        # Set up widgets signals
        self.clip_name_lineedit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.clip_name_lineedit.customContextMenuRequested.connect(self.clip_name_contextmenu)

        self.anim_layer_button.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.anim_layer_button.customContextMenuRequested.connect(self.animlayer_button_contextmenu)        

        # setting export icon
        if self.animExportObj.export.get is False:
            self.do_export_button.setIcon(self.uncheckedIcon)
        else:
            self.do_export_button.setIcon(self.checkedIcon)

        #add widgets
        self.anim_clip_boxLayout.addWidget(self.do_export_button)
        self.anim_clip_boxLayout.addWidget(self.rig_namespace_button)
        self.anim_clip_boxLayout.addWidget(self.clip_name_lineedit)
        self.anim_clip_boxLayout.addWidget(self.anim_layer_button)    
        self.anim_clip_boxLayout.addWidget(self.start_frame_spinebox)
        self.anim_clip_boxLayout.addWidget(self.end_frame_spinbox)
        self.anim_clip_boxLayout.addWidget(self.loop_button)
        self.vMain_boxlayout.addLayout(self.anim_clip_boxLayout)
        
        # Populate export path lineedit in parent window
        self.parent_window.export_path_lineedit.setText(self.get_relative_gamepath())         
    
    def get_namespace(self):
        if not self._rig.isReferenced():
            return ':'
        return cmds.referenceQuery(self._rig.name, ns=1)
    
    def get_rig_fullname(self, rig_obj):
        return ":".join([cmds.referenceQuery(rig_obj.name, ns=1), rig_obj.rig_name.get])
    
    def clip_name_contextmenu(self, point):
        ''' Adds context menu for right click signals '''
        seqMenu = QtWidgets.QMenu(self)

        deleteAction = QtWidgets.QAction('Delete Clip', self)
        deleteAction.triggered.connect(self.delete_clip)
        seqMenu.addAction(deleteAction)
        
        renameCharAction = QtWidgets.QAction('Rename Character Name', self)
        renameCharAction.triggered.connect(self.rename_character_name)
        seqMenu.addAction(renameCharAction)
        
        renameVariantAction = QtWidgets.QAction('Rename Character Varianr', self)
        renameVariantAction.triggered.connect(self.rename_character_variant)
        seqMenu.addAction(renameVariantAction)
        
        seqMenu.exec_(self.clip_name_lineedit.mapToGlobal(point))            

    def animlayer_button_contextmenu(self, point):
        ''' Adds context menu for right click signals '''
        layerMenu = QtWidgets.QMenu(self)

        setlayerAction = QtWidgets.QAction('Set Active Layers', self)
        setlayerAction.triggered.connect(self.set_animlayers)

        resetAction = QtWidgets.QAction('Reset All Layers', self)
        resetAction.triggered.connect(self.reset_active_animlayers)

        layerMenu.addAction(setlayerAction)
        layerMenu.addSeparator()
        layerMenu.addAction(resetAction)

        layerMenu.exec_(self.anim_layer_button.mapToGlobal(point)) 

    def get_relative_gamepath(self):
        # TO DO  need to figure out
        if self.animExportObj:
            return self.animExportObj.export_path

    def set_clip_data(self):
        '''
        Populate all meta attributes
        '''
        # derive the clip name from scene
        maya_scene_name = filepath.FilePath(cmds.file(q=True, sn=True))
        rig_variant_name = f'{self._rig.rig_name.get}_{self._rig.rig_variant.get}_'#.lower()
        clip_name = maya_scene_name.getBaseFileName().replace(f'{rig_variant_name}', '')
        self.clip_name_lineedit.setText(clip_name)
        
        # anim layers
        self.set_active_animlayers()
        
        # timeline edit
        self.animExportObj.export_start_frame.set(int(time_slider.startTime()))
        self.animExportObj.export_end_frame.set(int(time_slider.endTime()))

        # connect to rig object
        self.animExportObj.addConnection('rig',
                                        self._rig, 
                                        'anim_export_objs',
                                        srcAttrType='message',
                                        desAttrType='messageArray')
        
        # rename the anim clip meta object
        self.set_clip_name()

    def set_clip_name(self):
        '''
        sets the anim clip name
        '''
        self.animExportObj.export_rig_name.set(self._rig.rig_name.get)
        self.animExportObj.export_rig_variant.set(self._rig.rig_variant.get)
        self.animExportObj.export_clip_name.set(self.clip_name_lineedit.text())
        self.animExportObj.rename(f'{self.animExportObj.export_rig_variant.get}_{self.animExportObj.export_clip_name.get}_AnimExport')
        
        self.set_clip_widget_data()

    def set_clip_widget_data(self):
        '''
        populats all the wdiget info from the export object
        '''
        # get from dynamic prop
        self.clip_name_lineedit.setText(self.animExportObj.export_clip_name.get)
        
        # class inhertited prop
        self.rig_namespace_button.setText(self.get_namespace())
        
        # class dynamic prop
        self.start_frame_spinebox.setValue(self.animExportObj.export_start_frame.get)
        self.end_frame_spinbox.setValue(self.animExportObj.export_end_frame.get)
        
        # Populate export path lineedit in parent window
        self.parent_window.export_path_lineedit.setText(self.get_relative_gamepath())
    
    def set_rig_data(self, export_obj=None):
        '''
        Needs further thought 
        '''
        #if export_obj:
            #self._rig = export_obj.rig.get
        
        #else:
        # get the rig meta node based from namespace
        rig_objs = metaFactory.getMetaObjectsByType(metaFactory.RIG)

        if rig_objs:
            if len(rig_objs) > 1:
                if not self.animExportObj.rig.get:
                    combobox_items = [' ']
                    combobox_items += [x.rig_variant.get for x in rig_objs]
                    rig_name = namespace_dialog.RigDialog(combobox_items=combobox_items,
                                                          parent=self.parent_window)
                    result = rig_name.exec_()
                    
                    if result:
                        if rig_objs:
                            for rig_obj in rig_objs:
                                full_path = rig_obj.rig_variant.get
                                current_item = rig_name.rig_combobox.currentText()
                                if full_path == current_item:
                                    self._rig = rig_obj
                else:
                    self._rig = self.animExportObj.rig.get
    
            else:
                self._rig = rig_objs[0]

            # Connect the rig object to the anim export object
            self.animExportObj.addConnection('rig',
                                             self._rig,
                                             'anim_export_nodes',
                                             'message',
                                             'messageArray')
                
            # populate the button
            self.rig_namespace_button.setText(f':{self._rig.rig_variant.get}')
            
            metaFactory.createMetaNodeSelectionSet()

    def set_animlayers(self):
        '''
        Clears the active animLayers
        Args:
            None
        Returns:
            None
        '''
        activeAnimLayers = animLayer.getAllActiveLayers()
        if activeAnimLayers:
            self.animExportObj.export_layers.set([l.name for l in activeAnimLayers])

        else:
            self.animExportObj.export_layers.set(None)

        # Change the button display
        self.set_animlayer_button_color()

    def set_animlayer_default(self):
        '''
        Clears the animLayers
        Args:
            None
        Returns:
            None
        '''
        self.animExportObj.export_layers.get = None
        self.set_animlayer_button_color()

    def set_animlayer_button_color(self):
        '''
        Set the color and text for animlayer but
        Args:
            None
        Returns:
            None
        '''
        if self.animExportObj.export_layers.get:
            self.anim_layer_button.setStyleSheet("text-align: center; color: black; font: bold 14px; background-color: rgb(0,174,239);")
            self.anim_layer_button.setText(str(len(self.animExportObj.export_layers.get)))
        else:
            self.anim_layer_button.setStyleSheet("text-align: center; color: white;")
            self.anim_layer_button.setText('--None--')

    def set_clip_framerange(self):
        '''
        Frame the time line to animExportObj start and end frame
        '''
        time_slider.setStartEndTime(self.animExportObj.export_start_frame, 
                                    self.animExportObj.export_end_framee)
        cmds.currentTime(self.animExportObj.export_start_frame)

    def delete_clip(self):
        '''
        Deletes the animSeq
        Args:
            None
        Returns:
            None
        '''        
        cmds.delete(self.animExportObj.name)
        self.parent_window.export_path_lineedit.setText('Nothing To Export')
        self.deleteLater()
        
    def rename_character_name(self):
        rig_name = namespace_dialog.RigDialog(text_name=self.animExportObj.export_rig_name.get,
                                              parent=self.parent_window)
        result = rig_name.exec_()
        
        if result:
            self.animExportObj.export_rig_name.set(rig_name.name_lineedit.text())
        self.set_clip_widget_data()
    
    def rename_character_variant(self):
        rig_name = namespace_dialog.RigDialog(text_name=self.animExportObj.export_rig_variant.get,
                                              parent=self.parent_window)
        result = rig_name.exec_()
        
        if result:
            self.animExportObj.export_rig_variant.set(rig_name.name_lineedit.text())
        self.set_clip_widget_data()

    def rebuild_clip(self):
        '''
        Rebuild the sequence, this will rebuild the metaObject
        Args:
            None
        Returns:
            None
        '''
        # create our new animExportMetaObj
        newAnimExportObj = metaFactory.getMPyNode(metaFactory.ANIM_EXPORT)

        newAnimExportObj.layers.set(self.animExportObj.export_layers.get)
        newAnimExportObj.export_start_frame.set(self.animExportObj.export_start_frame.get)
        newAnimExportObj.export_end_frame.set(self.animExportObj.export_end_frame.get)

        newAnimExportObj.Export_AnimLooping.set(self.animExportObj.Export_AnimLooping.get)
        newAnimExportObj.export_rig_name.set(self.animExportObj.export_name.get)
        newAnimExportObj.export_rig_variant.set(self.animExportObj.export_variant.get)
        newAnimExportObj.export_clip_name.set(self.animExportObj.export_clip_name.get)

        cmds.delete(self.animExportObj.name)

        # add the new widget to the animExportWidget
        self.parent_window.createSequence(newAnimExportObj)

    def set_active_animlayers(self):
        '''
        Set the color and text for animlayer but
        Args:
            None
        Returns:
            None
        '''
        if self.animExportObj.export_layers.get:
            animLayer.muteAllOtherLayers(self.animExportObj.export_layers.get)

    def storeActiveAnimlayers(self):
        '''
        Store the active animation layers
        Args:
            None
        Returns:
            None
        '''        
        self.animExportObj.export_layers.set(animLayer.getAllActiveLayers())

    def reset_active_animlayers(self):
        '''
        Set the animSeq animmlayers to None
        Args:
            None
        Returns:
            None
        '''        
        self.animExportObj.export_layers.get = None
        self.set_animlayer_button_color()

    def set_start_frame(self):
        '''
        Set thge start frame
        Args:
            None
        Returns:
            None
        '''        
        self.animExportObj.export_start_frame.set(self.start_frame_spinebox.value())

    def set_end_frame(self):
        '''
        Set the end frame
        Args:
            None
        Returns:
            None
        '''        
        self.animExportObj.export_end_frame.set(self.end_frame_spinbox.value())

    def toggle_export_button(self, widget, attribute):
        '''
        Toggle the export for the animSeq
        Args:
            None
        Returns:
            None
        '''
        if self.animExportObj.attribute(attribute).get:
            self.animExportObj.attribute(attribute).set(False)
            widget.setIcon(self.uncheckedIcon)

        else:
            self.animExportObj.attribute(attribute).set(True)
            widget.setIcon(self.checkedIcon)

    def set_button_result(self, successfull):
        '''
        Color the button if export was successful
        Args:
            None
        Returns:
            None
        '''
        if successfull:
            self.clip_name_lineedit.setStyleSheet("text-align: center; color: white; font: bold 14px; background-color: rgb(98,150,39);")
        else:
            self.clip_name_lineedit.setStyleSheet("text-align: center; color: white; font: bold 14px; background-color: rgb(237,28,36);")