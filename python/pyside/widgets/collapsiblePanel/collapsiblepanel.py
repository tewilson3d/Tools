"""
UI Collapsible Panel
"""
######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore, QtWidgets
import pyside.widgets.baseWindow as baseWindow
import pyside.widgets.collapsiblePanel.collapsiblewidget as uiCollapsibleWidget
import pyside.widgets.collapsiblePanel.collapsiblegroup as uiCollapsibleGroup
from collections import OrderedDict

######################################
############# DEFINES ################
######################################


######################################
############# CLASSES ################
######################################
class PanelWidget(baseWindow.BaseWindow, uiCollapsibleWidget.BaseWidget):
    
    ui_name= "PanelWidget"

    def __init__(self, name, title='', parent=None):
        super(PanelWidget, self).__init__(parent=parent)
        self._name = name
        self._title = title
        self.util.recursive_settings = False

        if not self._title:
            self._title = self._name
        self._widgetInfo = OrderedDict()
        self.buildUI()

    def buildUI(self):
        #super(PanelWidget, self).setupUi(self)
        self._mainWidget = QtWidgets.QWidget(self)
        self._mainLayout = QtWidgets.QVBoxLayout(self._mainWidget)
        self._mainLayout.setSpacing(2)
        #self._mainLayout.setMargins(3)
        self._mainWidget.setLayout(self._mainLayout)
        self._mainWidget.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                       QtWidgets.QSizePolicy.Fixed) 

        self._scrollWidget = QtWidgets.QScrollArea()
        self._scrollWidget.setWidget(self._mainWidget)
        self._scrollWidget.setWidgetResizable(True)
        self.setCentralWidget(self._scrollWidget)

        # Add a stretch item.
        self._mainLayout.addStretch()
        self.setWindowTitle(self._title)
        self.setObjectName(self._name)

    def setPanelWidth(self, widthValue):
        self.setMaximumWidth(widthValue)

    def addWidget(self, widget):
        uniqueName = widget.uniqueName
        if uniqueName in self._widgetInfo:
            raise RuntimeError('Can not add widget with name {0}, already exists'.format(uniqueName))
        self._insertWidget(widget)

    def addGroup(self, name, title='', userMode=uiCollapsibleWidget.UserMode.COMMON):
        groupWidget = uiCollapsibleGroup.GroupWidget(name, title=title, userMode=userMode, parent=self)
        self.addWidget(groupWidget)
        return groupWidget

    def addButtonWidget(self, name, label='', command=None, bgColor=None, toolTip=None, iconPath=None, userMode=uiCollapsibleWidget.UserMode.COMMON):       
        buttonWidget = uiCollapsibleWidget.ButtonWidget(name, 
                                                        label=label, 
                                                        command=command, 
                                                        bgColor=bgColor,
                                                        iconPath=iconPath,
                                                        toolTip=toolTip,
                                                        parent=self, 
                                                        userMode=userMode)
        self.addWidget(buttonWidget)
        return buttonWidget

    @property
    def uniqueName(self):
        return self._name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newTitle):
        self.setWindowTitle(newTitle)
        self._title = newTitle

    def loadSetting(self):
        for key, item in self._widgetInfo:
            setting = self.util.getValue(key)
            if not setting:
                continue
            item.loadSetting(setting)

    def saveSetting(self):
        if not self.util:
            return
        for key, item in self._widgetInfo.items():
            setting = item.saveSetting()
            if not setting:
                continue
            self.util.setValue(key, setting) 

    def closeEvent(self, event):
        self.saveSetting()
        super(PanelWidget, self).closeEvent(event)  

    def _insertWidget(self, widget):
        self._mainLayout.insertWidget(self._mainLayout.count() - 1, widget)
        self._widgetInfo[widget.uniqueName] = widget


######################################
############# FUNCTIONS ##############
######################################
def showAsDockWidget(window):
    import maya.cmds as cmds
    if cmds.dockControl(window.uniqueName + 'Dock',
                        q=1,
                        ex=1):
        cmds.deleteUI(window.uniqueName + 'Dock')
        doForceVisible = True    
    cmds.dockControl(window.uniqueName + 'Dock', 
                     aa=["right", "left"],
                     a="right",
                     content=window.uniqueName,
                     label=window.title)    

def main():
    import functools
    import ui.qtutil as qtutil
    a = PanelWidget("Test", parent=qtutil.getMayaWindow())
    b1 = uiCollapsibleWidget.ButtonWidget("TestButton", label='test', command=functools.partial(printFunc, "TestButton1"))
    a.addWidget(b1)
    import pyside.widgets.collapsiblePanel.uiCollapsibleGroup as uiCollapsibleGroup

    g1 = uiCollapsibleGroup.GroupWidget("Test")
    b2 = g1.addButtonWidget("TestButton2", label="Test2", command=functools.partial(printFunc, "TestButton2"))
    a.addWidget(g1)

    showAsDockWidget(a)