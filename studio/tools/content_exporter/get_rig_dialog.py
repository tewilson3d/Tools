######################################
############# IMPORTS ################
######################################
import filepath
from pyside.qt_wrapper import loadUiType


######################################
############# DEFINES ################
######################################
baseWidget_uiPath = filepath.FilePath(__file__).dir().join('get_rig_dialog.ui')
form_class, base_class = loadUiType(baseWidget_uiPath)



######################################
############# CLASSES ################
######################################
class RigDialog(form_class, base_class): 

    def __init__(self, combobox_items=None, text_name=None, parent=None):
        super(RigDialog, self).__init__(parent=parent)
        self.setupUi(self)
        if combobox_items:
            self.rig_combobox.addItems(combobox_items)
        else:
            self.rig_combobox.setVisible(False)
        if text_name:
            self.name_lineedit.setText(text_name)
        else:
            self.name_lineedit.setVisible(False)

        # Button connection
        # current index changed is wrong
        self.rig_combobox.currentIndexChanged.connect(self.get_new_name)
        self.name_lineedit.returnPressed.connect(self.get_new_name)

    def get_new_name(self):
        '''
        Create the rigMetaNode

        Args:
            None
        Returns:
            None
        '''
        return self.accept()
