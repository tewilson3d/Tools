######################################
############# IMPORTS ################
######################################
import os
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds

import filepath
import ui.qtutil as qtutil
import pyside.widgets.baseWindow as baseWindow
from pyside.qt_wrapper import loadUiType

import meta.metaFactory as metaFactory
import studio.tools.content_exporter.anim_widgets.anim_export_widget as animWidget
import studio.tools.content_exporter.rig_widgets.rig_export_widget as rigWidget
import studio.tools.content_exporter.model_widgets.model_export_widget as modelWidget

import rigging.globals as globals
import rigging.lib.joint_utils as jnt_utils
import rigging.lib.components.createRig as createRig

######################################
############# DEFINES ################w
######################################
baseWindow_uiPath = filepath.FilePath(__file__).dir().join(__file__.replace('.py', '.ui'))
form_class, base_class = loadUiType(baseWindow_uiPath)

WINDOW_NAME          = "Exporter"
WINDOW_SETTINGS_NAME = 'Exporter_Settings'


######################################
############# CLASSES ################
######################################
class ExportWindow(baseWindow.BaseWindow, form_class):

    ui_name = 'ExporterWindow'
    build_rig_tab = 'rig_export_tab'
    build_anim_tab = 'anim_export_tab'
    build_model_tab = 'model_export_tab'
    build_env_tab = 'env_export_tab'
    build_generic_tab = 'generic_export_tab'

    def __init__(self, rigging_tab=None,animation_tab=None,model_tab=None):
        super(ExportWindow, self).__init__(qtutil.getMayaWindow())
        self.setupUi(self)

        self.util.title = WINDOW_NAME
        self.util.recursive_settings = False
        self.util.initializeSettings(WINDOW_SETTINGS_NAME)

        # define rig meta object to pass to anim/rig export widgets
        #self.rig_obj = None
        #self.create_rig_object()
        self.rig_widget=rigging_tab
        self.anim_widget=animation_tab
        self.model_widget=model_tab
        
        self.messageIds = []
        #self.initializeScriptJobs()
        current_tab = self.loadSetting()
        self.loadUIData(current_tab)

        # ui function
        #self.refresh_ui_button.clicked.connect(self.relaunch_window)
        
        # tool action 
        self.createDisplaySet_action.triggered.connect(self.create_meta_sets)
        #self.build_rig_tab_action.triggered.connect(self.relaunch_window)
        #self.build_model_tab_action.triggered.connect(self.relaunch_window)
        #self.build_anim_tab_action.triggered.connect(self.relaunch_window)

    def closeEvent(self, event):
        ''' '''
        if self.messageIds:
            for id in self.messageIds:
                OpenMaya.MMessage.removeCallback(id)
        self.messageIds = []

        self.saveSetting()       
        super(ExportWindow, self).closeEvent(event)     

    def saveSetting(self):
        '''
        Save wdiget settings
        '''
        self.util.settings.setValue(self.build_rig_tab, self.build_rig_tab_action.isChecked())
        self.util.settings.setValue(self.build_anim_tab, self.build_anim_tab_action.isChecked())
        self.util.settings.setValue(self.build_model_tab, self.build_model_tab_action.isChecked())
        self.util.settings.setValue(self.build_generic_tab, self.build_generic_tab_action.isChecked())
        self.util.settings.setValue('cuurentTab', self.export_tabwidget.currentIndex())        

    def loadSetting(self):
        '''
        Load settings
        '''
        if not self.util.settings:
            return

        build_rig = self.util.settings.getValue(self.build_rig_tab)
        build_anim = self.util.settings.getValue(self.build_anim_tab)
        build_model = self.util.settings.getValue(self.build_model_tab)
        build_generic = self.util.settings.getValue(self.build_generic_tab)
        current_tab  = self.util.settings.getValue('cuurentTab') 
        
        if build_rig:
            self.build_rig_tab_action.setChecked(int(build_rig))
        if build_anim:
            self.build_anim_tab_action.setChecked(int(build_anim))
        if build_generic:
            self.build_generic_tab_action.setChecked(int(build_generic))
        if build_model:
            self.build_model_tab_action.setChecked(int(build_model))
            
        return current_tab

    def initializeScriptJobs(self):
        '''
        Creates the script jobs or open and new scene
        '''
        scene_events = [OpenMaya.MSceneMessage.kAfterOpen, OpenMaya.MSceneMessage.kAfterNew]
        for event in scene_events:
            self.messageIds.append(OpenMaya.MSceneMessage.addCallback(event, 
                                                                      ExportWindow.reloadUICallback, 
                                                                      self))

    @staticmethod
    def reloadUICallback(uiInstance):
        """callback that gets called when a new or existing scene is opened"""
        uiInstance.loadUIData()

    def loadUIData(self,current_tab=None):
        """loads the UI data from the scene"""
        self.export_tabwidget.clear()

        #if self.rig_obj:
        
        #if self.rig_widget:
        self.rigTabWidget = rigWidget.RigExportWidget(self)
        self.export_tabwidget.addTab(self.rigTabWidget, self.rigTabWidget.TAB_NAME) 

        #if self.anim_widget:
        self.animTabWidget = animWidget.AnimExportWidget(self)
        self.export_tabwidget.addTab(self.animTabWidget, self.animTabWidget.TAB_NAME)

        #if self.model_widget:
        self.modelTabWidget = modelWidget.ModelExportWidget(self)
        self.export_tabwidget.addTab(self.modelTabWidget, self.modelTabWidget.TAB_NAME)
            
        if current_tab:
            self.export_tabwidget.setCurrentIndex(int(current_tab))
            
        self.create_meta_sets()

    def create_meta_sets(self):
        cmds.select(clear=True)
        import meta.metaFactory as metaFactory
        metaFactory.createMetaNodeSelectionSet()
        
    def relaunch_window(self,rig=True,anim=True,model=True):
        showUI(rig,anim,model)

def showUI(rig=None,anim=None,model=None):
    # testing a crash
    global win
    try:
        win.close()
    except:
        pass
    
    win = ExportWindow(rig, anim, model)
    win.show()
