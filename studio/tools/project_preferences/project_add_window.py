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
WINDOW_NAME = 'Project Manager'

# The UI file must live in the same place as this file
uiPath = filepath.FilePath(__file__).dir().join('project_add_window.ui')
form_class, base_class = loadUiType(uiPath)


######################################
############# CLASSES ################
######################################
class Window(baseWindow.BaseWindow, form_class):

    ui_name = 'projectMangerWindow'

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

    def EVENT_project_name_lineEdit_returnPressed(self, newState):
        self._mprefObj.setPreferenceValue(project_pref.TOOL_PROJECT,
                                          newState)

    def EVENT_art_path_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        self._mprefObj.setPreferenceValue(project_pref.ART_PATH,
                                          newPathStr[0])
        self._mprefObj.applySettings()

        # update line edit with new path
        self.art_path_lineEdit.setText(newPathStr[0])
        
    def EVENT_game_path_button_clicked(self):
        newPathStr = cmds.fileDialog2(dialogStyle=1, fm=3)
        self._mprefObj.setPreferenceValue(project_pref.GAME_PATH,
                                          newPathStr[0])
        self._mprefObj.applySettings()

        # update line edit with new path
        self.game_path_lineEdit.setText(newPathStr[0])    

    def _setAllUiElementsFromJson(self):
        ''' Sets all the widgest values '''

        # Artpath
        if self._mprefObj.prefsDict[project_pref.USE_CUSTOM_PATH]:
            self.art_path_lineEdit.setText(self._mprefObj.prefsDict[project_pref.ART_PATH])
        else:
            self.art_path_lineEdit.setText(filepath.ArtPath())
            
        # Gamepath
        if self._mprefObj.prefsDict[project_pref.USE_CUSTOM_PATH]:
            self.game_path_lineEdit.setText(self._mprefObj.prefsDict[project_pref.GAME_PATH])
        else:
            self.game_path_lineEdit.setText(filepath.GamePath())    
            
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