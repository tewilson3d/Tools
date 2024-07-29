######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtGui
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets

from pyside.widgets.icon import Icon
from pyside.widgets.color import Color

import filepath


######################################
############# DEFINES ################
######################################
#SPACE_OPERATOR = "and"
PLACEHOLDER_TEXT = "Search"


######################################
############# CLASSES ################ 
######################################
class LineEdit(QtWidgets.QLineEdit):

    searchChanged = QtCore.Signal()

    def __init__(self, *args):
        QtWidgets.QLineEdit.__init__(self, *args)

        self._dataset = None
        self._iconPadding = 6
        self._iconButton = QtWidgets.QPushButton(self)
        #self._iconButton.clicked.connect(self._iconClicked)

        icon = Icon(filepath.IconPath().join("search_simple.png"))
        self._iconButton.setIcon(icon)

        self.setPlaceholderText(PLACEHOLDER_TEXT)
        #self.textChanged.connect(self.search)

        self.update()

    def update(self):
        self.updateIconColor()

    def setDataset(self, dataset):
        """
        Set the data set for the search widget:
        
        :type dataset: studiolibrary.Dataset
        """
        self._dataset = dataset

    def dataset(self):
        """
        Get the data set for the search widget.
        
        :rtype: studiolibrary.Dataset 
        """
        return self._dataset

    #def _iconClicked(self):
        #"""
        #Triggered when the user clicks on the icon.

        #:rtype: None
        #"""
        #if not self.hasFocus():
            #self.setFocus()

    #def _textChanged(self, text):
        #"""
        #Triggered when the text changes.

        #:type text: str
        #:rtype: None
        #"""
        #self.search()

    def search(self):
        """Run the search query on the data set."""
        pass
        #raise NotImplementedError

    def contextMenuEvent(self, event):
        """
        Triggered when the user right clicks on the search widget.

        :type event: QtCore.QEvent
        :rtype: None
        """
        #self.showContextMenu()
        pass

    def showContextMenu(self):
        """
        Create and show the context menu for the search widget.

        :rtype QtWidgets.QAction
        """
        pass
        #menu = QtWidgets.QMenu(self)

        #subMenu = self.createStandardContextMenu()
        #subMenu.setTitle("Edit")
        #menu.addMenu(subMenu)

        #subMenu = self.createSpaceOperatorMenu(menu)
        #menu.addMenu(subMenu)

        #point = QtGui.QCursor.pos()
        #action = menu.exec_(point)

        #return action

    def setIcon(self, icon):
        """
        Set the icon for the search widget.

        :type icon: QtWidgets.QIcon
        :rtype: None
        """
        self._iconButton.setIcon(icon)

    def setIconColor(self, color):
        """
        Set the icon color for the search widget icon.

        :type color: QtGui.QColor
        :rtype: None
        """
        icon = self._iconButton.icon()
        icon = Icon(icon)
        icon.setColor(color)
        self._iconButton.setIcon(icon)

    def updateIconColor(self):
        """
        Update the icon colors to the current foregroundRole.

        :rtype: None
        """
        color = self.palette().color(self.foregroundRole())
        color = Color.fromColor(color)
        self.setIconColor(color)

    def settings(self):
        """
        Return a dictionary of the current widget state.

        :rtype: dict
        """
        settings = {"text": self.text()}
        return settings

    def setSettings(self, settings):
        """
        Restore the widget state from a settings dictionary.

        :type settings: dict
        :rtype: None
        """
        text = settings.get("text", "")
        self.setText(text)

    def resizeEvent(self, event):
        """
        Reimplemented so the icon maintains the same height as the widget.

        :type event:  QtWidgets.QResizeEvent
        :rtype: None
        """
        QtWidgets.QLineEdit.resizeEvent(self, event)

        self.setTextMargins(self.height(), 0, 0, 0)
        size = QtCore.QSize(self.height(), self.height())

        self._iconButton.setIconSize(size)
        self._iconButton.setFixedSize(size)
    
class ListWidget(QtWidgets.QListWidget):
    """custom class so we can subclass the key press and other events required"""

    def __init__(self, parent):
        super(ListWidget, self).__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        """implement key press event"""
        super(ListWidget, self).keyPressEvent(event)

        # execute the actions from the parent window
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.executeAction()

    def focusInEvent(self, event):
        """implement the focus in event"""
        super(ListWidget, self).focusInEvent(event)

        count = self.count()
        if not count:
            return

        selItems = self.selectedItems()
        if len(selItems):
            return

        item = self.item(0)
        item.setSelected(True)

class ListView(QtWidgets.QListView):
    """custom class so we can subclass the key press and other events required"""

    def __init__(self, parent):
        super(ListView, self).__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        """implement key press event"""
        super(ListView, self).keyPressEvent(event)

        # open files on Return pressed
        if event.key() == QtCore.Qt.Key_Return:
            self.parent.openFile()

    def focusInEvent(self, event):
        """implement the focus in event"""
        super(ListView, self).focusInEvent(event)

        if not self.model():
            return

        indices = self.selectedIndexes()
        if len(indices):
            return

        if not len(self.model().items):
            return

        index = self.model().index(0, 0)
        self.selectionModel().select(index, QtCore.QItemSelectionModel.Select)