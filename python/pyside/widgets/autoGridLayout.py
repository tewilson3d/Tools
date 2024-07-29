"""
Auto Grid Layout

When Adding/Removing widgets from the layout, the layout will be rebuilt to have all children
widgets fit within the size of the grid
"""
######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtWidgets


######################################
############# DEFINES ################
######################################
#: Grid Width Margin
GRID_WIDTH_MARGIN = 50

######################################
############# CLASSES ################
######################################
class AutoGridLayout(QtWidgets.QGridLayout):
    """
    Auto Grid Layout
    
    Automatically determine the proper position of the widgets when adding/removing widgets
    Will respect the width of the grids parent
    """
    def __init__(self,
                 parentObjIn=None):
        super(AutoGridLayout, self).__init__(parentObjIn)
        
        # Last Row
        self.lastRowInt = -1
        
        # Last Column
        self.lastColumnInt = -1
        
        # Current Width
        self.currentWidthInt = 0
        
        
    def addWidget(self,
                  widgetObjIn):
        """
        Add a widget to the layout
        
        Args:
            widgetObjIn (obj): Widget to add
            
        Returns:
            None
        """
        # Is this the first widget being added?
        if self.lastRowInt == -1 and self.lastColumnInt == -1:
            self.currentWidthInt += widgetObjIn.width()
            
            self.lastRowInt += 1
            self.lastColumnInt += 1
            
            super(AutoGridLayout, self).addWidget(widgetObjIn, self.lastRowInt, self.lastColumnInt)
        else:
            # Check the width, make sure this widget will fit in our current row
            if (self.currentWidthInt + widgetObjIn.width()) > self.parent().width() - GRID_WIDTH_MARGIN:
                # Adding this widget will go over our width, go to a new row

                # Increment the row
                self.lastRowInt += 1
                
                # Reset our column and width
                self.lastColumnInt = 0
                self.currentWidthInt = 0
            else:
                # Still within our limits, just increment the column
                self.lastColumnInt += 1
                
            # Actually add the widget
            super(AutoGridLayout, self).addWidget(widgetObjIn, self.lastRowInt, self.lastColumnInt)
            
            # Increment our width
            self.currentWidthInt += widgetObjIn.width()         
        
            
    def deleteWidget(self,
                     widgetObjIn):
        """
        Delete a widget from the layout
        
        Args:
            widgetObjIn (obj): Widget to delete
            
        Returns:
            None
        """
        # Go Through Columns/Rows and get our widgets in order
        widgetsList = []
        
        for currentRowInt in range(self.rowCount()):
            for currentColumnInt in range(self.columnCount()):
                widgetObj = None
                
                try:
                    widgetObj = self.itemAtPosition(currentRowInt, currentColumnInt).widget()
                except Exception as errorObj:
                    break
                
                if widgetObj is not None and widgetObj != widgetObjIn:
                    widgetsList.append(widgetObj)
        
        # Remove our items
        for currentRowInt in range(self.rowCount()):
            for currentColumnInt in range(self.columnCount()):                                        
                try:
                    layoutItemObj = self.itemAtPosition(currentRowInt, currentColumnInt)
                except Exception as errorObj:
                    break
                
                if widgetObj is not None:
                    self.removeItem(layoutItemObj)
         
        # Reset our columns/rows and width
        self.lastRowInt = -1
        self.lastColumnInt = -1
        self.currentWidthInt = 0
        
        # Re-add our widget
        for currentWidgetObj in widgetsList:
            self.addWidget(currentWidgetObj)
            
        # Delete our widget
        widgetObjIn.deleteLater()
        widgetObjIn.hide()
        
        # Refresh the UI
        self.update()
        self.parent().window().adjustSize()
        

######################################
############# FUNCTIONS ##############
######################################

######################################
############### MAIN #################
######################################