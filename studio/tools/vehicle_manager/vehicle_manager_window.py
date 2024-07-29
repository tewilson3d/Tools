######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds

import filepath
import ui.qtutil as qtutil
import modeling.lib.meshdata as meshdata
import rigging.lib.skinning_utils as sknUtil
import rigging.tools.skinSave.skinSave as skinSave

import meta.metaFactory as metaFactory

from pyside.qt_wrapper import QtCore, QtWidgets, loadUiType
import pyside.widgets.baseWindow as baseWindow


######################################
############# DEFINES ################
######################################
#Constants
WINDOW_NAME = 'vehicleManagerWindow'

#The UI file must live in the same place as this file
uiPath = filepath.FilePath(__file__).dir().join("vehicle_manager_window.ui")
form_class, base_class = loadUiType(uiPath)


######################################
############# CLASSES ################
######################################
class Window(baseWindow.BaseWindow):

    ui_name = 'vehicleManagerUI'

    def __init__(self, parent=qtutil.getMayaWindow()):
        super(Window, self).__init__(parent)

        self.util.initializeSettings(WINDOW_NAME)
        self.util.recursive_settings = False
        self.setWindowTitle("Vehicle Manager UI")
        #self.setupEventHandlers(self.widget)

    def EVENT_toFile_radioButton_clicked(self):
        '''
        Event for hiding export skinSaveNode options
        '''
        self.expOptions_groupBox.setVisible(True)





######################################
############### MAIN #################
######################################
def showUI():
    """shows the Window"""
    Window.showUI()