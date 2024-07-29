######################################
############# IMPORTS ################
######################################
#from thirdparty.mottosso.Qt import QtCore
#from thirdparty.mottosso.Qt import QtGui
#from thirdparty.mottosso.Qt import QtWidgets
from thirdparty.mottosso.Qt import QtCompat
from thirdparty.mottosso.Qt import IsPyQt4
from thirdparty.mottosso.Qt import IsPyQt5
from thirdparty.mottosso.Qt import IsPySide
from thirdparty.mottosso.Qt import IsPySide2

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

######################################
############# FUNCTIONS ##############
######################################
def isObjectValid(objectToTestObjIn):
    """
    Determine if `objectToTestObjIn` is valid

    Args:
        objectToTestObjIn (obj): Object to test

    Returns:
        (bool): Is the object valid
    """
    import shiboken2
    return shiboken2.isValid(objectToTestObjIn)

def createApp():
    """
    Create and Return the Qt App

    Args:
        None

    Returns:
        (:class:`QApplication`): Created Application
    """
    # See if we have an app already
    appObj = QtCore.QCoreApplication.instance()

    if appObj != None:
        return (appObj, False)

    # Create the App
    return (QtWidgets.QApplication([]), True)

def findTopLevelWidget(appObjIn):
    """
    Find the top level windget for appObjIn

    Args:
        appObjIn (object): Qt App Object

    Returns:
        (object): Top Level Widget
    """
    if appObjIn is not None:
        topLevelWidgetsList = appObjIn.topLevelWidgets()

        if len(topLevelWidgetsList) > 0:
            widgetObj = topLevelWidgetsList[0]

            widgetObjParent = widgetObj.parentWidget()
            while widgetObjParent is not None:
                widgetObj = widgetObjParent
                widgetObjParent = widgetObj.parentWidget()

            return widgetObj

    return None

def loadUiType(uiFile):
    """
    Pyside lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    """
    from PySide2 import QtUiTools
    return QtUiTools.loadUiType(uiFile)

def QSignal(*args):
    '''
    Signal connection, I think this is now obsolete with qtcore
    '''
    return QtCore.Signal(*args)