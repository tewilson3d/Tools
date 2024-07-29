######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore, QtWidgets

import filepath
from collections import OrderedDict

######################################
############# DEFINES ################
######################################
class UserMode(object):
    COMMON   = "COMMON"
    ADVANCED = "ADVANCED"

######################################
############# CLASSES ################
######################################

class BaseWidget(object):
    '''
    This is the base class that all the widgets for collapsible panel need to inherient.
    '''
    @property
    def uniqueName(self):
        return

    def loadSetting(self):
        pass

    def saveSetting(self):
        pass

    def setUserMode(self, newUserMode):
        pass


class ButtonWidget(BaseWidget, QtWidgets.QPushButton):
    def __init__(self, name, label='', command=None, bgColor=None, toolTip=None, iconPath=None, parent=None, userMode=UserMode.COMMON):
        '''
        Args:
            name : the unique name that button widget has, no dup in the panel.

        Kwargs:
            label  : the text shown on the widget.
            command: command to run when clicked.
            bgColor: background color, like ffffff.
            toolTip: tool tip.
            iconPath: icon path.
            parent:  parent for the widget.
            userMode:user mode for this button widget.
        '''
        super(ButtonWidget, self).__init__(parent=parent)
        self._name = name
        self._label = label
        self._command = command
        self._bgColor = bgColor
        self._toolTip = toolTip
        self._iconPath = filepath.FilePath(iconPath) if iconPath else None
        self._userMode = userMode

        self.buildUI()

    def buildUI(self):
        self.setText(self._label)
        if self._bgColor:
            self.setStyleSheet("background-color: {0}".format(self._bgColor))
        if self._toolTip:
            self.setToolTip(self._toolTip)
        if self._iconPath and self._iconPath.exists():
            self.setIcon(QtGui.QIcon(self._iconPath))
            self.setIconSize(20, 20)
        if self._command:
            self.clicked.connect(self._command)

    @property
    def uniqueName(self):
        return self._name

    @property
    def title(self):
        return self._label

    @title.setter
    def title(self, newTitle):
        self.setText(newTitle)
        self._label = newTitle

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, newCommand):
        self._command = newCommand

    @property
    def bgColor(self):
        return self._bgColor

    @bgColor.setter
    def bgColor(self, newColor):
        self.setStyleSheet("background-color: {0}".format(newColor))
        self._bgColor = newColor

    @property
    def toolTip(self):
        return self._toolTip

    @toolTip.setter
    def toolTip(self, newToolTip):
        self.setToolTip(newToolTip)
        self._toolTip = newToolTip

    @property
    def iconPath(self):
        return self._iconPath

    @iconPath.setter
    def iconPath(self, newIconPath):
        self.setIcon(QtGui.QIcon(newIconPath))
        self._iconPath = newIconPath

    def setUserMode(self, newUserMode):
        if newUserMode != self._userMode:
            self.setHidden(True)
        else:
            self.setHidden(False)


class ToolBarWidget(BaseWidget, QtWidgets.QWidget):
    def __init__(self, name, columnCount=7, parent=None):
        super(ToolBarWidget, self).__init__(parent=parent)
        self._name = name
        self._mainLayout = QtWidgets.QGridLayout(self)
        self._mainLayout.setSpacing(1)
        self._columnCount = columnCount
        self._buttonInfo = OrderedDict()

    def addItem(self, label, command, bgColor=None, iconPath=None, toolTip=None, isCheckable=False, userMode=UserMode.COMMON, rowColumn=(None, None)):
        if label in self._buttonInfo:
            raise RuntimeError("Can not add a button with the same name {0}".format(label))
        button = QtWidgets.QPushButton(self)
        button.setText(label)
        button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button.setFixedSize(40, 40)
        if bgColor:
            button.setStyleSheet("background-color: #{0}".format(bgColor))
        if iconPath:
            iconPath = filepath.FilePath(iconPath)
            if iconPath.exists():
                button.setIcon(QtGui.QIcon(iconPath))
        if toolTip:
            button.setToolTip(toolTip)
        button.setCheckable(isCheckable)
        if rowColumn != (None, None):
            self._mainLayout.addWidget(button, rowColumn[0], rowColumn[1])
        else:
            value = self._mainLayout.count() % self._columnCount
            if not value:
                self._mainLayout.addWidget(button, self._mainLayout.rowCount(), 0)
            else:
                self._mainLayout.addWidget(button, self._mainLayout.rowCount()-1, value)
        if command:
            button.clicked.connect(command)
        self._buttonInfo[label] =(button, userMode) 

    def addItems(self, itemInfoList):
        exceptionList = []
        for label, iconPath, command, toolTip, isCheckable, userMode, rowColumn in itemInfoList:
            try:
                self.addItem(label, iconPath, command, toolTip=toolTip, isCheckable=isCheckable, userMode=userMode, rowColumn=rowColumn)
            except Exception as e:
                exceptionList.append('{0} with Error {1}'.format(label, e))
        if exceptionList:
            raise RuntimeError("Failed to add button/buttons: {0}".format('/n'.join(exceptionList)))

    @property
    def uniqueName(self):
        return self._name

    def setUserMode(self, newUserMode):
        for item, userMode in self._buttonInfo.items():
            if userMode != newUserMode:
                item.setHiden(True)
            else:
                item.setHidden(False)

    def saveSetting(self):
        settingDict = {}
        for label, (item, _) in self._buttonInfo.items():
            if not item.isCheckable():
                continue
            settingDict[label] = item.isChecked()

    def loadSetting(self, settingDict):
        for label, isChecked in settingDict:
            if label not in self._buttonInfo:
                continue
            self._buttonInfo[label].setChecked(isChecked)