######################################
############# IMPORTS ################
######################################
import sys

import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaAnim as OpenMayaAnim

import filepath
import namespace as ns_util

import meta.metaFactory as metaFactory

import ui.qtutil as qtutil
from pyside.qt_wrapper import QtWidgets, loadUiType
import pyside.widgets.baseWindow as baseWindow

import studio.lib.fbxExporter as fbxExporter


######################################
############# DEFINES ################
######################################
ROOT_JOINT = 'Root'
EXPORT_FOLDER = 'Export'

uiPath = filepath.FilePath(__file__).dir().join("fbxExporter_window.ui")
form_class, base_class = loadUiType(uiPath)


# TO DO add export meta object

######################################
############# CLASSES ################
######################################
class FbxExportWindow(baseWindow.BaseWindow, form_class):		

    ui_name = "fbxExportWindow"
    TAB_NAME = 'FBX'

    def __init__(self, parent=None):
        if parent is None:
            parent = qtutil.getMayaWindow()
        super(FbxExportWindow, self).__init__(parent)	

        self.setupUi(self)
        self.includeHelp = True
        self.util.title = self.ui_name
        self.util.initializeSettings("FbxExportWindow")	
        self.util.recursive_settings = False

        #define our root joint since 99% of all characters have their named 'Root'
        self.root = ROOT_JOINT

        #initialize widgets		
        self.initializeSettings()

        #initialize the UI
        self.initializeUI()

        self.util.loadSettings()

    def keyPressEvent(self, event):
        '''
        Addressing the maya hotkey errors
        '''
        pass

    def closeEvent(self, event):
        '''
        kill the script jobs
        '''
        cmds.scriptJob( kill = self.playRangeJobNum, force=True)
        cmds.scriptJob( kill = self.sceneRangeJobNum, force=True)
        cmds.scriptJob( kill = self.newSceneJobNum, force=True)
        cmds.scriptJob( kill = self.sceneOpenedJobNum, force=True)

        baseWindow.BaseWindow.closeEvent(self, event)

    def initializeUI(self):
        self.toggleAnimationTimeline()

        #setup custom paths for export to show the user
        self.setExportNamePaths()

        #set some script jobs to auto update the spinners        
        self.playRangeJobNum = cmds.scriptJob( e = ["playbackRangeChanged", self.toggleAnimationTimeline], protected=True)
        self.sceneRangeJobNum = cmds.scriptJob( e = ["playbackRangeSliderChanged", self.toggleAnimationTimeline], protected=True)
        self.newSceneJobNum = cmds.scriptJob( e = ["NewSceneOpened", self.sceneChangedProc], protected=True)
        self.sceneOpenedJobNum = cmds.scriptJob( e = ["SceneOpened", self.sceneChangedProc], protected=True)

    def initializeSettings(self):

        self.animTimelineGroup.buttonClicked.connect(self.toggleAnimationTimeline)        
        self.customExportNameCheckBox.stateChanged.connect(self.enableCustomExportName)
        self.useCustomDirCheckBox.stateChanged.connect(self.enableCustomExportPath)
        self.exportGeoButton.pressed.connect(self.exportSkelMesh)
        self.exportStaticGeoButton.pressed.connect(self.exportStaticGeoProc)
        self.exportAnimButton.pressed.connect(self.multiAnimExport)
        self.browseButton.pressed.connect(self.browseForExportPath)
        self.createExportFolder_checkBox.stateChanged.connect(self.setExportNamePaths)
        self.export_to_houdini_checkBox.stateChanged.connect(self.setHoudiniPaths)

    def sceneChangedProc(self):
        #setup custom paths for export to show the user
        if not self.useCustomDirCheckBox.isChecked():
            self.setExportNamePaths()        

        #color the buttons to default
        self.colorUI(self.statusPushButton)
        self.statusPushButton.setText("Export Status:")        

    def setExportNamePaths(self):

        exportPath = ''
        sceneName = ''

        #get the scene path for the file
        scenePath = filepath.FilePath(cmds.file(q=True, sn=True))
        if self.createExportFolder_checkBox.isChecked():
            exportPath = filepath.FilePath(scenePath).dir().join(EXPORT_FOLDER)
        else:
            exportPath = filepath.FilePath(scenePath).dir()
        sceneName = str(scenePath.baseName()).split('.')[0]

        if not scenePath:
            self.printToStatus("Error: this is a blank scene, please save scene first!", 0)                        
            return exportPath, sceneName    

        #use the custom name if its there
        if self.customExportNameCheckBox.isChecked():
            tempText = self.customExportName.text()
            if not tempText:
                self.printToStatus("Error: no custom name set, using scene name", 0)                
                return exportPath, sceneName
            else:
                sceneName = tempText	    

        # set our UI text fields
        self.exportPath.setText(exportPath)
        self.customExportName.setText(sceneName.replace('Rig', 'Skelmesh'))

    def setHoudiniPaths(self):

        self.customExportNameCheckBox.setChecked(False)
        self.useCustomDirCheckBox.setChecked(False) 
        self.createExportFolder_checkBox.setChecked(False)

        #get the scene path for the file
        exportPath = filepath.DocumentPath().join('TempExports')
        sceneName = 'Temp'

        # set our UI text fields
        self.exportPath.setText(exportPath)
        self.customExportName.setText(sceneName)
        
    def toggleAnimationTimeline(self):	        

        buttonName = self.animTimelineGroup.checkedButton()        
        spinBoxValue = 0

        #time values
        mStartTime = OpenMaya.MTime()
        mEndTime = OpenMaya.MTime()        

        if buttonName.objectName() == 'useTimelineCheckBox':
            spinBoxValue = 0
            mStartTime = OpenMayaAnim.MAnimControl.minTime()
            mEndTime = OpenMayaAnim.MAnimControl.maxTime()

        elif buttonName.objectName() == 'useSceneLengthCheckBox':
            spinBoxValue = 0
            mStartTime = OpenMayaAnim.MAnimControl.animationStartTime()
            mEndTime = OpenMayaAnim.MAnimControl.animationEndTime()            

        elif buttonName.objectName() == 'useCustomTimeLineCheckBox':
            spinBoxValue = 1
            mStartTime.value = float(self.startTimeSpinBox)
            mEndTime.value = float(self.endTimeSpinBox)

        ##enable or disable the spinboxes
        #self.startTimeSpinBox.setEnabled = spinBoxValue
        #self.endTimeSpinBox.setEnabled = spinBoxValue      

        #set the value of the spinBoxes
        self.startTimeSpinBox = (mStartTime.value)
        self.endTimeSpinBox = (mEndTime.value)

    def enableCustomExportName(self):
        if self.customExportNameCheckBox.isChecked():
            self.customExportName.setEnabled(1)
        else:
            self.customExportName.setEnabled(0)

    def enableCustomExportPath(self):
        if self.useCustomDirCheckBox.isChecked():
            self.browseButton.setEnabled(1)

        else:
            self.exportPath.setEnabled(0)
            self.browseButton.setEnabled(0)

    def _checkIsWritable(self, filePathObj):
        '''
        Makes the file writeable if it is not
        '''
        if filePathObj.exists():
            if not filePathObj.isWritable():
                filePathObj.setWritable()

    def _checkDoTrianglate(self):
        if self.trinagleate_checkbox.isChecked():
            return True
        else:
            return False
        
    def exportSkelMesh(self):
        """
        Main function for exporting skeletion_mesh

        Args:
            None

        Returns:
            None

        """
        exportPath = self.getExportPath()

        #selection list to store
        selectionList = cmds.ls(sl=True, l=True)

        # add root and geomtery autodetecion
        # to do ---------------------------
        if not selectionList:

            # root joint and geometry
            if cmds.objExists(self.root):
                root_obj = metaFactory.getMPyNode(self.root)
                if root_obj.skinCluster:
                    selectionList = [sc.geometry.name for sc in root_obj.skinCluster] + [root_obj.name]

            else:
                return cmds.warning('Must select a mesh/s to export')

        # create the export folder if it does not exist
        # as of now it forces everything into a epxort folder
        if not exportPath.dir().exists():
            exportPath.dir().makeDir() 

        # check to see if the file is new
        self._checkIsWritable(exportPath)

        # Export
        fbxExporter.export(selectionList, exportPath, exportType='geo', triangulate=self._checkDoTrianglate())     

        #print success to status
        self.printToStatus("Export to {0} Successful!".format(exportPath), 1)

    def exportStaticGeoProc(self):
        """
        Static mesh exporter

        Args:
            None

        Returns:
            None

        """
        exportPath = self.getExportPath()

        if not exportPath:
            self.printToStatus("There is no export Path!", 0)
            return                

        # selection list to store
        selectionList = cmds.ls(sl=True, l=True)

        # print error if nothing is selected
        if not selectionList:
            if not cmds.objExists(self.root):
                self.printToStatus("Error: Nothing is selected!", 0)
                return        

        # create the export folder if it does not exist
        # as of now it forces everything into a epxort folder
        if not exportPath.dir().exists():
            exportPath.dir().makeDir()       

        # check to see if the file is new
        self._checkIsWritable(exportPath)

        # Export
        fbxExporter.export(selectionList, exportPath, exportType='staticGeo', triangulate=self._checkDoTrianglate())	    

        # print success to status
        self.printToStatus("Export to {0} Successful!".format(exportPath), 1)

    def exportAnimProc(self, fileNameStrOut=None):
        """
        Animation export Function

        Args:
            None

        Returns:
            None

        """
        exportPath = self.getExportPath(fileNameStr=fileNameStrOut)

        if not exportPath:
            self.printToStatus("There is no export Path!", 0)
            return                

        # need to address this with proper UI
        root_ns = ns_util.get_widget_namespace()

        # export based off of the spinBox values
        startTime = self.startTimeSpinBox
        endTime = self.endTimeSpinBox

        # need to further explore how we want to pass our skeleton
        # this should be replaced with meta call
        if len(cmds.ls(sl=True)):
            self.root = ns_util.baseName(cmds.ls(sl=True)[0])
            root_ns = ns_util.get_namespace(cmds.ls(sl=True)[0])

        selectionList = ns_util.apply_namespace(self.root,
                                                namespace=root_ns)

        # create the export folder if it does not exist
        # as of now it forces everything into a epxort folder
        if not exportPath.dir().exists():
            exportPath.dir().makeDir()

        # check to see if the file is new
        self._checkIsWritable(exportPath)      

        # Export
        fbxExporter.export(selectionList, 
                           exportPath, 
                           'anim', 
                           startTime=startTime, 
                           endTime=endTime)

        #print success to status
        self.printToStatus("Export to {0} Successful!".format(exportPath), 1)

    def browseForExportPath(self):
        
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, 
                                                                "Choose Directory",
                                                                filepath.GamePath(),
                                                                QtWidgets.QFileDialog.ShowDirsOnly)	    

        if not folderName:
            return

        exportPath = filepath.FilePath(folderName).asMayaPath()

        self.exportPath.setText(exportPath)	
        self.browseButton.setDown(False)

    def colorUI(self, ui, rgb = [100,100,100]):        
        ui.setStyleSheet("background-color: rgb("+str(rgb[0])+", "+str(rgb[1])+", "+str(rgb[2])+");\n")

    def getExportPath(self, fileNameStr=None):
        ''' fileNameStr, temp work in for exporting multiple files '''
        if not fileNameStr:
            fileNameStr = self.customExportName.text()

        return filepath.FilePath(self.exportPath.text()).join(['{0}.fbx'.format(fileNameStr)]).asMayaPath()

    def printToStatus(self, statusMessage, statusType):
        #success
        if statusType == 1:
            self.colorUI(self.statusPushButton, rgb = [0, 95, 0])
        #error
        elif statusType == 0:
            self.colorUI(self.statusPushButton, rgb = [95, 0, 0])

        self.statusPushButton.setText(statusMessage)
        sys.__stdout__.write( statusMessage + "\n")

    def multiAnimExport(self):
        ''' '''
        self.exportAnimProc()


def showUI():
    FbxExportWindow.showUI()

