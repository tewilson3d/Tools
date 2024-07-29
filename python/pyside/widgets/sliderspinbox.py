from pyside.qt_wrapper import QtCore, QtWidgets

class UISliderSpinBoxWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, minimum=1, maximum=100, startingValue=100, increment=1, spinBoxOnRight=True ):

        # Init all the standard widget stuff
        super(UISliderSpinBoxWidget, self).__init__( parent )

        # Store init parameters
        self.startingValue = startingValue
        self.minimum = minimum
        self.maximum = maximum
        self.increment = increment
        self.spinBoxOnRight = spinBoxOnRight

        # Setup UI
        self._setupResolutionUi()
        self._connectCallbacks()

    def value(self):
        return int(self.spinBox.value())

    def setValue(self, newValue):
        self.slider.setValue(newValue)

    def _setupResolutionUi(self):
        # Create a horizontal layout
        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(0,0,0,0)

        self.setLayout(horizontalLayout)
        #self.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed )
        #self.setMaximumHeight(30)

        self._createMainWidgets()

        if self.spinBoxOnRight:
            horizontalLayout.addWidget(self.slider)
            horizontalLayout.addWidget(self.spinBox)
        else:
            horizontalLayout.addWidget(self.spinBox)
            horizontalLayout.addWidget(self.slider)

        # Setup the values
        self._initializeWidgetValues()

    def _createMainWidgets(self):
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spinBox = QtWidgets.QSpinBox()

    def _initializeWidgetValues(self):
        self.slider.setMinimum(self.minimum)
        self.slider.setMaximum(self.maximum)
        self.slider.setTickInterval(self.increment)
        self.slider.setValue(self.startingValue)

        self.spinBox.setMinimum(self.minimum)
        self.spinBox.setMaximum(self.maximum)
        self.spinBox.setSingleStep(self.increment)
        self.spinBox.setValue(self.startingValue)
        #self.resolutionDisplay.setAlignment( QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter )
        #self.resolutionDisplay.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed )


    def _connectCallbacks(self):
        self.slider.valueChanged.connect(self._updateBlendSpinbox)
        self.spinBox.editingFinished.connect(self._updateBlendSlider)

    def _updateBlendSpinbox(self, newValue):
        self.spinBox.setValue(newValue)

    def _updateBlendSlider(self):
        newValue = self.spinBox.value()
        self.slider.setValue( newValue )