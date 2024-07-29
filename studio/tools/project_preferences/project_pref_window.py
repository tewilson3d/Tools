######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import filepath

from pyside.qt_wrapper import loadUiType
import pyside.widgets.baseWindow as baseWindow
import ui.qtutil as qtutil
import startup.projectPreferences as project_pref


######################################
############# DEFINES ################
######################################
WINDOW_NAME = 'Project Preferences'

# The UI file must live in the same place as this file
uiPath = filepath.FilePath(__file__).dir().join('project_pref_window.ui')
form_class, base_class = loadUiType(uiPath)


######################################
############# CLASSES ################
######################################
class Window(baseWindow.BaseWindow, form_class):

    ui_name = 'projectPreferencesWindow'

    def __init__(self, parent=qtutil.getMayaWindow()):
        super(Window, self).__init__(parent)
        self.util.recursive_settings = False
        self.util.initializeSettings(WINDOW_NAME)

        self.setupUi(self)

        # intianate the preference Object
        self._mprefObj = project_pref.ProjectPreference()

        # Set all the ui elements
        self._setAllUiElementsFromJson()

        # Hook up signals
        self.setupEventHandlers(self)

    def EVENT_tools_project_comboBox_currentIndexChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.TOOL_PROJECT,
                                          newState)

    def EVENT_artPath_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        self._mprefObj.setPreferenceValue(project_pref.ART_PATH,
                                          newPathStr[0])
        self._mprefObj.applySettings()

        # update line edit with new path
        self.artPath_lineEdit.setText(newPathStr[0])
        
    def EVENT_gamePath_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        self._mprefObj.setPreferenceValue(project_pref.GAME_PATH,
                                          newPathStr[0])
        self._mprefObj.applySettings()

        # update line edit with new path
        self.gamePath_lineEdit.setText(newPathStr[0])    

    def EVENT_driveCharPath_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        if newPathStr == None:
            self._mprefObj.setPreferenceValue(project_pref.DRIVECHAR_PATH,
                                              'false')
        else:
            self._mprefObj.setPreferenceValue(project_pref.DRIVECHAR_PATH,
                                              newPathStr[0])            
        self._mprefObj.applySettings()

        # update line edit with new path
        self.driveCharPath_lineEdit.setText(newPathStr[0])    
        
    def EVENT_driveShipPath_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        self._mprefObj.setPreferenceValue(project_pref.DRIVESHIP_PATH,
                                          newPathStr[0])
        self._mprefObj.applySettings()

        # update line edit with new path
        self.driveShipPath_lineEdit.setText(newPathStr[0])    
        
    def EVENT_useArtPath_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.USE_PROJECT,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_startDatabase_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.START_DATABASE,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_buildNamespaceUI_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.BUILD_NAMESPACE_UI,
                                          newState)
        self._mprefObj.applySettings()        

    def EVENT_updateUnits_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.UPDATE_UNITS,
                                          newState)
        self._mprefObj.applySettings()    

    def EVENT_linearUnit_comboBox_currentIndexChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.LINEAR_UNIT,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_timeUnit_comboBox_currentIndexChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.TIME_UNIT,
                                          newState)
        self._mprefObj.applySettings()    

    def EVENT_updateCamera_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.UPDATE_CAMERA,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_nearClip_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.NEAR_CLIP_PLANE,
                                          newState)
        self._mprefObj.applySettings()        

    def EVENT_farClip_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.FAR_CLIP_PLANE,
                                          newState)
        self._mprefObj.applySettings()   

    def EVENT_focalLength_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.FOCAL_LENGTH,
                                          newState)
        self._mprefObj.applySettings()     

    def EVENT_updateGrid_checkBox_stateChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.UPDATE_GRID,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_gridSize_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.GRID_SIZE,
                                          newState)
        self._mprefObj.applySettings()     

    def EVENT_gridDivisions_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.GRID_DIVS,
                                          newState)
        self._mprefObj.applySettings()

    def EVENT_gridSpacing_spinBox_valueChanged(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.GRID_SPACES,
                                          newState)
        self._mprefObj.applySettings()    

    def EVENT_radioButton_Y_toggled(self, newState):
        if newState:
            self._mprefObj.setPreferenceValue(project_pref.UP_AXIS,
                                              'y')
            self._mprefObj.setSceneUpAxis()

    def EVENT_radioButton_Z_toggled(self, newState):
        if newState:
            self._mprefObj.setPreferenceValue(project_pref.UP_AXIS,
                                              'z')
            self._mprefObj.setSceneUpAxis()

    def _setAllUiElementsFromJson(self):
        ''' Sets all the widgest values '''
        self.tools_project_comboBox.setCurrentIndex(self._mprefObj.prefsDict[project_pref.TOOL_PROJECT])
        self.startDatabase_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.START_DATABASE])
        self.buildNamespaceUI_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.BUILD_NAMESPACE_UI])
        
        # Artpath
        if self._mprefObj.prefsDict[project_pref.USE_CUSTOM_PATH]:
            self.artPath_lineEdit.setText(self._mprefObj.prefsDict[project_pref.ART_PATH])
        else:
            self.artPath_lineEdit.setText(filepath.ArtPath())
            
        # Gamepath
        if self._mprefObj.prefsDict[project_pref.USE_CUSTOM_PATH]:
            self.gamePath_lineEdit.setText(self._mprefObj.prefsDict[project_pref.GAME_PATH])
        else:
            self.gamePath_lineEdit.setText(filepath.GamePath())    
            
        self.useArtPath_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.USE_PROJECT])
        self.updateUnits_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.UPDATE_UNITS])
        self.linearUnit_comboBox.setCurrentIndex(self._mprefObj.prefsDict[project_pref.LINEAR_UNIT])
        self.timeUnit_comboBox.setCurrentIndex(self._mprefObj.prefsDict[project_pref.TIME_UNIT])
        self.updateCamera_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.UPDATE_CAMERA])
        self.nearClip_spinBox.setValue(self._mprefObj.prefsDict[project_pref.NEAR_CLIP_PLANE])
        self.farClip_spinBox.setValue(self._mprefObj.prefsDict[project_pref.FAR_CLIP_PLANE])
        self.focalLength_spinBox.setValue(self._mprefObj.prefsDict[project_pref.FOCAL_LENGTH])
        self.updateGrid_checkBox.setChecked(self._mprefObj.prefsDict[project_pref.UPDATE_GRID])
        self.gridSize_spinBox.setValue(self._mprefObj.prefsDict[project_pref.GRID_SIZE])
        self.gridDivisions_spinBox.setValue(self._mprefObj.prefsDict[project_pref.GRID_DIVS])
        self.gridSpacing_spinBox.setValue(self._mprefObj.prefsDict[project_pref.GRID_SPACES])
        self.radioButton_Y.setChecked(True if self._mprefObj.prefsDict[project_pref.UP_AXIS] == 'y' else False)
        self.radioButton_Z.setChecked(True if self._mprefObj.prefsDict[project_pref.UP_AXIS] == 'z' else False)

######################################
############### MAIN #################
######################################
def showUI():
    '''
    Shows the UI
    '''
    Window.showUI()