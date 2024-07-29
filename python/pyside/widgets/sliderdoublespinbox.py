from pyside.qt_wrapper import QtCore, QtWidgets
import uiSliderSpinBoxWidget

class UISliderDoubleSpinBoxWidget(uiSliderSpinBoxWidget.UISliderSpinBoxWidget):

    def __init__(self, parent=None, minimum=0, maximum=1, startingValue=1.0, increment=0.1, spinBoxOnRight=True ):

        # Init all the standard widget stuff
        super(UISliderDoubleSpinBoxWidget, self).__init__( parent, minimum, maximum, startingValue, increment, spinBoxOnRight )

    def _createMainWidgets(self):
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spinBox = QtWidgets.QDoubleSpinBox()

    def value(self):
        return self.spinBox.value()

    def setValue(self, newValue):
        self.slider.setValue( int(newValue*100) )

    def _initializeWidgetValues(self):
        self.slider.setMinimum(int(self.minimum*100))
        self.slider.setMaximum(int(self.maximum*100))
        self.slider.setTickInterval(int(self.increment*100))
        self.slider.setValue(int(self.startingValue*100))

        self.spinBox.setMinimum(self.minimum)
        self.spinBox.setMaximum(self.maximum)
        self.spinBox.setSingleStep(self.increment)
        self.spinBox.setValue(self.startingValue)
        #self.resolutionDisplay.setAlignment( QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter )
        #self.resolutionDisplay.setSizePolicy( QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed )


    def _updateBlendSpinbox(self, newValue):
        self.spinBox.setValue(newValue/100.0)

    def _updateBlendSlider(self):
        newValue = self.spinBox.value()
        self.slider.setValue( int(newValue*100) )