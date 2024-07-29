######################################
############# IMPORTS ################
######################################
from fstrings import f
from pyside.qt_wrapper import QtCore, QtWidgets
import filepath as filepathObj


######################################
############# DEFINES ################
######################################
SETTINGS_FILE = filepathObj.UserToolsPath().join('mayaUISettings.ini')


######################################
############# CLASSES ################
######################################
class Settings(object):
    '''
    Class for saving and getting settings.
    '''
    def __init__(self, filepath=None, create=True):
        if filepath:
            self._filepath = filepathObj.FilePath(filepath)
            if not create:
                if not self._filepath.exists() and \
                    not self._filepath.isWritable():
                    self._filepath = SETTINGS_FILE

        self._settings = QtCore.QSettings(str(self._filepath),
                                           QtCore.QSettings.IniFormat)

        #these lists give optional ways to either exclude widgets from a recursive save or force certain widgets to save
        self._force_widget_list = []
        self._exclude_widget_list = []

        #This is automatically populated during recursive save state to avoid saving widgets multiple times (once per parent)
        self._savedWidgets = []
        self._restoredWidgets = []

    def forceWidgetToSave(self, widget):
        """adds the widget to a list so its forced to save"""
        self._force_widget_list.append(widget)

    def excludeWidgetFromSave(self, widget):
        """adds the widget that's set to exclude when doing recursion"""
        self._exclude_widget_list.append(widget)

    def getSettings(self):
        '''Returns the C{QSettings} object.'''
        return self._settings

    def setValue(self, key, value, groups=[]):
        '''
        Sets the value of the given key. Each string in the C{groups} list
        creates a new subgroup to store the entry.

        e.g. setValue('isMovable', False, groups=['myWindow', 'myTabWidget'])
        '''
        for group in groups:
            self._settings.beginGroup(group)

        self._settings.setValue(key, value)

        for group in groups:
            self._settings.endGroup()

        # Ensures it gets saved out right away
        self._settings.sync()

    def getValue(self, key, groups=[]):
        '''Returns the value of the given key in the given group.'''
        for group in groups:
            self._settings.beginGroup(group)

        value = self._settings.value(key)

        if isinstance(value, list):
            for index, v in enumerate(value):
                # Special case for boolean values
                if v == 'true':
                    value[index] = True
                elif v == 'false':
                    value[index] = False
        else:
            # Special case for boolean values
            if value == 'true':
                value = True
            elif value == 'false':
                value = False

        for group in groups:
            self._settings.endGroup()

        return value

    def removeValue(self, key, groups=[]):
        '''
        Removes the value of the given key. Each string in the C{groups} list
        creates a new subgroup to store the entry.

        e.g. removeValue('isMovable', groups=['myWindow', 'myTabWidget'])
        '''
        for group in groups:
            self._settings.beginGroup(group)

        self._settings.remove(key)

        for group in groups:
            self._settings.endGroup()

        # Ensures it gets saved out right away
        self._settings.sync()

    def saveGeometry(self, widget):
        '''
        Saves the geometry and dock states of the given widget.
        If recursive, saves the geometry of all child widgets as well.

        Currently supported type of widgets:
            QWidget     (geometry)
            QDockWidget (geometry, floating)
            QMainWindow (geometry, state)
        '''
        self._saveGeometry(widget)
        self._settings.sync()

    def saveGeometryByName(self, parentWidget, widgetName):
        '''
        Finds the widget specified by parent widget and the widget name,
        then saves its geometry and dock states.
        '''
        widget = parentWidget.findChildren(QtWidgets.QWidget, name=widgetName)
        if widget:
            widget = widget[0]
            self.saveGeometry(widget)

    def _saveGeometry(self, widget, doForceSaves=True):
        '''Helper method for saving geometry recursively.'''

        self._settings.beginGroup(widget.objectName())

        # Save QWidget geometry
        if widget.inherits('QWidget'):
            self._settings.setValue('geometry', widget.saveGeometry())


        # Save QMainWindow state (toolbars and dockwidgets)
        if widget.inherits('QMainWindow'):
            self._settings.setValue('state', widget.saveState())

        # Save QDockWidget state (floating)
        if widget.inherits('QDockWidget'):
            self._settings.setValue('floating', int(widget.isFloating()))

        #only if we're not recursing, go through and force the saving of widgets
        if doForceSaves:
            for child in self._force_widget_list:
                self._saveGeometry(child, doForceSaves=True)

        self._settings.endGroup()

    def restoreGeometry(self, widget):
        '''
        Restores the geometry and dock states of the given widget.
        If recursive, restores the geometry of all child widgets as well.

        Currently supported type of widgets:
            QWidget     (geometry)
            QDockWidget (geometry, floating)
            QMainWindow (geometry, state)
        '''
        self._restoreGeometry(widget)

    def restoreGeometryByName(self, parentWidget, widgetName):
        '''
        Finds the widget specified by parent widget and the widget name,
        then restores its geometry and dock states.
        '''
        widget = parentWidget.findChildren(QtWidgets.QWidget, name=widgetName)
        if widget:
            widget = widget[0]
            self.restoreGeometry(widget)

    def _restoreGeometry(self, widget, doForceRestores=True ):
        '''Helper method for restoring geometry recursively.'''
        self._settings.beginGroup(widget.objectName())

        # Restore QWidget geometry
        if widget.inherits('QWidget'):

            try:
                geometry = self._settings.value('geometry').toByteArray()
            except:
                geometry = self._settings.value('geometry')

            if geometry:
                widget.restoreGeometry(geometry)

        # Restore QMainWindow state
        if widget.inherits('QMainWindow'):
            try:
                state = self._settings.value('state').toByteArray()
                widget.restoreState(state)
            except:
                state = self._settings.value('state')

            if state:
                widget.restoreState(state)

        # Restore QDockWidget state
        if widget.inherits('QDockWidget'):
            widget.setFloating(int(self._settings.value('floating', defaultValue=False)))

        if doForceRestores:
            for child in self._force_widget_list:
                self._restoreGeometry(child, doForceRestores=False)

        self._settings.endGroup()

    def saveState(self, widget, recursive=False):
        '''
        Saves the states of the given widget.
        If recursive, saves the states of all child widgets as well.

        Currently supported type of widgets:
            QComboBox (selected item text)
            QTabWidget (selected tab text, tab order)
            QCheckBox (check state)
            QAction (check state)
            QSpinBox
            QDoubleSpinBox
            QRadioButton (check state)
            UIFilePathWidget
            UIResolutionWidget
            UISliderSpinBox
            UISliderDoubleSpinBox
        '''
        self._savedWidgets = []
        self._saveState(widget, recursive=recursive)
        self._settings.sync()

    def _saveState(self, widget, recursive=False, doForceSaves=True):

        # Avoid resaving the same widget over and over (is this risky in recursive? I don't *think* so...)
        if widget in self._savedWidgets:
            return
        else:
            self._savedWidgets.append(widget)

        '''Helper method for saving states recursively.'''
        self._settings.beginGroup(widget.objectName())

        # Save combo box selected item
        if widget.inherits('QComboBox'):
            self._settings.setValue('currentText', widget.currentText())

        # QTabWidget
        if widget.inherits('QTabWidget'):
            # Save tab order
            if widget.isMovable():
                tabs = []
                for index in range(widget.count()):
                    tabs.append(widget.tabText(index))
                self._settings.setValue('tabOrder', tabs)

            # Save selected tab
            self._settings.setValue('currentTab', widget.tabText(widget.currentIndex()))

        # QCheckBox
        if widget.inherits('QCheckBox'):
            self._settings.setValue(f('{x}_checkState',x=widget.text()), widget.checkState())

        # QAction
        if widget.inherits('QAction') and widget.isCheckable():
            self._settings.setValue('isChecked', widget.isChecked())

        # QSpinBox and QDoubleSpinBox
        if widget.inherits('QSpinBox') or widget.inherits('QDoubleSpinBox'):
            self._settings.setValue('value', widget.value())
            
        # QRadioButton
        if widget.inherits('QRadioButton'):
            self._settings.setValue('value', widget.isChecked())

        if recursive:
            if widget.inherits('QMenu'):
                children = widget.actions()
            else:
                children = widget.findChildren(QtWidgets.QWidget)

            for child in children:
                if child in self._exclude_widget_list:
                    continue
                self._saveState(child, recursive=recursive)

        elif doForceSaves==True:
            for child in self._force_widget_list:
                self._saveState(child, recursive=False, doForceSaves=False)

        self._settings.endGroup()

    def restoreState(self, widget, recursive=False):
        '''
        Restores the states of the given widget.
        If recursive, restores the states of all child widgets as well.

        Currently supported type of widgets:
            QComboBox (selected item text)
            QTabWidget (selected tab text, tab order)
            QCheckBox (check state)
            QAction (check state)
            QSpinBox
            QDoubleSpinBox
            QRadioButton (check state)
            UIFilePathWidget
            UIResolutionWidget
            UISliderSpinBox
            UISliderDoubleSpinBox

        '''
        self._restoredWidgets = []
        self._restoreState(widget, recursive=recursive)

    def _restoreState(self, widget, recursive=False, doForceRestores=True):

        try:
            # Avoid restoring the same widget over and over (is this risky in recursive? I don't *think* so...)
            if widget in self._restoredWidgets:
                return
            else:
                self._restoredWidgets.append(widget)
    
            self._settings.beginGroup(widget.objectName())
    
            # Restore combo box selected item
            if widget.inherits('QComboBox'):
                text = self._settings.value('currentText')
                if text:
                    for index in range(widget.count()):
                        if text == widget.itemText(index):
                            widget.setCurrentIndex(index)
                            break
    
            # QTabWidget
            if widget.inherits('QTabWidget'):
                # Restore tab order
                if widget.isMovable():
                    tabs = self._settings.value('tabOrder')
                    if tabs:
                        for toIndex in range(len(tabs)):
                            for fromIndex in range(widget.count()):
                                if widget.tabText(fromIndex) == tabs[toIndex] and \
                                    fromIndex != toIndex:
                                    widget.tabBar().moveTab(fromIndex, toIndex)
                                    break
    
                # Restore selected tab
                text = self._settings.value('currentTab')
                if text:
                    for index in range(widget.count()):
                        if text == widget.tabText(index):
                            widget.setCurrentIndex(index)
                            break
    
            # QCheckBox
            if widget.inherits('QCheckBox'):
                checkState = self._settings.value(f('{x}_checkState',x=widget.text()))
                if checkState is not None:
                    widget.setCheckState(QtCore.Qt.CheckState(int(checkState)))
    
            # QAction
            if widget.inherits('QAction') and widget.isCheckable():
                isChecked = self._settings.value('isChecked')
                if isChecked is not None:
                    widget.setChecked(isChecked == "true")
    
            # QSpinbox
            if widget.inherits('QSpinBox'):
                value = self._settings.value('value')
                if value is not None:
                    widget.setValue(int(value))
    
            # QDoubleSpinBox
            if widget.inherits('QDoubleSpinBox'):
                value = self._settings.value('value')
                if value is not None:
                    widget.setValue(float(value))
                    
            # QRadioButton
            if widget.inherits('QRadioButton'):
                value = self._settings.value('value')
                if value is not None:
                    widget.setChecked(int(value))      
    
            if recursive:
                if widget.inherits('QMenu'):
                    children = widget.actions()
                else:
                    children = widget.findChildren(QtWidgets.QWidget)
    
                for child in children:
                    if child in self._exclude_widget_list:
                        continue
    
                    self.restoreState(child, recursive=recursive)
            # doForceRestores logic prevents infinite loops
            elif doForceRestores:
                for child in self._force_widget_list:
                    self.restoreState(child, recursive=False, doForceRestores=False)
    
            self._settings.endGroup()
        
        except:
            pass

    def removeGroup(self, group):
        ''' Remove group '''
        self._settings.remove(group)
