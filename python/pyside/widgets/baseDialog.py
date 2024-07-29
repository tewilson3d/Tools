######################################
############# IMPORTS ################
######################################
import sys
from pyside.qt_wrapper import QtCore, QtWidgets
import pyside.widgets.baseWidget as baseWidget
import pyside.widgets.widgetutil as widgetutil


######################################
############# CLASSES ################
######################################
class BaseDialog(QtWidgets.QDialog, baseWidget.BaseWidget):

    #UI name that to find the UI instance - used in showUI()
    ui_name = "dialog"

    def __init__(self, parent=None, modal=False):
        super(BaseDialog, self).__init__(parent=parent)
        self.__modal = modal
        if not parent:
            # Still no parent found, exec the dialog instead.
            self.__modal = True
        self.__helpMenu = None
        self.__menuBar = None
        self.includeHelp = False #defines whether or not to show the help menu
        self.util = widgetutil.WidgetUtil(self)

    def setupUi(self, window):
        self.setModal(self.__modal)
        super(BaseDialog, self).setupUi(window)

        # Create the help menu
        if self.includeHelp:
            self.__menuBar = QtWidgets.QMenuBar(parent=self)
            self.layout().setMenuBar(self.__menuBar)
            self.__helpMenu = QtWidgets.QMenu("Help", parent=self.__menuBar)
            self.__menuBar.addMenu(self.help_menu)
        
    @property
    def help_menu(self):
        return self.__helpMenu
        
    def showDialog(self, doLoadSettings=True):
        if doLoadSettings:
            self.util.loadSettings()        
        if not self.__modal:
            super(BaseDialog, self).show()
        else:
            super(BaseDialog, self).exec_() 

    def showEvent(self, event):
        """show event"""
        super(BaseDialog, self).showEvent(event)

    def closeEvent(self, event):
        """called when the UI is closed"""
        super(BaseDialog, self).closeEvent(event)
        self.cleanupOnClose()
        self.util.saveSettings()

    def cleanupOnClose(self):
        """implement any cleaup code here"""
        super(BaseDialog, self).cleanupOnClose()

        print("cleaning up on close")
