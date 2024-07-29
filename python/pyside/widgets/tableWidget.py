from pyside.qt_wrapper import QtCore, QtWidgets
import pyside.widgets.uiWidgetUtil as uiWidgetUtil

class UITableWidget(QtWidgets.QTableWidget):

    def __init__(self):
        super(UITableWidget, self).__init__()

        #initialize the utility helper
        self.util = uiWidgetUtil.WidgetUtil(self)

        self.__size_ratios = []

    @property
    def columns(self):
        """returns a string list of the column labels"""
        names = []
        columnCount = self.columnCount()
        for i in range(columnCount):
            names.append(self.horizontalHeaderItem(i).text())
        return names

    @columns.setter
    def columns(self, names):
        """sets the columns labels and column count based on the string list passed in"""
        if not isinstance(names, list):
            raise Exception("A string list is required with the UITableWidget.columns property call")

        self.setColumnCount(len(names))
        self.setHorizontalHeaderLabels(names)
        self.resizeColumns()

    @property
    def size_ratios(self):
        return self.__size_ratios

    @size_ratios.setter
    def size_ratios(self, sizes):
        self.__size_ratios = sizes

    def hideRowLabels(self):
        self.verticalHeader().setVisible(False)

    def showRowLabels(self):
        self.verticalHeader().setVisible(True)

    def hideColumnLabels(self):
        self.horizontalHeader().setVisible(False)

    def showColumnLabels(self):
        self.horizontalHeader().setVisible(True)

    def disableColumnSelection(self, column):

        for i in range(self.rowCount()):
            item = self.item(i, column)
            if not item:
                continue
            item.setFlags(QtCore.Qt.ItemIsEnabled)

    def disableRowSelection(self, row):

        for i in range(self.columnCount()):
            item = self.item(row, i)
            if not item:
                continue
            item.setFlags(QtCore.Qt.ItemIsEnabled)

    def disableColumnEditing(self, column):

        for i in range(self.rowCount()):
            item = self.item(i, column)
            if not item:
                continue
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def disableRowEditing(self, row):

        for i in range(self.columnCount()):
            item = self.item(row, i)
            if not item:
                continue
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

    def resizeEvent(self, event):
        """resize will ensure the headers maintain their size based on the table width"""
        self.resizeColumns()

    def resizeColumns(self):

        size = self.size()
        width = float(size.width()-25)

        count = self.columnCount()

        if self.__size_ratios and not len(self.__size_ratios) == count:
            raise Exception("Size ratio list needs to be the same count as the columns")

        ratio = 1.0 / float(count)

        for i in range(count):
            if self.__size_ratios:
                ratio = self.__size_ratios[i]
            self.setColumnWidth(i, width * ratio)

