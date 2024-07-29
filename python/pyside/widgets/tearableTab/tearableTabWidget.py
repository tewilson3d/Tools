"""
Tearable Tab Widget
"""
######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QSignal

import pyside.widgets.tearableTab.tearableTabBar as tearableTabBar
import pyside.widgets.tearableWidget as tearableWidget


######################################
############# DEFINES ################
######################################

######################################
############# CLASSES ################
######################################        
class TearableTabWidget(QtWidgets.QTabWidget):
    """
    Tearable Tab Widget
    
    Attributes:
        tabBarObj (obj): :py:class:`core.qt.widgets.tearableTab.tearableTabBar` Tab Bar
        
    Args:
        None
        
    Keyword Args:
        parentObjIn (obj): Parent
    """
    def __init__(self,
                 parentObjIn=None):
        # Call init
        super(TearableTabWidget, self).__init__(parentObjIn)
        
        # Create the tearable tab bar
        self.tabBarObj = tearableTabBar.TearableTabBar(self)
        
        # Connect the signals
        self.tabBarObj.OnDetachTab.connect(self.detachTab)
        self.tabBarObj.OnMoveTab.connect(self.moveTab)
        
        # Set the tab bar
        self.setTabBar(self.tabBarObj)
        
        # Set Moveable
        self.setMovable(True)
        
        #newWidgetObj = QtWidgets.QWidget(self)
        #self.addTab(newWidgetObj, "Test")
        
        #newWidget2Obj = QtWidgets.QWidget(self)
        #self.addTab(newWidget2Obj, "Test2")

    
    def moveTab(self,
                fromIndexIntIn,
                toIndexIntIn):
        """
        Move a tab
        
        Args:
            fromIndexIntIn (int): From Index
            toIndexIntIn (int): To Index
        
        Returns:
            None
        """
        # Get the from widget data
        widgetObj = self.widget(fromIndexIntIn)
        iconObj = self.tabIcon(fromIndexIntIn)
        textStr = self.tabText(fromIndexIntIn)
        
        # Remove the tab
        self.removeTab(fromIndexIntIn)
        
        # Insert the new tab
        self.insertTab(toIndexIntIn,
                       widgetObj,
                       iconObj,
                       textStr)
        
        # Set the current index
        self.setCurrentIndex(toIndexIntIn)
        
        
    def detachTab(self,
                   indexIntIn,
                   pointObjIn):
        """
        Detach a tab
        
        Args:
            indexIntIn (int): Tab to detatch
            pointObjIn (obj): Drop Point
            
        Returns:
            None
        """
        # Create a window
        detatchedWindowObj = tearableWidget.DetachedWindow(self.parentWidget())
        detatchedWindowObj.setWindowModality(QtCore.Qt.NonModal)
        
        # Set the layout
        mainLayoutObj = QtWidgets.QVBoxLayout(detatchedWindowObj)
        mainLayoutObj.setContentsMargins(0, 0, 0, 0)
        detatchedWindowObj.setLayout(mainLayoutObj)
        
        # Find the widget and connect
        tearOffWidgetObj = self.widget(indexIntIn)
        detatchedWindowObj.OnClose.connect(self.attachTab)
        detatchedWindowObj.setWindowTitle(self.tabText(indexIntIn))
        
        # Remove the tab bar
        tearOffWidgetObj.setParent(detatchedWindowObj)
        
        # Make the first active
        if 0 < self.count():
            self.setCurrentIndex(0)
            
        # Create and show
        mainLayoutObj.addWidget(tearOffWidgetObj)
        tearOffWidgetObj.show()
        detatchedWindowObj.resize(tearOffWidgetObj.size())
        detatchedWindowObj.show()
        
        detatchedWindowObj.move(QtWidgets.QCursor.pos())
        
        
    def attachTab(self,
                  parentObjIn):
        """
        Attach a tab
        
        Args:
            parentObjIn (obj): Parent
            
        Returns:
            None
        """
        # Retrieve the widget
        detachedWindowObj = parentObjIn
        tearOffWidgetObj = detachedWindowObj.layout().takeAt(0).widget()
        
        # Change the parent
        tearOffWidgetObj.setParent(self)
        
        # Attach
        newIndexInt = self.addTab(tearOffWidgetObj, detachedWindowObj.windowTitle())
        
        # Make active
        if newIndexInt != -1:
            self.setCurrentIndex(newIndexInt)
            
        # Cleanup window
        detachedWindowObj.OnClose.disconnect(self.attachTab)
        del(detachedWindowObj)


######################################
############# FUNCTIONS ##############
######################################

######################################
############### MAIN #################
######################################
if __name__ == "__main__":
    app = core.pyside.qt.createApp()
    mainWindow = QtWidgets.QMainWindow()
    mainWindow.resize(500, 500)
    centralWidget = QtWidgets.QWidget(mainWindow)
    centralWidget.resize(500, 500)
    
    layout = QtWidgets.QVBoxLayout(centralWidget)
    centralWidget.setLayout(layout)
    
    #tabWidget = TearableTabWidget(mainWindow)
    #tabWidget.setMinimumSize(200, 200)
    
    tearableParent = tearableWidget.TearableWidgetParent(centralWidget)
    tearableParent.setMinimumSize(200, 200)
    
    layout2 = QtWidgets.QVBoxLayout(tearableParent)
    tearableParent.setLayout(layout2)
    
    tearableWidgetObj = tearableWidget.TearableWidget(tearableParent)
    tearableWidgetObj.setMaximumSize(20, 20)
    tearableWidgetObj.setParent(tearableParent)
    tearableWidgetObj.setStyleSheet("background-color:blue;")
    layout2.addWidget(tearableWidgetObj)
    
    
    tearableWidgetObj2 = tearableWidget.TearableWidget(tearableParent)
    tearableWidgetObj2.setMaximumSize(20, 20)
    tearableWidgetObj2.setParent(tearableParent)
    tearableWidgetObj2.setStyleSheet("background-color:green;")
    layout2.addWidget(tearableWidgetObj2)


    label = QtWidgets.QLabel(tearableWidgetObj)
    label.setText("Hello")
    
    label2 = QtWidgets.QLabel(tearableWidgetObj2)
    label2.setText("2")


    #layout.addWidget(tabWidget)
    layout.addWidget(tearableParent)
    
    centralWidget.layout()
    tearableParent.layout()
    
    mainWindow.show()
    app[0].exec_()