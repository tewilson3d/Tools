######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QSignal

import pyside.widgets.tearableWidget as tearableWidget


######################################
############# DEFINES ################
######################################

######################################
############# CLASSES ################
######################################
class TearableTabBar(tearableWidget.TearableWidgetBase, QtWidgets.QTabBar):
    """
    Tearable Tab Bar
        
    Signals:
        OnDetachTab (obj): QSignal For Detatching Tab
        OnMoveTab (obj): QSignal For Moving Tab
        
    Args:
        parentObjIn (obj): Parent
    """
    
    # Signals
    
    # On Detach Tab
    OnDetachTab = QSignal(int, QtCore.QPoint)
    
    # On Move Tab
    OnMoveTab = QSignal(int, int)
    
    def __init__(self,
                 parentObjIn):
        # Call the base class
        super(TearableTabBar, self).__init__(parentObjIn)
    
        # Elide Mode
        #self.setElideMode(QtCore.Qt.ElideRight)
        
        # Selection Behavior on Remove
        self.setSelectionBehaviorOnRemove(QtWidgets.QTabBar.SelectLeftTab)


    def createDragObject(self):
        """
        Create the drag object

        Args:
            None

        Returns:
            (obj): Drag Object
        """
        # Create the drag object
        dragObj = QtWidgets.QDrag(self)

        # Create the mime object
        mimeDataObj = self.createMimeObject()

        dragObj.setMimeData(mimeDataObj)

        # Create a transparent screen dump
        widgetSizeObj = self.parentWidget().currentWidget()

        pixmapObj = QtWidgets.QPixmap.grabWindow(self.parentWidget().currentWidget().winId()).scaled(widgetSizeObj.width(), widgetSizeObj.height(), QtCore.Qt.KeepAspectRatio)
        targetPixmapObj = QtWidgets.QPixmap(pixmapObj.size())
        painterObj = QtWidgets.QPainter(targetPixmapObj)
        painterObj.setOpacity(0.5)
        painterObj.drawPixmap(0, 0, pixmapObj)
        painterObj.end()
        dragObj.setPixmap(targetPixmapObj)       

        return dragObj
    
    
    def createMimeObject(self):
        """
        Create the mime object for dragging

        Args:
            None

        Returns:
            (obj): Mime Object
        """
        # Create the mime object
        mimeDataObj = QtCore.QMimeData()

        # Distinguish between drops
        mimeDataObj.setData("action", "application/widget-detach")        

        return mimeDataObj
    
    
    def handleDrag(self,
                   eventObjIn,
                   dragObjIn):
        """
        Handle the drag

        Args:
            dragObjIn (obj): Drag Object

        Returns:
            None
        """
        # Handle Detach and Move
        draggedObj = QtCore.Qt.DropAction = dragObjIn.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction)
        if draggedObj == QtCore.Qt.IgnoreAction:
            eventObjIn.accept()
            self.OnDetachTab.emit(self.tabAt(self.dragStartPosObj), self.dragDroppedPosObj)
        elif draggedObj == QtCore.Qt.MoveAction:
            if not self.dragDroppedPosObj.isNull():
                eventObjIn.accept()
                self.OnMoveTab.emit(self.tabAt(self.dragStartPosObj), self.tabAt(self.dragDroppedPosObj)) 
                
                
    def dragEnterEvent(self,
                       eventObjIn):
        """
        Drag Enter Event
        
        Args:
            eventObjIn (obj): Drag Enter Event
            
        Returns:
            None
        """
        # Only accept if its a tab-reordering request
        mimeDataObj = eventObjIn.mimeData()
        formatsList = mimeDataObj.formats()
        
        if "action" in formatsList and mimeDataObj.data("action") == "application/tab-detach":
            eventObjIn.acceptProposedAction()
            
        super(TearableTabBar, self).dragEnterEvent(eventObjIn)
        
             
    def dragMoveEvent(self,
                      eventObjIn):
        """
        Drag Move Event
        
        Args:
            eventObjIn (obj): Drag Move Event
            
        Returns:
            None
        """
        # Only accept if its a tab-reordering request
        mimeDataObj = eventObjIn.mimeData()
        formatsList = mimeDataObj.formats()
        
        if "action" in formatsList and mimeDataObj.data("action") == "application/tab-detach":
            self.dragMovedPosObj = eventObjIn.pos()
            
            eventObjIn.acceptProposedAction()
            
        super(TearableTabBar, self).dragMoveEvent(eventObjIn)
        
        
    def dropEvent(self,
                  eventObjIn):
        """
        Drop Event
        
        Args:
            eventObjIn (obj): Drop Event
            
        Returns:
            None
        """
        # If a dragged dvent is dropped within this widget it is not a drag but a move
        self.dragDroppedPosObj = eventObjIn.pos()
        
        super(TearableTabBar, self).dropEvent(eventObjIn)
            
    
    
######################################
############# FUNCTIONS ##############
######################################

######################################
############### MAIN #################
######################################
                
                