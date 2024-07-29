######################################
############# IMPORTS ################
######################################
import sys
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets

######################################
############# DEFINES ################
######################################
# Only need column count to be 1 for now.
COLUMN_COUNT = 1

######################################
############# CLASSES ################
###################################### 
class TreeItem(object):
    '''
    Tree item class. 
    Subclass and override data() function to return different types of data.
    
    Args:
        data (object): Anything needs to be data.
    
    Kwargs:
        parent (:py:class: `core.qt.widgets.TreeItem`): Parent item.
    '''
    def __init__(self, data, parent=None):
        if parent:
            if not isinstance(parent, self.__class__):
                raise RuntimeError("Invalid parent, {0} type expected, got {1}.".format(self.__class__.__name__, parent))
        self._parent = parent
        self._itemData = data
        self._childItems = []
        
    @property
    def childItems(self):
        '''
        Property childItems getter. Get all the children nodes.
        '''
        return self._childItems
    
    @property
    def parent(self):
        '''
        Property parent getter. Get parent node.
        '''
        return self._parent
    
    @parent.setter
    def parent(self, newParent):
        '''
        Property parent setter. Set Parent node.
        '''
        self._parent = newParent
    
    @property
    def childCount(self):
        '''
        Property child count getter.
        '''
        return len(self._childItems)
    
    @property
    def columnCount(self):
        '''
        Property column count getter.
        '''
        return COLUMN_COUNT 
    
    @property
    def data(self):
        '''
        Property data getter.
        '''
        return self._itemData    
        
    def child(self, row):
        '''
        Get child at row.
        
        Args:
            row (int) : row number.
            
        Returns:
            (lib.qt.widgets.uiTreeModel.TreeItem) : item at row.
        '''
        try:
            return self._childItems[row]
        except IndexError:
            return None
    
    @property
    def row(self):
        '''
        Get row number.
        
        Returns:
            (int) : row number.
        '''
        if self._parent:
            return self._parent.childItems.index(self)
        return -1
        
    def setData(self, value):
        '''
        Set data to new value.
        
        Args:
            value (object) : new value.
        '''
        self._itemData = value
    
    def addChild(self, item):
        '''
        Add new child item.
        
        Args:
            item (:py:class:`lib.qt.widget.uiTreeModel.TreeItem`) : new child item.
        '''
        self._childItems.append(item)
        
    def removeChild(self, position):
        '''
        Remove child at position.
        
        Args:
            position (int) : position to remove child.
            
        Returns:
            (bool) : remove succeed or not.
        '''
        if position < 0 or position > len(self._childItems):
            return False
        removedItem = self._childItems.pop(position)
        del removedItem
        return True
    
    def insertChild(self, position, childData):
        '''
        Insert child at position with new data.
        
        Args:
            position (int)     : position to insert.
            childData (object) : new data for child.
            
        Returns:
            (bool)  : insert succeed or not.
        
        '''
        self._childItems.insert(position, self.__class__(childData, parent=self))
        return True
    
    def clearChildren(self):
        '''
        Clear all the children.
        '''
        for child in self._childItems:
            if child.childCount > 0:
                child.clearChildren()
            child.parent = None
        self._childItems = []
        
        
