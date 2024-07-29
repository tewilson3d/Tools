import maya.cmds as cmds
import maya.mel as mel


class GUI(object):
    def __init__(self):
        self.winName = 'linearizeOptionsWin'         

    def create(self, linOptions=0, *args):
        '''Build the window'''
        if cmds.window(self.winName, ex=True):
            cmds.deleteUI(self.winName)

        cmds.window(self.winName, t='Linearize Options')
        colLayout = cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1, 400)])
        # Adding a slider to adjust strength of linearize
        cmds.frameLayout( l="Linearize Strength:")
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 100), (2, 300)])
        self.field = cmds.floatField( min=0.05, max=1.00, value=linOptions, cc=self.updateField)
        self.slider = cmds.floatSlider( min=0.05, max=1.00, value=linOptions, step=.05, cc=self.updateSlide)
        cmds.setParent( top = True )
        cmds.text(l=' ')
        cmds.text(l='Set the % amount keys should be linearized.')
        cmds.text(l=' ')
        cmds.checkBox(label='auto tangent',
                      value=bool(cmds.optionVar(q='linearizeKeysAutoTangent')),
                      onc=lambda x: self.setAutoTangent(True),
                      ofc=lambda x: self.setAutoTangent(False))
        cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 200), (2, 200)])
        cmds.button( l="Apply", c=self.runLin )
        cmds.button( l="Close", c=self.deleteUI)
        cmds.showWindow( self.winName )
        
    def deleteUI(self, *args):
        cmds.deleteUI(self.winName)        
        
    def runLin(self, *args):
        linSet = cmds.floatSlider(self.slider, q=True, v=True)
        linearizeKeys(doLinear=linSet)
        
    def updateSlide(self, *args):
        linSet = cmds.floatSlider(self.slider, q=True, v=True)
        cmds.optionVar(fv=['linearizeKeys',linSet])
        cmds.floatField(self.field, e=True, v=linSet)
        
    def updateField(self, *args):
        linSet = cmds.floatField(self.field, q=True, v=True)
        cmds.optionVar(fv=['linearizeKeys',linSet])
        cmds.floatSlider(self.slider, e=True, v=linSet)  

    def setAutoTangent(self, enabled):
        cmds.optionVar(iv=['linearizeKeysAutoTangent', enabled])

def makeWin():
    win = GUI()
    if cmds.optionVar(q='linearizeKeys'):
        linOptions = cmds.optionVar(q='linearizeKeys')
    else:
        linOptions = 1
    win.create(linOptions)          

