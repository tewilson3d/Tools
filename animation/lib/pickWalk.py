######################################
############# IMPORTS ################
######################################
import json

import maya.cmds as cmds
import filepath

import maya_utils as rutil
import meta.metaFactory as metaFactory


######################################
############# DEFINES ################
######################################
UP    = 'pickwalkUp'
DOWN  = 'pickwalkDwon'
RIGHT = 'pickwalkRight'
LEFT  = 'pickwalkLeft'

SOURCE = 'sourceObject'
TAREGT = 'targetObject'
DIR    = 'direction'


######################################
############# FUNCTIONS ##############
######################################
def createPickWalk(node, target, direction):
    '''
    '''
    nodeObj = metaFactory.getMPyNode(node)
    targetObj = metaFactory.getMPyNode(target)
    
    if direction == UP:
        counterDirection = DOWN
    elif direction == DOWN:
        counterDirection = UP
    elif direction == LEFT:
        counterDirection = RIGHT
    elif direction == RIGHT:
        counterDirection = LEFT
        
    nodeObj.addConnection(direction,
                          targetObj,
                          counterDirection,
                          'message',
                          'message')
    
def pickWalk(direction):
    '''
    '''
    nodeObj = metaFactory.getObjectListFromSelection()
    if nodeObj:
        if nodeObj[0].attribute(direction):
            cmds.select(nodeObj[0].attribute(direction).value, r=True)
            

def writePickWalkFile(controlDictList, pickwalkfile):
    json.dump(controlDictList, 
              open(filepath.FilePath(pickwalkfile), 'w'), 
              sort_keys=False, 
              ensure_ascii=True,
              indent=True)

def readPickWalkFile(pickwalkfile=None):
    ''' '''
    pickwalkData = json.load(open(filepath.FilePath(pickwalkfile), 'r'),)
    
    if pickwalkData:
        for pickwalkitem in pickwalkData:
            for objKey, objValue in pickwalkitem.items():
                createPickWalk(node=str(objKey),
                               target=str(objValue[TAREGT]),
                               direction=str(objValue[DIR]))