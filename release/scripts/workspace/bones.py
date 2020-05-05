import bpy
import os
import re
from mathutils import *

JuHuaCan = bpy.app.version >= (2, 80, 0)

class TransFormDiff():
    rotationBuild = {}
    transformBuild = {}
    qDiff = None
    qRot = None
    rot0 = None
    drw = None
    drx = None
    dry = None
    drx = None
    def __init__(self):
        #print("构造函数被执行了~~~")
        self.rotationBuild = [0,0,0,0]
        self.rotationBuild[0]=0
        self.rotationBuild[1]=0
        self.rotationBuild[2]=0
        self.rotationBuild[3]=0
        self.transformBuild = [0,0,0] 
        self.transformBuild[0]=0
        self.transformBuild[1]=0
        self.transformBuild[2]=0


def getBoneNameInDPath(val):
    idx = val.find("[\"")
    if(idx!=-1):
        return val[idx+2:val.find("\"]", idx)]
    else:
        return val[:val.rfind("#")]

def getSelectedBoneName():
    selected_bone_name = 0
    var = bpy.context.selected_pose_bones
    if not var:
        var = bpy.context.selected_bones
    if var and var[0]:
        selected_bone_name = var[0].name
    if selected_bone_name:
        print('selected_bone_name', selected_bone_name)
    return selected_bone_name

# 获取第一帧信息
def buildComparee(action):
    deltaDictRef = {}
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
                    print("first rotation", boneName)
                    tDiff.rotationBuild[dIdx] = co.y
    return deltaDictRef

# 获取所有帧信息
def buildAllComparee(action):
    deltaDict = {}
    for curveI in action.fcurves:
        dPath = curveI.data_path
        boneName = getBoneNameInDPath(dPath)
        print("obj."+dPath)
        dIdx = curveI.array_index
        print(dPath + " Channel#" + str(dIdx))
        tranfrom_type = 0
        if(dPath.find("location")!=-1): 
            tranfrom_type=0
        if(dPath.find("rotation")!=-1): 
            tranfrom_type=1
        if(dPath.find("scale")!=-1) :
            tranfrom_type=2
        for kI in curveI.keyframe_points:
            co = kI.co;
            key = boneName+"#"+str(co.x)#+"#"+tranfrom_type+"#"+dIdx
            if(tranfrom_type==1):
                transFormDiff = None
                print("processing...", key, dPath, dIdx)
                if key in deltaDict:
                    transFormDiff = deltaDict[key]
                    #print("found???", key)
                else:
                    transFormDiff = TransFormDiff()
                    deltaDict[key] = transFormDiff
                    #print("new ???", key, transFormDiff.rotationBuild[dIdx])
                #if(transFormDiff.rotationBuild[dIdx] != 0):
                    #print("conflict!!!", transFormDiff.rotationBuild[dIdx], key, dPath, dIdx)
                transFormDiff.rotationBuild[dIdx] = co.y
                #print("dump ???", key, co.y)
                
            #print("found!!!", transFormDiff.rotationBuild[dIdx], co.y)
    return deltaDict

 
if __name__ == '__main__':
    print("\nStarting Add Relatice Animation Offsets……\n")

    sce = bpy.context.scene

    obj = bpy.context.object

    poseBones = obj.pose.bones

    matrixDict = {}

    for bI in poseBones:
        #print(bI.name, bI.matrix) # pose bone [https://docs.blender.org/api/current/bpy.types.PoseBone.html]
        thisBone = bI.bone
        parentBone = thisBone.parent
        if parentBone!=None:
            #https://stackoverflow.com/questions/12034813/what-space-is-this-matrix-in
            boneOS = bI.matrix
            parentOS = poseBones[parentBone.name].matrix
            boneRP = thisBone.matrix_local  # rest pose matrix in bone local space
            parentBoneRP = parentBone.matrix_local  # parent bone's rest pose matrix in bone local space
            
            # boneRP * mm == thisNewRest
            # parentBoneRP^-1 * thisNewRest == thisNewRelativeToParent
            # parentOS * thisNewRelativeToParent == ThisCurrentLocalSpace
            
            if JuHuaCan:
                matrixDict[bI.name] = (parentBoneRP.inverted() @ boneRP).inverted() @ parentOS.inverted() @ boneOS
            else:
                matrixDict[bI.name] = (parentBoneRP.inverted() * boneRP).inverted() * parentOS.inverted() * boneOS
     
    action = obj.animation_data.action #bpy.data.actions["action_id"]

    print()

    print("Current take : ", action.name)        
               
    deltaDictRef = buildComparee(action)

    for boneName in deltaDictRef:
        mm = matrixDict[boneName]
        loc0, rot0, sca0 = mm.decompose()
        #print(boneName)
        transFormDiff = deltaDictRef[boneName]

        qBuild = Quaternion(transFormDiff.rotationBuild)
        transFormDiff.rot0 = rot0
        transFormDiff.qDiff = qBuild.rotation_difference(rot0)
            
    deltaDict = buildAllComparee(action)

    for keys in deltaDict:
        print("process2", keys)
        transFormRef = deltaDictRef[getBoneNameInDPath(keys)]
        transFormDiff = deltaDict[keys]
        
        transFormDiff.qRot = Quaternion(transFormDiff.rotationBuild)
        
        if JuHuaCan:
            transFormDiff.qRot = transFormDiff.qRot @ transFormRef.qDiff
        else:
            transFormDiff.qRot = transFormDiff.qRot * transFormRef.qDiff


    for curveI in action.fcurves:
        dPath = curveI.data_path
        boneName = getBoneNameInDPath(dPath)
        print(eval("obj."+dPath))
        dIdx = curveI.array_index
        print(dPath + " Channel#" + str(dIdx))
        tranfrom_type = 0
        if(dPath.find("location")!=-1): 
            tranfrom_type=0
        if(dPath.find("rotation")!=-1): 
            tranfrom_type=1
        if(dPath.find("scale")!=-1) :
            tranfrom_type=2
        for kI in curveI.keyframe_points:
            co = kI.co;
            key = boneName+"#"+str(co.x)#+"#"+tranfrom_type+"#"+dIdx
            transFormDiff = deltaDict[key]
            if(tranfrom_type==1):
                #co.y = transFormDiff.rotationBuild[dIdx]
                co.y = transFormDiff.qRot[dIdx]
                
    for curveI in action.fcurves:
        curveI.update()
