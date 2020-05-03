Python side : https://github.com/KnIfER/blender-addons

### Scriptlets :   
[workspace/bones.py](https://github.com/KnIfER/KnIlender/blob/blender-v2.79b-release/release/scripts/workspace/bones.py)  
###### Armature Animation Offsetter
######  ——  [WIP]Add transform to current action. Idea comes from the aniamiton editor of Unreal Engine 4.

[workspace/Character1.py](https://github.com/KnIfER/KnIlender/blob/blender-v2.79b-release/release/scripts/workspace/Character1.py)
###### Unity metadata utility
###### ——  Unity 2019 can still parse the animation clips correctly, but it failed to record them in the .meta file. This is a help.

### Compile (Windows) : 
Just follow blender's official guide. You can use svn or wget(recommended) to download those [precompiled v2.79 dependencies](https://svn.blender.org/svnroot/bf-blender/tags/blender-2.79a-release/lib/win64_vc14/) (3.40GB).  
Or You can download compressed archives seprately : 
###### ——  Baidu SlowPan : [Common includes(pnek)](https://pan.baidu.com/s/1Pg_Bn0EbzB_2D7DLwdZ-Og)、[Release lib(jgib)](https://pan.baidu.com/s/1whwUdrLd_t-TW3rH_r0LoQ)、[Debug lib(idac)](https://pan.baidu.com/s/1y1gJJLfPzurR5i31LZe5Hw).
###### ——  Google drive: [Common includes(89MB)](https://drive.google.com/open?id=1MVy-N9iybt1xj45RtlZ24cbUU7JIM_v8)、[Release lib(57MB)](https://drive.google.com/open?id=1k7YCAEKybraIQtmODdZz5H1C6zDJf-7w)、[Debug lib(204MB)](https://drive.google.com/open?id=1p1XbkcU1z69emXkw0O5CygDPmZrFDeHN).

# Blender 2.79b mod

Why blender? Please refer to the workflow between Blender 2.79 and Unity 2019:

Unity natively support .blend files —— no need to export again and again. 

Blender file format being used as an asset format for Unity Game Engine! 

That's Amazing.  

Why mod? Mainly because it's fun!  

Why v2.79?  

I. Font is very small and cannot scale in previous versions. ~~(Same in foregone 'Unity's : What a pair of fellow sufferers!)~~  

II. v2.8 changed storage format and Unity can no longer recogonize it's animations.

