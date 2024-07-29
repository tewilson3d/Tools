from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QtGui

arrowRightPixmap_xpm = ["11 11 2 1",
                        "  g None",
                        ". g #999999",
                        "  .        ",
                        "  ..       ",
                        "  . .      ",
                        "  .  .     ",
                        "  .   .    ",
                        "  .    .   ",
                        "  .   .    ",
                        "  .  .     ",
                        "  . .      ",
                        "  ..       ",
                        "  .        " ]

arrowDownPixmap_xpm = ["11 11 2 1",
                       "  g None",
                       ". g #999999",
                       "           ",
                       "           ",
                       "           ",
                       "...........",
                       " .       . ",
                       "  .     .  ",
                       "   .   .   ",
                       "    . .    ",
                       "     .     ",
                       "           ",
                       "           " ]


class QCollapsibleFrame(QtWidgets.QFrame):
    def __init__(self, title, parent=None):
        super(QCollapsibleFrame, self).__init__(parent)
        self._collapsed = False
        self._childWidget = None

        self._arrowRightPixmap = QtGui.QPixmap(arrowRightPixmap_xpm)
        self._arrowDownPixmap = QtGui.QPixmap(arrowDownPixmap_xpm)

        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)

        self._frameLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom, self)
        self._labelLayout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)

        self._arrowLabel = QtWidgets.QLabel('arrowLabel', self)
        self._arrowLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self._arrowLabel.setPixmap(self._arrowDownPixmap)

        self._labelLayout.addWidget(self._arrowLabel)

        self._frameLabel = QtWidgets.QLabel('frameLabel', self)
        #self._frameLabel.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        labelFont = self._frameLabel.font()
        labelFont.setBold(True)

        self._frameLabel.setFont(labelFont)
        self._labelLayout.addWidget(self._frameLabel)
        self._frameLayout.addLayout(self._labelLayout)

        self._frameLayout.addStretch()

        self.setTitle(title)

    def title(self):
        return self._frameLabel.text()

    def setTitle(self, title):
        self._frameLabel.setText(title)

    def alignment(self):
        return self._frameLabel.alignment()

    def setAlignment(self, alignment):
        self._frameLabel.setAlignment(alignment)

    def isCollapsed(self):
        return self._collapsed

    def setCollapsed(self, state):
        if self.isCollapsed() == state: 
            return

        if state:
            self.emit(QtCore.SIGNAL('preCollapse()'))
            self._arrowLabel.setPixmap(self._arrowRightPixmap)
            if self.childWidget(): 
                self.childWidget().hide()
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
            self._collapsed = True
            self.emit(QtCore.SIGNAL('collapsed()'))
        else:
            self.emit(QtCore.SIGNAL('preExpand()'))
            self._arrowLabel.setPixmap(self._arrowDownPixmap)
            if self.childWidget(): 
                self.childWidget().show()
            self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
            self._collapsed = False
            self.emit(QtCore.SIGNAL('expanded()'))

        self.emit(QtCore.SIGNAL('toggled(bool)'), state)

    def childWidget(self):
        return self._childWidget


    def setChildWidget(self, child):
        if child == None: return

        if self._childWidget != None:
            self._childWidget.close()
            self._childWidget = None

        self._childWidget = child

        if self._childWidget.parentWidget() != self:
            self._childWidget.setParent(self)

        self._frameLayout.insertWidget(1, self._childWidget, 1)

        if self.isCollapsed():
            if self._childWidget.isVisible():
                self._childWidget.hide()
        else:
            if self._childWidget.isHidden():
                self._childWidget.show()
        self._childWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                        QtWidgets.QSizePolicy.Maximum)

    def toggle(self):
        self.setCollapsed(not self.isCollapsed())

    def collapse(self):
        self.setCollapsed(True)

    def expand(self):
        self.setCollapsed(False)

    def mousePressEvent(self, event):
        if event.button() != QtCore.Qt.LeftButton:
            event.ignore()
            return

        if self._labelLayout.geometry().contains(event.pos()):
            self.toggle()

    def setFrameLayoutMarginSpace(self, left, top, right, bottom, space):
        self._frameLayout.setContentsMargins(left, top, right, bottom)
        self._frameLayout.setSpacing(space)   

    def setLabelLayoutMarginSpace(self, left, top, right, bottom, space):
        self._labelLayout.setContentsMargins(left, top, right, bottom)
        self._labelLayout.setSpacing(space)