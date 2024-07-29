from pyside.qt_wrapper import QtWidgets
import functools

# Method decorator to set cursor to the given shape when the function is run.
# e.g.
#
# @setCursor(QtCore.Qt.WaitCursor)
# def reload(self):
#     ...
#
# Running reload() will set the cursor to wait cursor while it is working.
def setCursor(cursorShape):
    def wrapped(f):
        def wrapped_f(widget, *args, **kargs):
            # Sets the override cursor
            QtWidgets.QApplication.setOverrideCursor(QtWidgets.QCursor(cursorShape))           

            try:
                # Run the function
                result = f(widget, *args, **kargs)
            finally:
                # Set back the original cursor
                QtWidgets.QApplication.restoreOverrideCursor()

            # Return the result
            return result
        return wrapped_f
    return wrapped

# Function for overwriting the default system excepthook.
def excepthook(widget, prefunc=None, postfunc=None):
    '''
    Function for overwriting the default system excepthook.
    This will catch unhandled exceptions and display it in a critical message box.

    @param widget    The widget that the message box should parent to
    @param prefunc   Function to generate the pre-text,
                     i.e. text to print before the errors in the details page
    @param postfunc  Function to generate the post-text,
                     i.e. text to print after the errors in the details page
    '''
    def wrapped(excType, excValue, tracebackobj):
        '''
        @param excType       exception type
        @param excValue      exception value
        @param tracebackobj  traceback object
        '''
        separator = '-' * 75
        errmsg = ''

        # Add pre-text
        # if pretext:
        #     errmsg += '%s\n%s\n' % (pretext, separator)
        if prefunc:
            pretext = prefunc()
            if pretext:
                errmsg += '%s\n%s\n' % (pretext, separator)

        # The error
        errmsg += '%s:\n%s\n' % (str(excType), str(excValue))

        # Traceback info
        import StringIO, traceback
        tbinfofile = StringIO.StringIO()
        traceback.print_tb(tracebackobj, None, tbinfofile)
        tbinfofile.seek(0)
        tbinfo = tbinfofile.read()
        errmsg += '%s\n%s\n' % (separator, tbinfo)

        # # Add post-text
        if postfunc:
            posttext = postfunc()
            if posttext:
                errmsg += '%s\n%s\n' % (separator, posttext)

        messageBox = QtWidgets.QMessageBox(
                        QtWidgets.QMessageBox.Critical,
                        'Unexpected Error',
                        'An unexcepted error occured. Please let your technical artists know!',
                        buttons=QtWidgets.QMessageBox.Ok,
                        parent=widget)

        messageBox.setDetailedText(errmsg)
        messageBox.open()

    return wrapped

def checkModifiers(func):
    '''Function for get current key modifiers, the result will be passed into the wrapped function 
       as keyword argument "modifiers".
       Example:
           @checkModifier
           def getMod(self, modifiers):
               for modifier in modifiers:
                   print modifier
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        kwargs['modifiers'] = QtWidgets.QApplication.keyboardModifiers()
        return func(*args, **kwargs)
    return wrapper
        
