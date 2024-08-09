import bpy


def create_collection(collection_name):
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
        return new_collection
    else:
        return bpy.data.collections[collection_name]
