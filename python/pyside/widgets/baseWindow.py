######################################
############# IMPORTS ################
######################################
import re
import functools
import contextlib

from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets
import pyside.widgets.baseWidget as baseWidget
import pyside.widgets.widgetutil as widgetutil


######################################
############# CLASSES ################
######################################
class BaseWindow(QtWidgets.QMainWindow, baseWidget.BaseWidget):

    #UI name that to find the UI instance - used in showUI()
    ui_name = "window"

    def __init__(self, parent=None):
        super(BaseWindow, self).__init__(parent)

        self._helpMenu = None
        self.includeHelp = False
        self.util = widgetutil.WidgetUtil(self)

    @contextlib.contextmanager
    def waitCursor(self):
        """
        Wait Cursor Context Manager

        Args:
            None

        Yields:
            None
        """
        try:
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            yield None
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()

    def setupEventHandlers(self, eventHandlerParentObjIn):
        """
        Connect Event Handlers

        Args:
            eventHandlerParentObjIn (obj): Parent Object which contains the event handler functions

        Returns:
            None
        """
        # Get all the children
        qtChildrenList = self.findChildren(QtWidgets.QWidget)
        qtChildrenList.extend(self.findChildren(QtWidgets.QAction))

        # Go through the children and see if we have event handlers for them
        for currentChildObj in qtChildrenList:
            # Get the object name
            objectNameStr = currentChildObj.objectName()

            # Look for a handler
            for currentAttrStr in dir(eventHandlerParentObjIn):
                """
                To make it simpler to create event handlers for Qt Objects, we are using a regular expression to find
                event handlers for individual widgets. Event handler functions are defined by starting the function named
                with `EVENT_`. The regular expression then looks for the widget name followed by a `_` and then the signal name.

                Take the following as a scenario:

                We have a QPushButton named `pbut_selectedPlayerTeam` and we want to create an event handler for the `clicked` signal.

                Knowing all this we would name our function `EVENT_pbut_selectedPlayerTeam_clicked`
                """
                reObj = re.search("EVENT_({0})_(?P<signal>[a-zA-Z0-9]*)(_|$)".format(objectNameStr), currentAttrStr)

                if reObj is not None:
                    # Get the signal
                    signalStr = reObj.groupdict()["signal"]

                    # Make sure the widget has the signal
                    if hasattr(currentChildObj, signalStr):
                        # Get the signal
                        signalObj = getattr(currentChildObj, signalStr)
                        functionObj = getattr(eventHandlerParentObjIn, currentAttrStr)

                        # Build the slot
                        newSlotFunc = functools.partial(functionObj)

                        # Connect the slot
                        signalObj.connect(newSlotFunc)
                    else:
                        # TODO: Should we raise an error here or have some sort of warning?
                        raise AttributeError("Invalid Event Handler for {0} - {0} has no SIGNAL named {1}".format(objectNameStr,
                                                                                                                  signalStr))         

    def setupUi(self, window):
        super(BaseWindow, self).setupUi(window)

        # Create the help menu
        if self.includeHelp:
            menuBar = self.menuBar()
            self._helpMenu = QtWidgets.QMenu("Help")
            menuBar.addMenu(self.help_menu)

    @property
    def help_menu(self):
        return self._helpMenu

    def show(self, doLoadSettings=True):
        if doLoadSettings:
            self.util.loadSettings()
        super(BaseWindow, self).show()

    def showEvent(self, event):
        """show event"""
        super(BaseWindow, self).showEvent(event)

    def closeEvent(self, event):
        """called when the UI is closed"""
        super(BaseWindow, self).closeEvent(event)
        self.cleanupOnClose()
        self.util.saveSettings()

    def cleanupOnClose(self):
        """implement any cleaup code here"""
        super(BaseWindow, self).cleanupOnClose()
        print("cleaning up on close")