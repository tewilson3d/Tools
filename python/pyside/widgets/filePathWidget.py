''' This widget provides an easy and foolproof way to select power of two resolutions '''

from pyside.qt_wrapper import QtCore, QtGui, QSignal, QtWidgets
import filepath

class FilePathWidget(QtWidgets.QWidget):

    pathChanged = QSignal(filepath.FilePath)

    def __init__(self, parent=None, startingPath="", useFolder=False, fileFilter="" ):
        # Init all the standard widget stuff
        super(FilePathWidget, self).__init__( parent )

        # Store init parameters
        self.startingPath = filepath.FilePath(startingPath)
        self.path = self.startingPath
        self.useFolder = useFolder
        self.fileFilter = fileFilter

        # Setup UI
        self._setupFilePathUi()
        self._connectCallbacks()

    def text(self):
        return self.lineEditPath.text()

    def setText(self, text):
        self.lineEditPath.setText( text )
    
    def setStartingPath(self, newPath):
        self.startingPath = filepath.FilePath(newPath)

    def _setupFilePathUi(self):

        # Create a horizontal layout
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(0,0,0,0)
        horizontalLayout.setSpacing(3)

        self.setLayout(horizontalLayout)
        self.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed )
        self.setMaximumHeight(30)

        # Create the widgets
        self.lineEditPath = QtWidgets.QLineEdit( self.startingPath )
        self.pushButtonBrowseFiles = QtWidgets.QPushButton()

        horizontalLayout.addWidget(self.lineEditPath)
        horizontalLayout.addWidget(self.pushButtonBrowseFiles)

        # Make the browse button small
        self.pushButtonBrowseFiles.setMinimumWidth(22)
        self.pushButtonBrowseFiles.setMaximumWidth(22)
        self.pushButtonBrowseFiles.setMaximumHeight(20)

    def _connectCallbacks(self):
        self.pushButtonBrowseFiles.clicked.connect(self._browseForPath)
        self.lineEditPath.textEdited.connect(self._pathEdited)

    def _browseForPath(self):
        if not self.startingPath:
            self.startingPath = filepath.FilePath(self.lineEditPath.text()).dir()
        if self.useFolder:
            newPath, _ = QtWidgets.QFileDialog.getExistingDirectory(parent=self, caption="Please select a folder", dir=self.startingPath)
        else:
            newPath, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption="Please select a file", dir=self.startingPath, filter=self.fileFilter)

        if newPath:
            self.path = filepath.FilePath(newPath)
            self.lineEditPath.setText(self.path)
            self.pathChanged.emit(self.path)

    def _pathEdited(self, newPath):
        self.path = filepath.FilePath(newPath)
        self.pathChanged.emit(self.path)