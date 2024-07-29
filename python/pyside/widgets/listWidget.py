from pyside.qt_wrapper import QtCore, QtWidgets
import pyside.widgets.widgetutil as widgetUtil
import pyside.widgets.hotkeyUtil as hotkeyUtil


class ListWidget(QtWidgets.QListWidget):

    def __init__(self):
        super(UIListWidget, self).__init__()

        #initialize the utility helper
        self.util = widgetUtil.WidgetUtil(self)
        self.hotkey_util = hotkeyUtil.HotkeyUtil()

    def disableSelection(self):
        """disables the selection of all items"""
        for i in range(self.count()):
            item = self.item(i)
            if not item:
                continue
            item.setFlags(QtCore.Qt.NoItemFlags | QtCore.Qt.ItemIsEnabled)

    def keyPressEvent(self, event):
        super(UIListWidget, self).keyPressEvent(event)
        self.hotkey_util.keyPressEvent(event)