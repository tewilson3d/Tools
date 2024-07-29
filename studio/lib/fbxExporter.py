######################################
############# IMPORTS ################
######################################
import sys
import fileinput

import maya.cmds as cmds
import maya.mel as mel

import filepath
import decorators
import animation.lib.timeSlider as timeSlider

# perforce
try:
    import helix.perforce as perforce
    p4obj = perforce.PerforceWrapper()
except:
    p4obj = None

# ---TO DO switch to cmds
##cmds.FBXExportSkins('-v', True)
##cmds.FBXExportShapes('-v', True)


######################################
############# FUNCTIONS ##############
######################################
def export(selectionList,
           exportPath,
           exportType='geo',
           startTime=None,
           endTime=None,
           exportAsAscii=False,
           triangulate=True,
           stripNamespace=False,
           saveSourceControl=False,
           deleteSkeletonRigData=False):
    """
    Discriptor

    Args:
        selectionList (MSelectionList, list), Needs a MSelList or a list
        exportPath (Path), Path object
        exportType
        startTime
        endTime
        exportAsAscii : export fbx as ascii file or binary file
        triangulate : triangulate mesh on export

    Returns:
        None
    """
    file_is_new = False
    
    if not isinstance(exportPath, filepath.FilePath):
        exportPath = filepath.FilePath(exportPath)

    if not isinstance(selectionList, list):
        selectionList = [selectionList]

    # check source control, if file is new add at the end of exporting
    if not exportPath.exists():
        exportPath.dir().makeDir()
        file_is_new = True
    
    if file_is_new is False and saveSourceControl:
        p4_checkout_file(exportPath.asUnixPath())
    
    sys.__stdout__.write( "begining to export \n")

    # select what was passed in for export
    cmds.select(selectionList, replace=True)

    sys.__stdout__.write( "got object \n")

    # create a string to eval
    mel.eval('FBXResetExport')
    evalString = f'FBXExport -f "{str(exportPath.asMayaPath())}" -s'

    # Animation
    if exportType == 'anim':

        # if the startTime param is None then use the current animation timeline
        # else set the current timeline to the passed in params
        if startTime is None:
            startTime = timeSlider.startTime()
    
        if endTime is None:	    
            endTime = timeSlider.endTime()
        
        timeSlider.setStartEndTime(startTime, endTime)

        sys.__stdout__.write( f"set anim start time {str(startTime)}  {str(endTime)} \n")

        #set the fbx option to export baked anim
        mel.eval('FBXExportBakeComplexAnimation -v 1')
        mel.eval('FBXExportBakeResampleAnimation -v 1')
        mel.eval('FBXExportQuaternion -v "quaternion"')
        mel.eval('FBXExportBakeComplexStep -v 1')
        cmds.FBXExportShapes('-v', True)

        startTimeEval = f'FBXExportBakeComplexStart -v {str(startTime)}'
        endTimeEval = f'FBXExportBakeComplexEnd -v {str(endTime)}'
        
        ## seems to be needed to for exporting a specific timeline
        #mel.eval(f'FBXExportSplitAnimationIntoTakes -v \"{exportPath.baseName()}\" {str(startTime)} {str(endTime)}')

        mel.eval(startTimeEval)
        mel.eval(endTimeEval)

    # Mesh
    else:
        mel.eval('FBXExportAnimationOnly -v 0')
        
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v true")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportSmoothMesh -v true")

    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportQuaternion -v quaternion")
    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v true")

    # Triangulate
    if triangulate:
        mel.eval('FBXExportTriangulate -v 1')
    else:
        mel.eval('FBXExportTriangulate -v 0')    

    # Constraints
    mel.eval("FBXExportConstraints -v false")

    # Cameras
    mel.eval("FBXExportCameras -v false")

    # Lights
    mel.eval("FBXExportLights -v false")

    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")

    # Connections
    mel.eval("FBXExportInputConnections -v false")    

    # Determine file type
    if exportAsAscii:
        mel.eval('FBXExportInAscii -v 1')
    else:
        mel.eval('FBXExportInAscii -v 0')

    mel.eval('FBXExportFileVersion -v "FBX201800"')     
    mel.eval('FBXImportConvertUnitString -v "cm"')
    mel.eval('FBXExportUpAxis "y"')     

    sys.__stdout__.write( "setup all evals \n")
    
    # Strips all exseccive str attrs
    if deleteSkeletonRigData:
        with decorators.mayaUndoOn():
            jnt_lits = cmds.ls(type='joint') 
            for jnt in jnt_lits:
                if cmds.objExists(jnt + '.rigData'):
                    cmds.deleteAttr(jnt, at='rigData')

        mel.eval(evalString)
        cmds.undo()
        cmds.undo()
        
    else:
        # Eval the fbx exporter
        mel.eval(evalString)
    
    sys.__stdout__.write( "exported \n")
    
    # add to source control if new
    if file_is_new and saveSourceControl:
        p4_add_file(exportPath)

    # Find namespace if exist
    if stripNamespace:
        ns = selectionList[0].split(':')
        if len(ns) > 1:
            if stripNamespace and exportAsAscii:
                if len(ns[0].split('|')) > 1:
                    ns = f'{ns[0].split("|")[-1]}:'
                else:
                    ns = f'{ns[0]}:'
    
                # strip the namespace
                strip_namespace(exportPath, ns)

def p4_checkout_file(file_path):
    '''
    Checks out the file before exporting
    Returns:
        isSuccessful
        isFileNew
    '''
    if p4obj:
        p4obj.checkout(file_path.asUnixPath())

def p4_add_file(file_path):
    '''
    Adds the new file to p4
    '''
    if p4obj:
        p4obj.add([file_path.asUnixPath()])

def strip_namespace(fbx_file, namespace):
    '''
    strips the namespace from the fbx file,
    this to help overcome unity namespace issues

    Args:
        fbx_file(str):
        namespace(str)
    Returns:
        none
    '''
    if not isinstance(fbx_file, filepath.FilePath):
        fbx_file = filepath.FilePath(fbx_file)

    for i, line in enumerate(fileinput.input(fbx_file, inplace=1)):
        sys.stdout.write(line.replace(namespace, ''))