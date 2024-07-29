from pyside.qt_wrapper import QtGui
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets

class LineEdit(QtWidgets.QLineEdit):
    '''Custom line edit class that supports placeholder text.
    '''
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)

        # Private variables
        self.__placeholderText = ''
        self.__placeholding = True
        self.__defaultPalette = self.palette()

    def setPlaceholderText(self, text):
        '''Sets the placeholder text.
        '''
        self.__placeholderText = text
        if text and self.__placeholding and not self.hasFocus():
            self.setText(text)

    def placeholderText(self):
        '''Returns the current placeholder text.'''
        return self.__placeholderText

    def focusOutEvent(self, event):
        '''Overriden event handler called when this widget loses focus.
           Sets the placeholder text if there is currently no user input.
        '''
        super(LineEdit, self).focusOutEvent(event)

        if not self.__placeholderText:
            return

        if not self.text():
            self.__placeholding = True
            if self.__placeholderText:
                self.setText(self.__placeholderText)

    def focusInEvent(self, event):
        '''Overriden event handler called when this widget gets focus.
           Sets the placeholder text if there is currently no user input.
        '''
        super(LineEdit, self).focusInEvent(event)
        
        if not self.__placeholding:
            return
        else:
            self.__placeholding = False
            self.setText('')

    def setPalette(self, palette):
        '''Overridden method. Sets a darker text color when placeholder text is
           displayed.
        '''
        self.__defaultPalette = palette

        if self.__placeholding:
            palette = QtGui.QPalette(palette)
            palette.setColor(
                QtGui.QPalette.Text,
                self.__defaultPalette.color(QtGui.QPalette.Text)#.dark()
            )

        super(LineEdit, self).setPalette(palette)

    def setText(self, text):
        '''Overridden method to set the text on the line edit.
           Updates the color palette before setting the text.
        '''
        self.setPalette(self.__defaultPalette)
        super(LineEdit, self).setText(text)

    def text(self):
        '''Overridden method to return the current text in the line edit.
        '''
        if self.__placeholding:
            return ''

        return super(LineEdit, self).text()