class TreeItemModel(QtCore.QAbstractItemModel):
    '''
    Tree Item Model. Subclass of :py:class:`QtCore.QAbstractItemModel`.
    
    Args:
        data (object)              : data need to be stored in the model.
        
    Kwargs:
        parent(QtCore.QObject)     : parent for model.
        headerData (tuple/list)    : header data for model. If set with list or tuple, column count will be the len of headerData. 
                                     If not set, column count will be COLUMN_COUNT.
    '''
    def __init__(self, data, parent=None, headerData=None):
        super(TreeItemModel, self).__init__(parent=parent)
        self._rootItem = TreeItem(None)
        self._headerData = headerData
        self.setupModelData(self._rootItem, data)
         
    def setupModelData(self, root, data):
        '''
        Have to implement this for storing data in the model.
        
        Args:
            root (TreeItem) : root item for data.
            data (object)   : data to store.
            
        Examples:
            A implementation of this method for dictionary data type would be like this.
            For this case, data for each item will be "key:item".
            
            def setupModelData(self, root, data):
                for key, item in data.items():
                    if isinstance(item, dict):
                        parentItem = TreeItem("{0}: {1}".format(key, item), root)
                        self.setupModelData(parentItem, item)
                    else:
                        TreeItem("{0}: {1}".format(key, item), root)
        '''
        raise NotImplementedError()
    
    def getItem(self, index):
        '''
        Get item at index. If can not found item at index, always return root item.
        
        Args:
            index (QtCore.QModelIndex) : item at index.
            
        Returns:
            (TreeItem) : item at index.
        '''
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self._rootItem
    
    ########### Override methods ############
    def rowCount(self, parent=QtCore.QModelIndex()):
        '''
        Row count.
        
        Kwargs:
            parent (QtCore.QModelIndex) : parent model index for current item.
            
        Returns:
            (int) : row count.
        '''
        if parent.isValid() and parent.column() != 0:
            return 0
        
        parentItem = self.getItem(parent)   
        return parentItem.childCount
    
    def parent(self, index):
        '''
        Parent.
        
        Args:
            index (QtCore.QModelIndex) : get parent index for item at index.
            
        Returns:
            (QtCore.QModelIndex) : parent model index.
        '''
        item = self.getItem(index)
        parentItem = item.parent
        
        if parentItem == self._rootItem or not parentItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row, 0, parentItem)
    
    def index(self, row, column, parent=QtCore.QModelIndex()):
        '''
        Get model index at row, column.
        
        Args:
            row (int)                   : row number.
            column(int)                 : column number.
            
        Kwargs:
            parent (QtCore.QModelIndex) : parent model index
            
        Returns:
            (QtCore.QModelIndex)        : model index.
        '''
        parentItem = self.getItem(parent)
        childItem = parentItem.child(row)
        
        if childItem:
            return self.createIndex(row, column, childItem)
        return QtCore.QModelIndex()
    
    def columnCount(self, parent=QtCore.QModelIndex()):
        '''
        Get column count.
        
        Kwargs:
            parent (QtCore.QModelIndex) : parent model index
            
        Returns:
            (int) : column count.
        '''
        if isinstance(self._headerData, (tuple, list)):
            return len(self._headerData)
        return COLUMN_COUNT
    
    def data(self, index, role=QtCore.Qt.DisplayRole):
        '''
        Get data at index. 
        It only implements most simple function, which is just return the data stored in items.
        This can be overwritten to get more functions.
        
        Args:
            index (QtCore.QModelIndex) : model index to get data.
            
        Kwargs:
            role (QtCore.Qt.Role)      : roles for data.
            
        Returns:
            (object) : data.
        '''
        if not index.isValid():
            return None
        
        item = index.internalPointer()
        
        if not item:
            return None
        
        if role == QtCore.Qt.DisplayRole:
            return item.data
        
        return None
    
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        '''
        Set data.
        
        Args:
            index (QtCore.QModelIndex) : set data for index.
            value (object)             : data to set.
            
        Kwargs:
            role (QtCore.Qt.Role)      : role to set.
        '''
        item = self.getItem(index)
        item.setData(value)
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        '''
        Header data to display.
        
        Args:
            section (int)                       : Column number of the header.
            orientation (QtCore.Qt.Orientation) : Horizontal or vertical.
            
        Kwargs:
            role (QtCore.Qt.Role)               : Role.
        '''
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if isinstance(self._headerData, (list, tuple)):
                if section > len(self._headerData):
                    return None
                return self._headerData[section]
            else:
                return self._headerData
        return None
    
    def flags(self, index):
        '''
        Flags for index.
        
        Args:
            index (QtCore.QModelIndex) : index.
            
        Returns:
            (QtCore.Qt.ItemFlags)
        '''
        if not index.isValid():
            return QtCore.Qt.NoItemFlags
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        
    
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        '''
        Insert rows. This only inserts None items for now. Need to be overwritten in inherient class.
        
        Args:
            position (int) : start to insert from.
            rows     (int) : number of items to insert.
            
        Kwargs:
            parent   (QtCore.QModelIndex) : parent index.
            
        Returns:
            (bool)  : insert succeed or not.
        '''
        parentItem = self.getItem(parent)
        self.beginInsertRows(parent, position, position + rows - 1)
        
        success = True
        for row in range(rows):
            childCount = parentItem.childCount
            # put data to be None for now.
            if not parentItem.insertChild(position, None):
                success = False
        self.endInsertRows()
        return success
    
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        '''
        Remove rows.
        
        Args:
            position (int) : start to remove from.
            rows     (int) : number of items to insert.
            
        Kwargs:
            parent   (QtCore.QModelIndex) : parent index.
            
        Returns:
            (bool)  : remove succeed or not.
        '''        
        parentItem = self.getItem(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        success = True
        for row in range(rows):
            if not parentItem.removeChild(position):
                success = False
        self.endRemoveRows()
        return success
        
    
### Example : Try a dict data for model ###

class TestTreeModel(TreeItemModel):
    def __init__(self, data, parent=None, headerData=None):
        super(TestTreeModel, self).__init__(data, parent=parent, headerData=headerData)
        
    def setupModelData(self, root, data):
        for key, item in data.items():
            if isinstance(item, dict):
                parentItem = TreeItem("{0}: {1}".format(key, item), root)
                root.addChild(parentItem)
                self.setupModelData(parentItem, item)
            else:
                root.addChild(TreeItem("{0}: {1}".format(key, item), root))
                
 
def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    layout = QtWidgets.QHBoxLayout()
    dialog.setLayout(layout)
    tm = TestTreeModel({'a':{'d':3},'b':2,'c':3}, headerData=['header1', 'header2'])
    tv = QtWidgets.QTreeView()
    
    tv.setModel(tm) 
    layout.addWidget(tv)
    dialog.show()
    sys.exit(app.exec_())