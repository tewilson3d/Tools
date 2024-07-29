#######################################
############# IMPORTS ################
######################################
import maya.cmds as cmds
import animation.lib.channelbox_utils as channel_util



######################################
############# CLASSES   ##############
######################################
class Util(object):
    '''
    Util fuunction for the Mesh meta object
    '''
    def __init__(self, meshObj):
        '''
        Args:
            meshObj (Mesh) 'util.metaclasses.mesh,Mesh()'
        Returns:
            None
        '''
        self._parentObj = meshObj

    @property
    def checkMeshHistory(self):
        '''
        Check for mesh history
        --To Do-- need to handle skincluster and outher skinned history
        '''
        initialShadingGroup = "initialShadingGroup"

        # Check if there is history on the mesh
        historyList = cmds.listHistory(self._parentObj.name, 
                                       interestLevel=2, 
                                       pruneDagObjects=True)
        if not historyList:
            return   

        if initialShadingGroup in historyList:
            # For some reason, it returns the intial shading group inside the history list, 
            # exclude it here.
            historyList.remove(initialShadingGroup)

        return historyList

    @property
    def fixMeshHistory(self):
        cmds.bakePartialHistory(self._parentObj.name, prePostDeformers=True)

    @property
    def fixNonDeformerHistory(self):
        '''
        Removes all non-deformer history
        '''
        cmds.bakePartialHistory(self._parentObj.name,
                                prePostDeformers=True, 
                                preDeformers=False, 
                                postSmooth=False, 
                                preCache=False)    

    @property
    def fixExtraShapeNodes(self):
        '''
        Removes any extra shape nodes if there is no skincluste
        '''
        shapes = self._parentObj.intermediateShape
        if shapes:
            if len(shapes) > 1:
                cmds.delete([s.name for s in shapes[1:]])

    @property
    def polyCount(self):
        '''
        Return the poly count
        '''
        if self._parentObj.shape:
            return cmds.polyEvaluate(self._parentObj.shape.name, face=True)
    
    def movePivotLocation(self, position):
        
        cmds.move(position[0],
                  position[1],
                  position[2],
                  f'{self._parentObj.name}.scalePivot',
                  f'{self._parentObj.name}.rotatePivot',
                  a=True,
                  ws=True,
                  rpr=True)                       

    @property
    def freezeTransform(self):
        '''
        Overloading the mayaObject to handle joint
        Args:
            None
        Returns:
            None
        '''
        cmds.makeIdentity(self._parentObj.name, apply=True, t=True, r=True, s=True)

    def setReference(self, setReference=True):
        '''
        Temp until we get a real mesh and transfrom class
        '''
        try:
            if setReference:
                cmds.setAttr('{0}.{1}'.format(self._parentObj.shape.name, 'overrideEnabled'), 1)
                cmds.setAttr('{0}.{1}'.format(self._parentObj.shape.name, 'overrideDisplayType'), 2)            
            else:
                cmds.setAttr('{0}.{1}'.format(self._parentObj.shape.name, 'overrideDisplayType'), 0)
        
        except:
            return cmds.error('Mesh Obejct Transform SetReference Errored')     

    def setDefaultValues(self):
        ''' Zero and set channel attrs to default '''
        channel_util.set_channel_defaults(self._parentObj.name)
        
'''

    #def checkNoneMergedVertices(self, minDistance=0.001):
        #Return list of none merged vertices and this will exclude
        #any none merged verts from other uv shells
        
        #checkData = {}
        #for mesh in meshList:
            #cmds.select(clear=True)
            #cmds.select(mesh)
            #cmds.polySelectConstraint(sh=0, bo=1, t=0x8000, w=1, m=3)
            #selectedEdges = cmds.ls(selection=True, flatten=True)
            #cmds.polySelectConstraint(sh=0, bo=0, t=0x8000, w=0, m=3)
            #vertexList = []
            #for selectedEdge in selectedEdges:
                #vertices = cmds.polyListComponentConversion(selectedEdge, bo=True, fe=True, tv=True)
                #if len(vertices) == 1:
                    #vertices = cmds.ls(vertices, flatten=True)
                #for vertex in vertices:
                    #vertexList.append(vertex)
            #vertexSet = set(vertexList)
            #vertexList = list(vertexSet)

            #vertexPosData = {}
            #for vertex in vertexList:
                #id = vertex.split('.')[-1]
                #vertexPos = cmds.xform(vertex, q=True, ws=True, t=True)
                #vertexPosData[id] = om.MVector(vertexPos[0], vertexPos[1], vertexPos[2])

            #notMergedVertices = []
            #for vert in vertexPosData.keys():
                #for vert2 in vertexPosData.keys():
                    #if vert2 != vert:
                        #diffVec = vertexPosData[vert2] - vertexPosData[vert]
                        #distance = diffVec.length()
                        #if distance < minDistance:
                            #notMergedVertices.append(vert2)
            #if notMergedVertices:
                #checkData[mesh] = notMergedVertices                 
        #return checkData

    #def fixMerge(self, minDistance=0.001):
       
        #Not fully tested or migrated over TODO
    
        #for mesh, notMergedVertices in self.checkNoneMergedVertices.items():
            #if len(notMergedVertices) == 0:
                #return
            #for vtx in notMergedVertices:
                #cmds.select('{0}.{1}'.format(self._parentObj.name,
                                                #vtx), 
                            #add=True)
            #cmds.polyMergeVertex(ch=False, d=minDistance)
            #cmds.select(clear=True)
'''