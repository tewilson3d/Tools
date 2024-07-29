######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import loadUiType

import filepath
import animation.lib.timeSlider as timeslider
import animation.lib.animLayer as animLayer

import studio.lib.fbxExporter as fbxExporter
import studio.tools.content_exporter.anim_widgets.anim_clip_widget as anim_clip_widget


# MetaFactory
import meta.metaFactory as metaFactory


######################################
############# DEFINES ################
######################################
animWidget_uiPath = filepath.FilePath(__file__).dir().join(__file__.replace('.py', '.ui'))
animWidget_form_class, animWidget_base_class = loadUiType(animWidget_uiPath)


######################################
############# CLASSES ################
######################################
class AnimExportWidget(animWidget_base_class, animWidget_form_class): 

    TAB_NAME = 'Animation'

    def __init__(self, parent):
        super(AnimExportWidget, self).__init__(parent)
        self.setupUi(self)
        self.animExportList = metaFactory.getMetaObjectsByType(metaFactory.ANIM_EXPORT, True)

        # Set up signals
        self.create_animation_button.clicked.connect(self.create_animation)

        self.animation_boxlayout.setDirection(QtWidgets.QBoxLayout.BottomToTop)
        self.animation_boxlayout.addStretch(1)

        # Export Button
        self.export_button.pressed.connect(self.export_animation)

        # Build existing objects
        self.create_existing_animations()

    def toggle_all_animations(self):
        '''
        Sets all to False or True
        Args:
            None
        Returns:
            None
        '''
        animMetaObjs = metaFactory.getMetaObjectsByType(metaFactory.ANIM_EXPORT)
        
        if self.selAll_button.isChecked():
            for animObj in animMetaObjs:
                animObj.doExport.set(True)
            self.selAll_button.setIcon(self.exportAllIcon)
            self.selAll_button.setChecked(True)
        
        else:
            for animObj in animMetaObjs:
                animObj.doExport.set(False)
            self.selAll_button.setIcon(self.exportNoneIcon)
            self.selAll_button.setChecked(False)

    def create_existing_animations(self):
        '''
        Populate the ui from all existing animation nodes
        Args:
            None
        Returns:
            Builds the ui widgets from the results
        '''
        if not self.animExportList:
            self.animExportList = metaFactory.getMetaObjectsByType(metaFactory.ANIM_EXPORT)
        
        if self.animExportList:
            for animExportObj in self.animExportList:
                self.create_animation(animExportObj, fill_data=False)

    def create_animation(self, export_obj=None, fill_data=True):
        '''
        Creates the animSeqWidget from the animExportMetaObj
        
        Args:
            animExportMetaObj (AnimExportMetaNode): anim epxort meta object

        Returns:
            create the widget
        '''
        # Create new metanode
        if export_obj is None:
            export_obj = metaFactory._getInstance(metaFactory.ANIM_EXPORT)

        # If export_obj is referenced skip
        if export_obj.isReferenced():
            return

        # Pass our metaObj to the QSequenceBox
        animSeqWidget = anim_clip_widget.AnimClipBox(export_obj, self, fill_data)
        self.animation_boxlayout.addWidget(animSeqWidget)
        
        
    def export_animation(self):
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
        currentStartFrame = timeslider.startTime()
        currentEndFrame = timeslider.endTime()

        for i in range(1, self.animation_boxlayout.count()):
            export_widget = self.animation_boxlayout.itemAt(i).widget()
            export_obj = export_widget.animExportObj
            
            # Check to see if we need export
            if not export_obj.export.get:
                continue
            
            if export_obj.export_joint is None:
                raise Exception('Skeleton Root is not set.\n'+
                                'Please SetRig on {0}'.format(export_obj.export_name.get))

            try:
                # Set active animlayers
                if export_obj.export_layers.get:
                    animLayer.muteAllOtherLayers(export_obj.export_layers.get)
    
                # Export
                fbxExporter.export(export_obj.export_joint,
                                   export_obj.export_path.asMayaPath(), 
                                   exportType='anim', 
                                   startTime=export_obj.export_start_frame.get,
                                   endTime=export_obj.export_end_frame.get,
                                   saveSourceControl=True)

            except Exception as e:
                export_widget.set_button_result(False)
                raise    
            else:
                export_widget.set_button_result(True)
     
        # set the timeslider range back to default
        timeslider.setStartEndTime(currentStartFrame, currentEndFrame)