"""
Tearable Widget
"""
#
#

######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QSignal

from 

######################################
############# DEFINES ################
######################################

######################################
############# CLASSES ################
######################################
class DetachedWindow(QtWidgets.QDialog):
    """
    Detached Window

    Args:
        None

    Keyword Args:
        parentObjIn (obj): Parent
    Signals:
        OnClose (obj): QSignal Close
    """
    # Signals
    OnClose = QSignal(QtWidgets.QWidget)

    def __init__(self,
                 parentObjIn=None):
        super(DetachedWindow, self).__init__(parentObjIn)


    def closeEvent(self,
                   eventObjIn):
        """
        Close Event

        Args:
            eventObjIn (obj): QCloseEvent

        Returns:
            None
        """
        self.OnClose.emit(self)
        
        
class TearableWidgetBase(object):
    """
    Tearable Widget Base
    
    Attributes:
        dragStartPosObj (obj): QtPos Drag Start Position
        dragDroppedPosObj (obj): QtPos Drag Dropped Position
        dragMovedPosObj (obj): QtPos Drag Moved
        isDragInitiated (bool): Is the drag initiated?
        
    Args:
        parentObjIn (obj): Parent        
    """
    def __init__(self,
                 parentObjIn):
        # Call the base class
        super(TearableWidgetBase, self).__init__(parentObjIn)
    
        # Accept Drops
        self.setAcceptDrops(True)
        
        # Attributes
        self.dragStartPosObj = QtCore.QPoint()
        self.dragDroppedPosObj = QtCore.QPoint()
        self.dragMovedPosObj = QtCore.QPoint()
        self.isDragInitiated = QtCore.QPoint()    
        

    def mousePressEvent(self,
                        eventObjIn):
        """
        Mouse Press Event Override

        Args:
            eventObjIn (obj): QMouseEvent

        Returns:
            None
        """
        # See if we are dragging with the left mouse button
        if eventObjIn.button() == QtCore.Qt.LeftButton:
            # Set the drag start position
            self.dragStartPosObj = eventObjIn.pos()

        # Reset our values
        self.dragDroppedPosObj.setX(0)
        self.dragDroppedPosObj.setY(0)
        self.dragMovedPosObj.setX(0)
        self.dragMovedPosObj.setY(0)

        # Reset drag initiated
        self.isDragInitiated = False

        # Call the base mouse event
        super(TearableWidgetBase, self).mousePressEvent(eventObjIn)


    def mouseMoveEvent(self,
                       eventObjIn):
        """
        Mouse Move Event Override

        Args:
            eventObjIn (obj): QMouseEvent

        Returns:
            None
        """        
        # Distinguish a drag
        if (not self.dragStartPosObj.isNull()) and ((eventObjIn.pos() - self.dragStartPosObj).manhattanLength() > QtWidgets.QApplication.startDragDistance()):
            # We are dragging
            self.isDragInitiated = True

        # Is the left button pressed and we are dragging and the mouse moved outside of the tab bar
        if (eventObjIn.buttons() & QtCore.Qt.LeftButton) and self.isDragInitiated and not (self.geometry().contains(eventObjIn.pos())):
            # Stop the move to be able to convert to a drag
            finishMoveEventObj = QtWidgets.QMouseEvent(QtCore.QEvent.MouseMove,
                                                   eventObjIn.pos(), 
                                                   QtCore.Qt.NoButton, 
                                                   QtCore.Qt.NoButton, 
                                                   QtCore.Qt.NoModifier)
            # Finish the move event
            super(TearableWidgetBase, self).mouseMoveEvent(finishMoveEventObj)


            # Initiate the drag
            self.initiateDrag(eventObjIn)
        else:
            super(TearableWidgetBase, self).mouseMoveEvent(eventObjIn)      
            
            
    def initiateDrag(self,
                     eventObjIn):
        """
        Initiate the drag
        
        Args:
            eventObjIn (obj): QMouseEvent
            
        Returns:
            None
        """
        # Initiate drag
        dragObj = self.createDragObject()
        
        # Handle the drag
        self.handleDrag(eventObjIn,
                        dragObj)
        
        
    def handleDrag(self,
                   eventObjIn,
                   dragObjIn):
        """
        Handle the drag
        
        Args:
            eventObjIn (obj): QMouseEvent
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
        pixmapObj = QtWidgets.QPixmap.grabWidget(self).scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio)
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
        
            
class TearableWidget(TearableWidgetBase, QtWidgets.QWidget):
    """
    Tearable Widget
    
    Args:
        parentObjIn (obj): Parent
        
    Signals:
        OnDetach (obj): QSignal For Detatching Widget        
    """
    OnDetatch = QSignal(QtWidgets.QWidget, QtCore.QPoint)
    
    def __init__(self, 
                 parentObjIn):
        super(TearableWidget, self).__init__(parentObjIn)
    
    
    def eventFilter(self, 
                    sourceObjIn,
                    eventObjIn):
        """
        Event Filter
        
        Args:
            sourceObjIn (obj): Source
            eventObjIn (obj): Event
            
        Returns:
            (bool): Accepted/Rejected
        """
        if eventObjIn.type() == QtCore.QEvent.MouseMove:
            self.mouseMoveEvent(eventObjIn)
            return True
        elif eventObjIn.type() == QtCore.QEvent.MouseButtonPress:
            self.mousePressEvent(eventObjIn)
            return True
        
        return QtWidgets.QWidget.eventFilter(self, sourceObjIn, eventObjIn)                                         
                     
                     
    def setParent(self,
                  parentObjIn,
                  windowFlagsIntIn=QtCore.Qt.WindowFlags()):
        """
        Set Parent Override
        
        Ensure that if we are parented to a `core.qt.widgets.tearableWidget.TearableWidgetParent` instance
        we call the neccessary functions to connect the `OnDetach` signal
        
        Args:
            parentObjIn (obj): New Parent
        
        Keyword Args:
            windowFlagsIntIn (int): Window Flags
            
        Returns:
            None
        """
        super(TearableWidget, self).setParent(parentObjIn, windowFlagsIntIn)
        
        if isinstance(parentObjIn, TearableWidgetParent):
            parentObjIn.connectDetatchSignals(self)
            
            
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
            self.OnDetatch.emit(self, self.dragDroppedPosObj)
        elif draggedObj == QtCore.Qt.MoveAction:
            if not self.dragDroppedPosObj.isNull():
                eventObjIn.accept()
                
                
class TearableWidgetParent(QtWidgets.QWidget):
    """
    Tearable Widget Parent
    
    Args:
        None
        
    Keyword Args:
        parentObjIn (obj): Parent
    """
    def __init__(self,
                 parentObjIn=None):
        super(TearableWidgetParent, self).__init__(parentObjIn)
        
    
    def __dir__(self):
        """
        Dir Override
        
        Args:
            None
            
        Returns:
            (list): Attributes
        """
        # Get our base attirbutres
        baseAttributesList = dir(super(TearableWidgetParent, self))
        
        # Get the QtChildren
        qtChildrenList = self.findChildren(QtCore.QObject)
        
        # Get the object names
        objectNamesList = [x.objectName() for x in qtChildrenList if len(x.objectName()) > 0]
        objectNamesList = list(set(objectNamesList))
        
        # Build our new attribute list
        attrList = baseAttributesList + objectNamesList
        
        return attrList
    
        
    def __getattr__(self,
                    attrNameStrIn):
        """
        Get Attribute Override

        Args:
            attrNameStrIn (str): Attribute Name

        Returns:
            (void): Requested Attribute

        Raises:
            (AttributeError): Attribute Not Found
        """
        if attrNameStrIn in self.__dict__:
            return self.__dict__[attrNameStrIn]
        else:
            # Check for children
            childObj = self.findChild(QtCore.QObject, attrNameStrIn)

            if childObj is not None:
                return childObj

        raise AttributeError("'{0}' object has no attribute '{1}'".format(self, 
                                                                          attrNameStrIn))
    
    
    def connectDetatchSignals(self,
                              tearableWidgetObjIn):
        """
        Connect the detach signals
        
        Args:
            tearableWidgetObjIn (obj): Tearable Widget Instance
            
        Returns:
            None
        """
        if isinstance(tearableWidgetObjIn, TearableWidget):
            try:
                tearableWidgetObjIn.OnDetatch.disconnect(self.detach)
            except TypeError as errorObj:
                pass
            
            tearableWidgetObjIn.OnDetatch.connect(self.detach)
                
    
    def attach(self,
               parentObjIn):
        """
        Attach a widget

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
        #self.layout().addWidget(tearOffWidgetObj)
        
        # Cleanup window
        detachedWindowObj.OnClose.disconnect(self.attach)
        detachedWindowObj.close()
        del(detachedWindowObj)
        
        tearOffWidgetObj.show()
        self.layout()
        
        
    def detach(self,
               childWidgetObjIn,
               pointObjIn):
        """
        Detach a widget

        Args:
            childWidgetObjIn (obj): Child Widget
            pointObjIn (obj): Drop Point

        Returns:
            None
        """
        # Create a window
        detatchedWindowObj = DetachedWindow(self.parentWidget())
        detatchedWindowObj.setWindowModality(QtCore.Qt.NonModal)

        # Set the layout
        mainLayoutObj = QtWidgets.QVBoxLayout(detatchedWindowObj)
        mainLayoutObj.setContentsMargins(0, 0, 0, 0)
        detatchedWindowObj.setLayout(mainLayoutObj)

        # Find the widget and connect
        tearOffWidgetObj = childWidgetObjIn
        detatchedWindowObj.OnClose.connect(self.attach)
        
        # TODO: How to get new window title?
        #detatchedWindowObj.setWindowTitle(self.tabText(indexIntIn))

        # Remove the tab bar
        tearOffWidgetObj.setParent(detatchedWindowObj)

        # Create and show
        mainLayoutObj.addWidget(tearOffWidgetObj)
        tearOffWidgetObj.show()
        detatchedWindowObj.resize(tearOffWidgetObj.size())
        detatchedWindowObj.show()

        detatchedWindowObj.move(QtWidgets.QCursor.pos())                
                
######################################
############# FUNCTIONS ##############
######################################

######################################
############### MAIN #################
######################################