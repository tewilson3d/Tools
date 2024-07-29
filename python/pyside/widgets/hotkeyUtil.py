from pyside.qt_wrapper import QtCore, QtWidgets


class Hotkey(object):
    """ class for handling the hotkeys """

    def __init__(self, hkey=None, text=None, modifier=None, func=None):
        self.hkey = hkey
        self.text = text
        self.modifier=modifier
        self.func = func

    def execute(self):
        """execute the function associated with this hotkey"""
        if self.func:
            self.func()

class HotkeyUtil(object):
    """Hotkey utility helper"""

    def __init__(self):
        self.hotkey_list = []

    def keyPressEvent(self, event):
        """function that should get called in a widget key press event"""

        hkey = event.key()
        text = event.text()
        modifier = event.modifiers()

        #if its a string lets just make sure its lower - this way when a shift
        #modifier is used, the text still correlates
        if not type(hkey) is int:
            hkey = hkey.lower()

        #loop the hotkeys and find a match for the key and modifier passed in
        for hotkey in self.hotkey_list:
            if hotkey.hkey == hkey or hotkey.text == text:
                if modifier == hotkey.modifier:
                    hotkey.execute()
                elif not modifier and not hotkey.modifier:
                    hotkey.execute()


    def addHotkey(self, hkey=None, text=None, func=None, modifier=None):
        """add the hotkey to the class so it will execute when called.
            modifier is optional and you can add either hkey or text"""

        hotkey = Hotkey(hkey=hkey, text=text, modifier=modifier, func=func)
        self.hotkey_list.append(hotkey)