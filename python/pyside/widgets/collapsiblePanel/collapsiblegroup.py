"""
UI Collapsible Group
"""
######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore, QtWidgets
import pyside.widgets.collapsiblePanel.collapsibleframe as collapsibleframe
import pyside.widgets.collapsiblePanel.collapsiblewidget as collapsiblewidget
from collections import OrderedDict


######################################
############# DEFINES ################
######################################


######################################
############# CLASSES ################
######################################
class GroupWidget(collapsiblewidget.BaseWidget, collapsibleframe.QCollapsibleFrame):
    def __init__(self, name, title='', userMode=collapsiblewidget.UserMode.COMMON, parent=None):
        super(GroupWidget, self).__init__(title, parent)
        self._name = name
        self._title = title
        if not self._title:
            self._title = self._name
        self._userMode = userMode
        self.buildUI()
        self._widgetList = OrderedDict()

    def buildUI(self):
        # Set up a central widget here.
        self.setTitle(self._title)
        self._mainWidget = QtWidgets.QWidget(self)
        self._mainLayout = QtWidgets.QVBoxLayout(self._mainWidget)
        self._mainWidget.setLayout(self._mainLayout)
        self._mainLayout.setSpacing(4)
        #self._mainLayout.setMargin(3)
        self.setChildWidget(self._mainWidget)

    def addWidget(self, widget):
        uniqueName = widget.uniqueName
        if uniqueName in self._widgetList:
            raise RuntimeError('Can not add widget with name {0}, already exists'.format(label))
        self._mainLayout.addWidget(widget)
        self._widgetList[uniqueName] = widget

    def addButtonWidget(self, name, label='', 
                        command=None, bgColor=None, 
                        toolTip=None, iconPath=None, 
                        userMode=collapsiblewidget.UserMode.COMMON):
        buttonWidget = collapsiblewidget.ButtonWidget(name, 
                                                      label=label, 
                                                      command=command, 
                                                      bgColor=bgColor,
                                                      iconPath=iconPath,
                                                      toolTip=toolTip,
                                                      parent=self, 
                                                      userMode=userMode)
        self.addWidget(buttonWidget)
        return buttonWidget

    def addGroup(self, name, title='', userMode=collapsiblewidget.UserMode.COMMON, parent=None):
        groupWidget = GroupWidget(name, title=title, userMode=userMode, parent=self)
        self.addWidget(groupWidget)
        return groupWidget

    def contextMenu(self):
        pass

    @property
    def uniqueName(self):
        return self._name

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newTitle):
        self._title = newTitle
        self.setTitle(newTitle)

    def setUserMode(self, newUserMode):
        if newUserMode != self._userMode:
            self.setHidden(True)
        else:
            self.setHidden(False)
        for widget in self._widgetList.items():
            widget.setUserMode(newUserMode)

    def loadSetting(self, settingDict):
        for key, setting in settingDict:
            if not key in self._widgetList:
                continue
            self._widgetList[key].loadSetting(setting)
        isCollapsed = settingDict.get(self._title, False)
        if isCollapsed == True:
            self.collapse()
        else:
            self.expand()

    def saveSetting(self):
        settingDict = {}
        for key, item in settingDict.items():
            setting = item.saveSetting()
            if not setting:
                continue
            settingDict[key] = setting
        settingDict[self._title] = self.isCollapsed()
        return settingDict