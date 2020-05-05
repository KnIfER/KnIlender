import bpy
import os
import re
from mathutils import *

#for a in bpy.data.actions:
#    print(a.name) 
#    print(a.fcurves) 
#    print(a.frame_range) 
#    print(a.pose_markers) 

sce = bpy.context.scene
obj = bpy.context.object

matrixDict = {}

    
for bI in obj.pose.bones:
    #print(bI.name, bI.matrix) # bone in object space
    matrixDict[bI.name] = bI.matrix
    #mm = Matrix(bI.matrix)
    loc, rot, sca = bI.matrix.decompose()
    #print(rot.invert())
    
    
        
action = obj.animation_data.action
poseBones = obj.pose.bones

#action = bpy.data.actions["action_id"]

print()
print(action.name)

#for curveI in action.fcurves:
#    dPath = curveI.data_path
#    print(eval("obj."+dPath))
#    dIdx = curveI.array_index
#    print(dPath + " Channel#" + str(dIdx))
#    for kI in curveI.keyframe_points:
#        print(kI.co) #coordinates x,y

class TransFormDiff():
    rotationBuild = {}
    transformBuild = {}
    qDiff = None
    qRot = None
    drw = None
    drx = None
    dry = None
    drx = None
    def __init__(self):
        #print("构造函数被执行了~~~")
        self.rotationBuild = [0,0,0,0]
        self.transformBuild = [0,0,0]
        self.rotationBuild[0]=0
        self.rotationBuild[1]=0
        self.rotationBuild[2]=0
        self.rotationBuild[3]=0

deltaDictRef = {}

def getBoneNameInDPath(val):
    idx = val.find("[\"")
    if(idx!=-1):
        return val[idx+2:val.find("\"]", idx)]
    else:
        return val[:val.rfind("#")]

for curveI in action.fcurves:
    dPath = curveI.data_path
    boneName = getBoneNameInDPath(dPath)
    #print(eval("obj."+dPath))
    dIdx = curveI.array_index
    #print(dPath + " Channel#" + str(dIdx))
    tranfrom_type = 0
    if(dPath.find("location")!=-1): 
        tranfrom_type=0
    if(dPath.find("rotation")!=-1): 
        tranfrom_type=1
    if(dPath.find("scale")!=-1) :
        tranfrom_type=2
    for kI in curveI.keyframe_points:
        co = kI.co;
        if(co.x==1):
            if(tranfrom_type==1):
                tDiff = None
                if boneName in deltaDictRef:
                    tDiff = deltaDictRef[boneName]
                else:
                    tDiff = deltaDictRef[boneName] = TransFormDiff()
                #print("first rotation", boneName)
                tDiff.rotationBuild[dIdx] = co.y
     
def getRotation(mt):
    loc0, rot0, sca0 = mt.decompose()
    return rot0
          
for boneName in deltaDictRef:
    thisBone = poseBones[boneName].bone
    pBone = thisBone.parent
    mm = poseBones[boneName].matrix
    #mm = thisBone.convert_local_to_pose(mm, thisBone.matrix_local)
    #    #, parent_matrix=matrixDict[pBone.name],
    #    #parent_matrix_local=pBone.matrix_local)
    
    boneOS = poseBones[boneName].matrix # current pose
    parentOS = poseBones[pBone.name].matrix
    boneRP = thisBone.matrix_local  # rest pose matrix in bone local space
    parentBoneRP = pBone.matrix_local  # parent bone's rest pose matrix in bone local space
    
    #print("Materrix!!!",  boneOS.inverted())
    #print("Materrix!!!", parentBoneRP)
    #print("Materrix!!!", boneRP)
    #print("Materrix!!!", parentBoneRP @ boneRP)
    #print("Materrix!!!", ( parentBoneRP @ boneRP ).inverted())
    
    mm =  ( parentBoneRP.inverted() * boneRP ).inverted() * parentOS.inverted() * boneOS
    
    
    loc0, rot0, sca0 = mm.decompose()
    #print(boneName)
    transFormDiff = deltaDictRef[boneName]

    qBuild = Quaternion(transFormDiff.rotationBuild) # stored in fcurve
    
    
    
    qDiff = rot0.rotation_difference(qBuild)
    print("what's up?")
    print("what's up?", pBone)
    print("what's up0", boneName, getRotation(thisBone.matrix_local))# rest location
    print("what's up?", boneName, rot0)
    print("what's up?", boneName, qBuild)
