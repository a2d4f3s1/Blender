## メッシュ名をオブジェクト名に変更し、メッシュリンクなオブジェクトを選択

import bpy
objects = bpy.data.objects
shareObjects = list()

## Deselect All
for object in objects:
    bpy.context.scene.objects[(object.name)].select_set(False)

## Copy Name obj to mesh
for obj in objects:
    if obj.data and obj.data.users == 1: ## if no shared mesh
        obj.data.name = obj.name
    else :
        print (obj)
        shareObjects.append(obj)

## Select Linked mesh obj
for obj in shareObjects:
    bpy.context.scene.objects[(obj.name)].select_set(True)
