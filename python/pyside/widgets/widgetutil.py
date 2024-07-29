from pyside.qt_wrapper import QtCore, QtWidgets

class WidgetUtil(object):

    def __init__(self, widget):

        if not isinstance(widget, QtWidgets.QWidget):
            raise Exception("Any widget passed into WidgetFn, must be a sublcass of QtWidgets.QWidget")

        self._widget = widget
        self._recursive_settings = False
        self._settings = None

    @property
    def widget(self):
        return self._widget

    @widget.setter
    def widget(self, widget):
        self._widget = widget

    @property
    def settings(self):
        return self._settings

    @property
    def recursive_settings(self):
        return self._recursive_settings

    @recursive_settings.setter
    def recursive_settings(self, value):
        """specify whether to be recursive by default or not"""
        self._recursive_settings = value

    @property
    def title(self):
        return self.widget.windowTitle()

    @title.setter
    def title(self, title):
        self.widget.setWindowTitle(title)

    @property
    def size(self):
        return self.widget.width(), self.widget.height()

    @size.setter
    def size(self, size):
        geo = self.widget.geometry()
        self.widget.setGeometry(geo.x(), geo.y(), size[0], size[1])

    @property
    def width(self):
        return self.widget.width()

    @width.setter
    def width(self, width):
        geo = self.widget.geometry()
        self.widget.setGeometry(geo.x(), geo.y(), width, geo.height())

    @property
    def height(self):
        return self.widget.height()

    @height.setter
    def height(self, height):
        geo = self.widget.geometry()
        self.widget.setGeometry(geo.x(), geo.y(), geo.width(), height)

    def initializeSettings(self, name):
        import pyside.settings as settings
        import filepath        

        settings_path =  filepath.UserToolsPath().join(name+ '_UISettings.ini')
        self._settings = settings.Settings(filepath=settings_path)

    def getValue(self, valueName, group):
        """ gets the value of the given widget attribute """
        if self._settings:
            return self._settings.getValue(valueName, [group])

    def setValue(self, key, value, groups=[]):
        """ sets the value """
        if self._settings:
            self._settings.setValue(key, value, groups)
    
    def getSettings(self):
        ''' gets qsettings object '''
        if self._settings:
            return self._settings.getSettings()
        
    def removeGroupValue(self, group):
        ''' removes the given group from the tool settings.ini file '''
        self._settings.removeGroup(group)
        
    def saveSettings(self):
        """saves the UI settings"""
        if self.settings:
            self.settings.saveGeometry(self.widget)
            self.settings.saveState(self.widget, recursive=self.recursive_settings)

    def loadSettings(self):
        """restore the UI settings"""
        if self.settings:
            self.settings.restoreGeometry(self.widget)
            self.settings.restoreState(self.widget, recursive=self.recursive_settings)
