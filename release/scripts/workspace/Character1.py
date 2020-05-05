import bpy
import os
import re

bpy.ops.wm.save_mainfile()

template = '\n    - serializedVersion: 16\n\
      name: %s\n\
      takeName: %s\n\
      internalID: 0\n\
      firstFrame: %d\n\
      lastFrame: %d\n\
      wrapMode: 0\n\
      orientationOffsetY: 0\n\
      level: 0\n\
      cycleOffset: 0\n\
      loop: 0\n\
      hasAdditiveReferencePose: 0\n\
      loopTime: 1\n\
      loopBlend: 0\n\
      loopBlendOrientation: 0\n\
      loopBlendPositionY: 0\n\
      loopBlendPositionXZ: 0\n\
      keepOriginalOrientation: 0\n\
      keepOriginalPositionY: 1\n\
      keepOriginalPositionXZ: 0\n\
      heightFromFeet: 0\n\
      mirror: 0\n\
      curves: []\n\
      events: []\n\
      transformMask: []\n\
      maskType: 3\n\
      maskSource: {instanceID: 0}\n\
      additiveReferencePoseFrame: 0'
      
templateStart='\n    - serializedVersion: 16\n\
      name: '
templateEnd='\n    -'
templateEnd2='\n      additiveReferencePoseFrame'
      
print(template%('Clip Name','Clip Name',11,0))

class TakeRecord:
    name=''
    ff=0
    lf=0
    def __init__(self, name, range):
        print("TakeRecord __init__!!!")
        self.name = name
        self.ff = (int)(range.x-1)
        self.lf = (int)(range.y-1)
        
TakeRecords = {}

for a in bpy.data.actions:
    print(a.name) 
    print(a.fcurves) 
    print(a.frame_range) 
    print(a.pose_markers) 
    TakeRecords[a.name] = TakeRecord(a.name, a.frame_range)

def appendAllLeft():
    val=''
    for TRI in TakeRecords: 
        nowRecord = TakeRecords[TRI]
        if nowRecord.ff<=nowRecord.lf and nowRecord.ff>=0:
            val+=template%(nowRecord.name,nowRecord.name,nowRecord.ff,nowRecord.lf)
            print("append new:", nowRecord.name)
    return val

PatternNM='name: (.*)'
PatternFF='firstFrame: (.*)'
PatternLF='lastFrame: (.*)'
     
def processTake(take):
    mTake = re.search(PatternNM, take)
    ret = take
    changed = False
    if mTake:
        print("[Name] ", mTake.group())
        mTakeName=mTake.group(1)
        nowRecord = TakeRecords.get(mTakeName)
        if nowRecord:
            TakeRecords.pop(mTakeName)
        if nowRecord and nowRecord.ff<=nowRecord.lf and nowRecord.ff>=0:
            #print("\nm Clip recorded found match :", nowRecord)
            #Locate first frame. Replace or append afterwards if records not match.
            mTake = re.search(PatternFF, take)
            val1=0
            val2=0
            if mTake:
                val1 = int(mTake.group(1))
                print("{firstFrame} ", val2)
                if val1!=nowRecord.ff:
                    take = take.replace(mTake.group(), 'firstFrame: '+str(nowRecord.ff))
                    changed = True
            else:
                take = take+('\nfirstFrame: '+str(nowRecord.ff));
                changed = True
            #Locate last frame. Replace or append afterwards if records not match.
            mTake = re.search(PatternLF, take)
            if mTake:
                val2 = int(mTake.group(1))
                print("{lastFrame} ", val2)
                if val2!=nowRecord.lf:
                    take = take.replace(mTake.group(), 'lastFrame: '+str(nowRecord.lf))
                    changed = True
            else:
                take = take+('\nlastFrame: '+str(nowRecord.lf));
                changed = True
            ret = take
            if changed:
                print("{key frame changed before}:", val1, val2)
                print("{key frame changed after}::", nowRecord.ff, nowRecord.lf)
        else:
            print("{---removing---} ", mTakeName)
            ret = ''
            changed = True
    else:
        print("!!!???:", mTake.group())
    #error:name field not found   
    return ret, changed
    
LineEnd = "\n"

def getNextBlockStart(idxST):
    ret = metaData.find(templateStart, idxST)
    if ret>0:
        return ret, False
    len2 = len(metaData)
    while True:
        ret = metaData.find(LineEnd, idxST)
        if ret<0:
            break
        for i in range(1, 6):
            if ret+i>=len2:
                break;
            if metaData[ret+i]!=" ":
                return ret, True
            else:
                idxST = ret + 1
    return len2, True

metaData=""
dirname=os.path.dirname(bpy.context.blend_data.filepath)
filename=bpy.path.basename(bpy.context.blend_data.filepath)+'.meta'
metaTarget=os.path.join(dirname, filename)
print(metaTarget, os.path.isfile(metaTarget)) 
if os.path.isfile(metaTarget):
    f = open(metaTarget,'r')
    metaData = f.read()
    f.close()
    idx = metaData.find('clipAnimations: []')
    needWrite=0
    # Directly inset or compare and then modify
    if idx>0:
        part1 = metaData[0:idx+15]
        part2 = metaData[idx+18:]
        middle=''
        for a in bpy.data.actions:
            middle+=template%(a.name,a.name,a.frame_range.x-1,a.frame_range.y-1)
        result = part1+middle+part2;
        f = open(metaTarget,'r+')
        f.write(result)
        f.close()
        print('writing done......')
    else:
        metaDoc = ''
        lastEnd=0
        idxTS = metaData.find(templateStart)
        stIdx = idxTS
        if idxTS>0:
            while idxTS>0:
                metaDoc += metaData[lastEnd:idxTS]
                idxTS+=len(templateStart)
                idxEnd, endIdx = getNextBlockStart(idxTS)
                if idxEnd>0:
                    take = metaData[idxTS-len(templateStart):idxEnd]
                    print('parsing take : ', take)
                    lastEnd=idxTS=idxEnd
                    take, changed = processTake(take)
                    if changed:
                        needWrite=1
                    metaDoc += take
                if endIdx:
                    print("↑↑↑ ↑↑↑ ↑↑↑")
                    break
                idxTS = metaData.find(templateStart, idxTS)
                
            if not needWrite and len(TakeRecords)>0:
                needWrite=True
                lastEnd=stIdx;
                metaDoc = metaData[0:lastEnd]
                
            if needWrite or len(TakeRecords)>0:
                metaDoc += appendAllLeft() # insert new items
                metaDoc += metaData[lastEnd:]
                f = open(metaTarget,'r+')
                f.write(metaDoc)
                f.close()
        
        #print("metaDoc", metaDoc)