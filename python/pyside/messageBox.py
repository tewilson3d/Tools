######################################
############# IMPORTS ################
######################################
from pyside.qt_wrapper import QtWidgets
from pyside.qt_wrapper import QtCore
from pyside.qt_wrapper import createApp
from pyside.qt_wrapper import findTopLevelWidget


######################################
############# FUNCTIONS ##############
######################################
def spawnMessageBox(messageStrIn,
                    titleStrIn,
                    iconObjIn=QtWidgets.QMessageBox.Information,
                    buttonsObjIn=QtWidgets.QMessageBox.Ok,
                    isModalIn=True,
                    parentObjIn=None,
                    appObjIn=None):
    """
    Spawn a message box with user specified title, message, icon, buttons and modality

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Message to display
        titleStrIn (str): Window Title

    Keyword Args:
        iconObjIn (object): Icon to show (:class:`QtWidgets.QMessageBox.Icon`)
        buttonsObjIn (object): Buttons on message box (:class:`QtWidgets.QMessageBox.StandardButtons`)
        isModalIn (bool): Whether this message box is modal
        parentObjIn (object): Parent
        appObjIn (object): Existing App

    Returns:
        (object): Button Response (:class:`QtWidgets.QMessageBox.StandardButton`)
    """
    appObj = appObjIn
    parentObj = parentObjIn

    if appObjIn == None and parentObj == None:
        appObj, didCreateApp = createApp()

    # Get a parent object if none given
    if parentObj is None:
        parentObj = findTopLevelWidget(appObj)

    # Make the message box
    messageBoxObj = QtWidgets.QMessageBox(parent=parentObj)
    messageBoxObj.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    # Get the return value
    messageBox = QtWidgets.QMessageBox(iconObjIn,
                                       titleStrIn,
                                       messageStrIn,
                                       buttons=buttonsObjIn,
                                       parent=messageBoxObj)

    if isModalIn:
        returnValueObj = messageBox.exec_()
    else:
        messageBox.setWindowModality(QtCore.Qt.NonModal)

        # If non-modal, need to create an event loop to wait for the response
        # before returning
        eventLoop = QtCore.QEventLoop(parentObj)
        messageBox.finished.connect(eventLoop.quit)
        messageBox.show()
        eventLoop.exec_()

        # We will reach here only after the message box finished() signal is emitted
        returnValueObj = messageBox.result()

    return returnValueObj

def spawnErrorMessageBox(messageStrIn,
                         titleStrIn='Error',
                         parentObjIn=None,
                         appObjIn=None,
                         isModalIn=True):
    """
    Spawn an error message box with `messageStrIn` with a title of `titleStrIn`

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Error Message
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        isModalIn (bool): Whether this message box is modal

    Returns:
        None
    """
    spawnMessageBox(messageStrIn,
                    titleStrIn,
                    iconObjIn=QtWidgets.QMessageBox.Critical,
                    buttonsObjIn=QtWidgets.QMessageBox.Abort,
                    isModalIn=isModalIn,
                    parentObjIn=parentObjIn,
                    appObjIn=appObjIn)

def spawnWarningMessageBox(messageStrIn,
                           titleStrIn='Warning',
                           parentObjIn=None,
                           appObjIn=None,
                           isModalIn=True):
    """
    Spawn a warning message box with `messageStrIn` with a title of `titleStrIn`

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Error Message
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        isModalIn (bool): Whether this message box is modal

    Returns:
        None
    """
    spawnMessageBox(messageStrIn,
                    titleStrIn,
                    iconObjIn=QtWidgets.QMessageBox.Warning,
                    buttonsObjIn=QtWidgets.QMessageBox.Ok,
                    isModalIn=isModalIn,
                    parentObjIn=parentObjIn,
                    appObjIn=appObjIn)

def spawnOkCancelMessageBox(messageStrIn,
                            titleStrIn='Cancel?',
                            parentObjIn=None,
                            appObjIn=None,
                            isModalIn=True):
    """
    Spawn a message box with OK/Cancel buttons

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Message to display
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        isModalIn (bool): Whether this message box is modal

    Returns:
        (object): Button Response
    """
    return spawnMessageBox(messageStrIn,
                           titleStrIn,
                           iconObjIn=QtWidgets.QMessageBox.Information,
                           buttonsObjIn=QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                           isModalIn=isModalIn,
                           parentObjIn=parentObjIn,
                           appObjIn=appObjIn)


def spawnYesNoMessageBox(messageStrIn,
                         titleStrIn='YesNo?',
                         parentObjIn=None,
                         appObjIn=None,
                         isModalIn=True):
    """
    Spawn a message box with Yes/No Buttons

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Message to display
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        isModalIn (bool): Whether this message box is modal

    Returns:
        (object): Button Response
    """
    result = spawnMessageBox(messageStrIn,
                           titleStrIn,
                           iconObjIn=QtWidgets.QMessageBox.Question,
                           buttonsObjIn=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                           isModalIn=isModalIn,
                           parentObjIn=parentObjIn,
                           appObjIn=appObjIn)
    
    if result == QtWidgets.QMessageBox.Yes:
        return True
    
    elif result == QtWidgets.QMessageBox.No:
        return False    
    
    
def spawnAlertMessageBox(messageStrIn,
                         titleStrIn='Alert',
                         parentObjIn=None,
                         appObjIn=None,
                         isModalIn=True):
    """
    Spawn an Alert Message Box

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Message to display
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        isModalIn (bool): Whether this message box is modal

    Returns:
        (object): Button Response
    """
    return spawnMessageBox(messageStrIn,
                           titleStrIn,
                           iconObjIn=QtWidgets.QMessageBox.Information,
                           buttonsObjIn=QtWidgets.QMessageBox.Ok,
                           isModalIn=isModalIn,
                           parentObjIn=parentObjIn,
                           appObjIn=appObjIn)


def spawnInputMessageBox(messageStrIn,
                         titleStrIn='Need Input',
                         parentObjIn=None,
                         appObjIn=None,
                         lineEditModeIntIn=QtWidgets.QLineEdit.Normal,
                         defaultTextStrIn=""):
    """
    Spawn an input message box

    Will also create and run a :class:`QtWidgets.QApplication` if `appObjIn` is None

    Args:
        messageStrIn (str): Input Message
        titleStrIn (str): Window Title

    Keyword Args:
        parentObjIn (object): Parent
        appObjIn (object): Existing App
        lineEditModeIntIn (int): Line Edit Mode :class:`QtWidgets.QLineEdit` Options
        defaultTextStrIn (str): Default text for the input line

    Returns:
        (tuple): (str, int) - Text, Response
    """
    # Create the app if neccessary
    appObj = appObjIn
    parentObj = parentObjIn

    if appObjIn == None and parentObj == None:
        appObj, didCreateApp = pyside.qt.createApp()

    # Get a parent object if none given
    if parentObj is None:
        parentObj = pyside.qt.findTopLevelWidget(appObj)

    # Create the Input Dialog
    textStr, responseInt = QtWidgets.QInputDialog.getText(parentObjIn,
                                                          titleStrIn,
                                                          messageStrIn,
                                                          lineEditModeIntIn,
                                                          defaultTextStrIn,
                                                          QtCore.Qt.WindowStaysOnTopHint)

    return (textStr, responseInt)

######################################
############### MAIN #################
######################################
