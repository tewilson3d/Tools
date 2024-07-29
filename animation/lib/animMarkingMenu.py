import maya.cmds as cmds
import maya.mel as mel
from functools import partial

import rigging.globals as rig_globals
import ui.markingMenuTemplate as userMM
import animation.tools.ikFkSwitch.snapIkFk as snapIkFk
import animation.tools.snapParentSpace.snapParentSpace as snapParentSpace
import animation.tools.selectAllControls as selectControls

parentspace = rig_globals.rig.parentspace
ikblend = rig_globals.rig.ik


class MMAnimationTool(userMM.MarkingMenuTemplate):
    ''' Skinning marking menu '''
    def __init__(self):
        super(MMAnimationTool, self).__init__('AnimationTool')
        
        self.NPlabel = 'Select All'
        self.SPlabel = 'Mainp Mode Tool'
        
        self.buildTool()

    def Nfunction(self, *args):
        selectControls.main()
        
    def Wfunction(self, *args):
        snapIkFk.apply()

    def Efunction(*args):
        val = args[1]    
        snapParentSpace.switch(value=val)
        
    def Sfunction(*args):
        mel.eval("animToolModeGUI();")

    def buildTool(self):
        '''
        Build the menu based on whats selected
        '''
        self.buildMM()
        
        if len(cmds.ls(sl=True)):
            obj = cmds.ls(sl=True)[0]
            if cmds.objExists(f'{obj}.{ikblend}'):
                self.WPlabel = 'IK/FK Switch'

            # build our marking menu from our selected objects 'ParentSpace' attr
            if cmds.objExists(f'{obj}.{parentSpace}'):
  
                PSattr = cmds.attributeQuery(parentspace,n=obj, listEnum=True)
                splitted = PSattr[0].split(':')
                
                mmDict={}
                for i,e in enumerate(splitted):
                    mmDict[e]=i
                    
                # build subMenu options with our parentSpace values
                cmds.menuItem(l='ParentSpace Switch', sm=True, rp='E')
                for key in mmDict.keys():
                    cmds.menuItem(l=key, command=partial(self.Efunction, mmDict[key]))
                    
                cmds.setParent('mainMM', m=True)