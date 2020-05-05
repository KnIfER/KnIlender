import bpy
import bones

import importlib
importlib.reload(bones)

#bpy.ops.transform.rotate(value=0.996455, axis=(1, 0, 0), constraint_axis=(True, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, release_confirm=True, use_accurate=False)

def getInfoCatalogs():
    context = bpy.context
    info = context.screen.areas[len(context.screen.areas)-1] # do properly
    c = context.copy()
    c["area"] = info
    bpy.ops.info.select_all_toggle(c)
    bpy.ops.info.report_copy(c)
    clipboard = bpy.context.window_manager.clipboard
    return clipboard

def getDoList(logs):
    arr = logs.split('\n')
    dol = ''
    for arrI in arr:
        if arrI.startswith('bpy.ops.transform'):
            dol += arrI+'\n'
    return dol

def execute():
    clipboard = getInfoCatalogs()

    if clipboard=='':
        clipboard = getInfoCatalogs()

    print('clipboard', clipboard)
    
    obj = bpy.context.object
    
    action = obj.animation_data.action

    selected_bone_name = bones.getSelectedBoneName()
    
    if clipboard!='' and selected_bone_name:
        #repeat operations for one bone on every keyframes
        
        DoList = getDoList(clipboard)
        
        #first fetch all channels in all keyframes for all bones
        deltaDict = bones.buildAllComparee(action)
        
        scene = bpy.context.scene
        
        nowFrame = scene.frame_current
        
        for frame in range(scene.frame_start, scene.frame_end + 1):
            framekey = selected_bone_name+"#"+str(frame*1.0)
            if framekey in deltaDict:
                scene.frame_set(frame)
                print('Do了', framekey)
                exec(DoList)
                bpy.ops.anim.keyframe_insert_menu(type='Rotation')
                #break
        
        scene.frame_set(1)
        
    
    
    
    
    
    
    

if __name__ == '__main__':
    execute()



