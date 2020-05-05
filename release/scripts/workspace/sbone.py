import bpy
import os
import re
from mathutils import *
import bones

import importlib
importlib.reload(bones)

def getRotationComponent(m):
    loc, rot, sca = m.decompose()
    return rot

def execute():
    print("\nStarting Add World-Space Animation Offset For Single Bone……\n")
    
    sce = bpy.context.scene

    obj = bpy.context.object

    poseBones = obj.pose.bones

    matrixDict = {}

    action = obj.animation_data.action
    
    selected_bone_name = bones.getSelectedBoneName()
        
    bI = poseBones[selected_bone_name]


    thisBone = bI.bone
    parentBone = thisBone.parent
    boneOS = bI.matrix
    parentOS = poseBones[parentBone.name].matrix
    boneRP = thisBone.matrix_local  # rest pose matrix in bone local space
    parentBoneRP = parentBone.matrix_local  # parent bone's rest pose matrix in bone local space

    matrixThis = boneOS

    # Assuming parent bone doesn't change

    deltaDictRef = bones.buildComparee(action)
    mm = boneOS
    loc0, rot0, sca0 = mm.decompose() # current pose in local space
    curve_rot0 = 0

    if selected_bone_name:
        transFormDiff = deltaDictRef[selected_bone_name]
        curve_rot0 = qBuild0 = Quaternion(transFormDiff.rotationBuild) # pose in the fcurve
        
        qBuild = qBuild0
        
        qm0 = qBuild.to_matrix().to_4x4()
        qm = parentOS * (parentBoneRP.inverted() * boneRP) * qm0
        qBuild = qm.to_quaternion()
        
        #qBuild = getRotationComponent(parentOS) * getRotationComponent(parentBoneRP.inverted()) * getRotationComponent(boneRP) * qBuild
        #qBuild = getRotationComponent(parentOS) * getRotationComponent(parentBoneRP.inverted()) * getRotationComponent(boneRP) * qBuild
        #qBuild = getRotationComponent((parentBoneRP.inverted()*boneRP)*parentOS) * qBuild
        
        #qBuild = qBuild * getRotationComponent((parentBoneRP.inverted() * boneRP))  * getRotationComponent(parentOS)
        #qBuild = qBuild * getRotationComponent(parentOS * (parentBoneRP.inverted() * boneRP))
        
        
        
        
        ##qBuild = qBuild0
        ##rot = getRotationComponent((parentBoneRP.inverted() * boneRP).inverted() * parentOS.inverted() * boneOS)
        ##transFormDiff.qDiff = rot - qBuild
        #print("diff is # 1:", rot)
        #print("diff is # 2:", qBuild)
        #print("diff is # 3:", rot - qBuild)
        
        
        qDiff = qBuild.rotation_difference(rot0)
        
        #qDiff = (qm0.inverted() * qDiff.to_matrix().to_4x4()).to_quaternion()
        
        var1 = getRotationComponent(parentOS) * getRotationComponent(parentBoneRP.inverted()) * getRotationComponent(boneRP) * qBuild
        var2 = getRotationComponent(parentOS) * getRotationComponent(parentBoneRP.inverted()) * getRotationComponent(boneRP) * rot0
        
        print("qDiff is:", qDiff.to_euler())
        print("rot0 is:", rot0.to_euler())
        print("val   is:", var1.to_euler())
        print("val 1 is:", var2.to_euler())
        
        print("diff is 1:", qBuild.to_euler())
        print("diff is 2:", rot0.to_euler())
        
    if True:
        return
        
    deltaDict = bones.buildAllComparee(action)

    for keys in deltaDict: # iterate over all bones and key frames
        if bones.getBoneNameInDPath(keys)==selected_bone_name:
            print("process2", keys)
            transFormRef = deltaDictRef[selected_bone_name]
            transFormDiff = deltaDict[keys]
            
            qRot = Quaternion(transFormDiff.rotationBuild) # pose in the fcurve
            
            #qRot1 = qRot * getRotationComponent(boneRP) * getRotationComponent(parentBoneRP.inverted())  * getRotationComponent(parentOS)
            #
            #qRot1 = qRot1 * transFormRef.qDiff
            #
            #qRot = qRot1 * getRotationComponent(parentOS.inverted()) * (getRotationComponent(boneRP) * getRotationComponent(parentBoneRP.inverted())).inverted()
        
            #qRot1 = qRot * getRotationComponent((parentBoneRP.inverted() * boneRP))  * getRotationComponent(parentOS)
            #
            #qRot1 = qRot1 * transFormRef.qDiff
            #
            #qRot = qRot1 * getRotationComponent(parentOS.inverted()) * getRotationComponent((parentBoneRP.inverted() * boneRP).inverted())
        
            
            #qRot1 =  qRot * getRotationComponent(parentOS * (parentBoneRP.inverted() * boneRP))
            #
            #qRot1 = qRot1 * transFormRef.qDiff
            #
            ##qRot = qRot1 * getRotationComponent((parentBoneRP.inverted() * boneRP).inverted() * parentOS.inverted())
            #qRot = qRot1 * getRotationComponent(parentOS * (parentBoneRP.inverted() * boneRP)).inverted()
            
            #qRot = qRot * transFormRef.qDiff
            
            qTmp = curve_rot0.rotation_difference(qRot)
            
            qRot += transFormRef.qDiff + qTmp
            
            
            transFormDiff.qRot = qRot
        
    print()

    for curveI in action.fcurves:
        dPath = curveI.data_path
        boneName = bones.getBoneNameInDPath(dPath)
        if boneName==selected_bone_name:
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


if __name__ == '__main__':
    execute()