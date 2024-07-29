######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import animation.lib.timeSlider as time_slider


######################################
############# DEFINES ################
######################################



######################################
############# FUNCTIONS ##############
######################################
def smartBake(nodes, keyframes, growKeyFrames=False):
    ''' Bakes keys where there were original keyframes within the specified range '''
    frames = getKeyChannels()

    for frame in frames:
        # sets an adjacent keyframe before frame if doSmartBake is True
        if growKeyFrames:
            cmds.currentTime(frame-1, e = True)
            executeCommand()
            # qury itt type, cmds.keyTangent(q=1, g=1, )
            cmds.setKeyframe(keyChannels[str(frame)], itt='spline', ott='spline')

        # sets the key
        cmds.currentTime(frame, e=True)
        self.executeCommand()
        cmds.setKeyframe(self.keyChannels[str(frame)])

        # sets an adjacent keyframe after frame if doSmartBake is True
        if self.doGrowKeyframes:
            cmds.currentTime(frame+1, e = True)
            self.executeCommand()
            cmds.setKeyframe(self.keyChannels[str(frame)], itt='spline', ott='spline')

def fullBake(self):
    ''' Bakes animation to all frames specified from "start" to "end" by 'step' '''
    cmds.bakeResults(node, 
                     simulation=True, 
                     time=(self.start, self.end),
                     sampleBy=self.step,
                     preserveOutsideKeys=False,
                     sparseAnimCurveBake=False)

    # bake results flattens tangents so we have to spline them back
    cmds.keyTangent(node, time=(self.start, self.end), itt='spline', ott='spline')

def getKeyChannels(node, attribute=None):
    ''' 
    Traverses through the selected objects to store a dictionary of lists 
    containing channel names keyed/indexed by the frames they were keyframed on 
    '''
    returnKeyframes = []

    # first populate keyChannel keys so that they are sorted
    if attribute is None:
        allKeyframes = cmds.keyframe(node, q=True, timeChange=True, time=())

    else:
        allKeyframes = cmds.keyframe('{0}.{1}'.format(node,
                                                      attribute), 
                                     q=True, timeChange=True, time=())

    if allKeyframes == None:
        return []

    allKeyframes = sorted(list(set(allKeyframes)))        
    for key in allKeyframes: 
        if key >= self.start and key <= self.end:
            self.keyChannels[str(key)] = []
            returnKeyframes.append(key)

    # find channels with keyframes
    if attribute is None:
        channels = cmds.listAttr(node, k=True)

    # if specific attribute is passed
    else:
        channels = [attribute]

    for channel in channels:
        keyframes = cmds.keyframe('{0}.{1}'.format(node, 
                                                   channel),
                                  q=True, 
                                  timeChange=True, 
                                  time=())
        if keyframes == None:
            continue

        for frame in keyframes:
            if frame >= self.start and frame <= self.end:
                self.keyChannels[str(frame)].append('{0}.{1}'.format(node, 
                                                                     channel))                

    # make channel lists unique
    for key in self.keyChannels.keys():
        self.keyChannels[key] = list(set(self.keyChannels[key]))      

    return returnKeyframes   