def linearizeKeys(doLinear=0):
    if doLinear == 0:
        if cmds.optionVar(q='linearizeKeys'):
            doLinear = cmds.optionVar(q='linearizeKeys')
        else:
            doLinear = 1
    #Get a list of selected animation curves
    selectedCurves = cmds.keyframe(q=True, n=True)
    #For each of the selected curves...
    if not selectedCurves:
        cmds.warning('please select an animated object, then specific keys to linearize.')
        return None
    for curve in selectedCurves:
        print ("curve: " + curve + "\n")

        #Get the indices of the selected keys on the curve
        selectedKeyIndices = cmds.keyframe(curve, q=True, iv=True, sl=True)
        if not selectedKeyIndices:
            cmds.warning('Please select specific keys to linearize.')
            return None
        allKeyIndices = cmds.keyframe(curve, q=True, iv=True, sl=False)
        print (selectedKeyIndices)
        print (allKeyIndices)

        #The new version is able to do multiple 'sections,' meaning we need to know continuous cSets. we'll find if a key is skipped.
        curveSets = []
        curSet = []
        for key in selectedKeyIndices:

            # exception for last key
            if key == selectedKeyIndices[-1]:
                '''
        here, we have to catch if the last section is the end of the curve and
        if the first section is the start of the curve. If so, we make one giant
        section treated as one to get around the end of the loop.
        '''                
                if key == allKeyIndices[-1]\
                   and selectedKeyIndices[0] == allKeyIndices[0]:
                    curSet.append(key)
                    if curveSets:
                        for c in curveSets[0]:
                            curSet.append(c)
                    curveSets.append(curSet)
                    curveSets = [l for l in curveSets if curveSets.index(l) is not 0]
                else:
                    curSet.append(key)
                    curveSets.append(curSet)
                    curSet = []                    
            else:
                curSet.append(key)
                if selectedKeyIndices[selectedKeyIndices.index(key) +1] != key + 1:
                    curveSets.append(curSet)
                    curSet = []

        for cSet in curveSets:
            #Get the index of the next key
            lastIndexInArray = cSet[-1]
            nextKeyIndex = lastIndexInArray + 1
            print ("lastIndexInArray: " + str(lastIndexInArray) + "\n")
            print ("nextKeyIndex: " + str(nextKeyIndex) + "\n")

            #Get the value and time of the next key
            nextKeyTime = cmds.keyframe(curve, index=(nextKeyIndex,nextKeyIndex), q=True)
            if nextKeyTime:
                print ("nextKeyTime: " + str(nextKeyTime[0]) + "\n")
            else:
                nextKeyTime = cmds.keyframe(curve, index=(lastIndexInArray,lastIndexInArray), q=True)
                nextKeyIndex = lastIndexInArray

            nextKeyValue = cmds.keyframe(curve, index=(nextKeyIndex,nextKeyIndex), ev = True, q=True)
            if nextKeyValue:
                print ("nextKeyValue: " + str(nextKeyValue[0]) + "\n")
            else:
                cmds.warning("Key value missing! Something is selected incorrectly.")           
            #Get the index of the previous key
            previousKeyIndex = cSet[0] - 1
            if previousKeyIndex < 0:
                previousKeyIndex = cSet[0]

            print ("previousKeyIndex: " + str(previousKeyIndex) + "\n")

            '''
            if last in selected == last in all:
            nextKeyValue = recalculate based on first key

            inverse if keyIndex is the first key.

            '''


            #Get the value and time of the previous key
            previousKeyValue= cmds.keyframe(curve, index=(previousKeyIndex,previousKeyIndex), ev = True,  q=True)
            previousKeyTime= cmds.keyframe(curve, index=(previousKeyIndex,previousKeyIndex), q=True)

            #Get the difference in value/time between the previous key and the next key
            if nextKeyValue and previousKeyValue:
                valDiff = (nextKeyValue[0] - previousKeyValue[0])

                print ("valDiff: " + str(valDiff) + "\n")

            if nextKeyTime and previousKeyTime:
                timeDiff = (nextKeyTime[0] - previousKeyTime[0])

            #For each of the selected keys on this curve...
            for keyIndex in cSet:
                #Get the time of the current key
                currentIndexTime = cmds.keyframe(curve, index=(keyIndex,keyIndex), q=True)
                # if this is a 'loop,' adjust nextKeyTime to the future to account for looping
                ''' This is an odd case, and I should clarify and clean up more... here's the logic:
                - If we're looping, we need the first frames to "seem" like the last frames, ie the
                "time" must be past the end of the curve, like with infinite cycle. but ONLY when
                dealing with frames in the last section of the curve... when looking at the front
                section, we need the opposite. so, we adjust the "times" accordingly. 
                '''
                previousLinTime = previousKeyTime
                nextLinTime = nextKeyTime
                if nextKeyTime < currentIndexTime:
                    firstKey = cmds.keyframe(curve, index=(0,0), q=True)[0]
                    lastKey = cmds.keyframe(curve, index=(len(allKeyIndices)-1,len(allKeyIndices)-1), q=True)[0]
                    nextLinTime = [lastKey + (nextKeyTime[0] - firstKey)]
                elif previousKeyTime > currentIndexTime:
                    firstKey = cmds.keyframe(curve, index=(0,0), q=True)[0]
                    lastKey = cmds.keyframe(curve, index=(len(allKeyIndices)-1,len(allKeyIndices)-1), q=True)[0]
                    previousLinTime = [firstKey - (lastKey - previousKeyTime[0])]                  
                #Get the percentage of the distance that this key lies between the previous key's time and the next key's time
                linMel = ("linstep " + str(previousLinTime[0])+ " " + str(nextLinTime[0]) +" " + str(currentIndexTime[0]))
                timePercentage = mel.eval(linMel)
                #Get the value of the current key
                currentIndexValue = cmds.keyframe(curve, index=(keyIndex,keyIndex), ev=True, q=True)
                # get a precentage of the precentage
                precPrecntage = currentIndexValue[0] * 0.1
                print (str(precPrecntage) + "\n")
                #Get the percentage of the distance that this key lies between the previous key's value and the next key's value
                #Then get a value to use as the scale point. This is the value of the point that lies on a linear path between the
                #previous key and the next key at the given time.
                valuePercentage = 0.0
                scalePoint = [0.0]
                # Question this math... probably the first part to revise
                goal = previousKeyValue[0] + (timePercentage * valDiff)
                scalePoint = currentIndexValue[0] - (doLinear * (currentIndexValue[0] - goal))

                cmds.keyframe(curve, e=True, vc=scalePoint, index = (keyIndex,keyIndex))
                print ("timePercentage: " + str(timePercentage) + " valDiff: " + str(valDiff)  + " $gosl: " + str(goal) + "\n")
                print ("scalePoint: " + str(scalePoint) + " nextKeyValue[0]: " + str(nextKeyValue) + " previousKeyValue[0]: " + str(previousKeyValue) + "\n")

        if cmds.optionVar(q='linearizeKeysAutoTangent'):
            mel.eval('source autoTangent; aTan_smoothKeys(0.0, 1);')
