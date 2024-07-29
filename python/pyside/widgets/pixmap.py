######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtGui
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets

from pyside.widgets.color import Color


######################################
############# CLASSES ################
######################################
class Pixmap(QtGui.QPixmap):

    def __init__(self, *args):
        QtGui.QPixmap.__init__(self, *args)

        self._color = None

    def setColor(self, color):
        """
        :type color: QtGui.QColor
        :rtype: None
        """
        if isinstance(color, basestring):
            color = Color.fromString(color)

        if not self.isNull():
            painter = QtGui.QPainter(self)
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
            painter.setBrush(color)
            painter.setPen(color)
            painter.drawRect(self.rect())
            painter.end()