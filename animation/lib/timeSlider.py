######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaAnim as OpenMayaAnim

import maya_utils


######################################
############# Functions ################
######################################
def startTime():
    '''return first frame of the current playback range'''
    return OpenMayaAnim.MAnimControl.minTime().value

def endTime():
    '''return last frame of the current playback range'''
    return OpenMayaAnim.MAnimControl.maxTime().value

def setStartEndTime(startframe, endframe):
    '''
    Sets the start and end frame and the playback start and end frame
    This is primarly used for fbx export
    Args:
        startframe (float/int):
        endframe   (float/int):
    Returns:
        None
    '''
    OpenMayaAnim.MAnimControl.setMinTime(OpenMaya.MTime(startframe, OpenMaya.MTime.uiUnit()))
    OpenMayaAnim.MAnimControl.setMaxTime(OpenMaya.MTime(endframe, OpenMaya.MTime.uiUnit()))

def currentFrame(frame=None):
    '''returns the current frame'''
    
    if not frame:return cmds.currentTime(query=True)
    else: cmds.currentTime(frame)

def timeUnits(set=None):
    '''get or set Maya's time units. This is the animation FPS. The following are
    valid FPS: 1,5,10,20,15,24,25,30,40,48,50,60,80,100,120,200'''
    
    timeStr = {'film':24, 'game':15, 'pal':25, 'ntsc':30, 'show':48, 'palf':50,
               'ntscf':60, 'sec':1, '5fps':5, '10fps':10, '20fps':20, '40fps':40,
               '80fps':80, '100fps':100, '120fps':120, '200fps':200}
    
    if set:
        timelookup = dict(zip(timeStr.itervalues(), timeStr.iterkeys()))
        cmds.currentUnit(time=timelookup[set])
    else:
        return timeStr[cmds.currentUnit(q=True,time=True)]

def getSelectedTimeRange():
    ''' returns the selected time range '''
    
    timeControl = maya_utils.getMelGlobalVariable('$gPlayBackSlider')
    if cmds.timeControl( timeControl, q = True, rangeVisible = True ):
        start_end = cmds.timeControl( timeControl, q = True, rangeArray = True )
        return [start_end[0], start_end[-1]-1]
    else:
        return [startTime(), endTime()]