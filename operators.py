import json
import os
import bpy
import tempfile
from bpy_extras.io_utils import ImportHelper
from .scene import Layout
from .llm_utils import ask_newobject, ask_nextobject
from .utils import create_collection, degrees2radians
from .object_generator import get_generator, ClayAPI
from bpy_extras.object_utils import AddObjectHelper, object_data_add
import numpy as np
import math
import trimesh


class SceneGen_OT_initbbox(bpy.types.Operator):
    bl_idname = "scenegen.initbbox"
    bl_label = "Init BBox"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        object_collection = create_collection("generated_objects")
        bbox_collection = create_collection("layout_bbox")
        # first, remove all objects and meshes
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
        Layout(context.scene.layout).init_bbox()
        return {"FINISHED"}


# generate objects
class SceneGen_OT_genobj(bpy.types.Operator, AddObjectHelper):
    bl_idname = "scenegen.genobj"
    bl_label = "GenObj"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # get the current chosen obj description
        obj_name = context.object.name
        obj_desc = context.object.description
        bbox = [
            context.object.dimensions[0],
            context.object.dimensions[2],
            context.object.dimensions[1],
        ]
        location = context.object.location
        angles = context.object.rotation_euler.z
        generator: ClayAPI = get_generator("ClayAPI")
        tri_mesh = generator.generate_by_text_bbox([obj_desc], [bbox])[0]

        mesh = bpy.data.meshes.new(name=obj_name)
        mesh.from_pydata(np.array(tri_mesh.vertices), [], np.array(tri_mesh.faces))

        gen_objname = "gen_" + obj_name
        if gen_objname in bpy.data.objects:
            gen_obj = bpy.data.objects[gen_objname]
        else:
            gen_obj = object_data_add(context, mesh, operator=self, name=gen_objname)
            bpy.data.collections["generated_objects"].objects.link(gen_obj)
            # bpy.data.collections["Collection"].objects.link(gen_obj)
            # remove from deault scene collection
            default_collection = bpy.data.collections["Collection"]
            default_collection.objects.unlink(gen_obj)
        gen_obj.dimensions = bbox
        gen_obj.location = location
        gen_obj.rotation_euler = [math.radians(90), 0, angles]
        return {"FINISHED"}


# update objects of generated meshes
class SceneGen_OT_updateobjs(bpy.types.Operator, AddObjectHelper):
    bl_idname = "scenegen.updateobjs"
    bl_label = "UpdateObjs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        object_dir = os.path.join(context.scene.json_path, "../objects")
        for obj_bbox in bpy.data.collections["layout_bbox"].objects:
            obj_name = obj_bbox.name
            obj_desc = obj_bbox.description
            bbox = [
                obj_bbox.dimensions[0],
                obj_bbox.dimensions[2],
                obj_bbox.dimensions[1],
            ]
            location = obj_bbox.location
            angles = obj_bbox.rotation_euler.z
            # import object by path
            obj_path = os.path.join(object_dir, f"{obj_name}.obj")
            if obj_name in bpy.data.meshes:
                mesh = bpy.data.meshes[obj_name]
            else:
                tri_mesh = trimesh.load(obj_path)
                mesh = bpy.data.meshes.new(name=obj_name)
                mesh.from_pydata(
                    np.array(tri_mesh.vertices), [], np.array(tri_mesh.faces)
                )
            gen_objname = "gen_" + obj_name
            if gen_objname in bpy.data.objects:
                gen_obj = bpy.data.objects[gen_objname]
            else:
                gen_obj = object_data_add(
                    context, mesh, operator=self, name=gen_objname
                )
                bpy.data.collections["generated_objects"].objects.link(gen_obj)
                # bpy.data.collections["Collection"].objects.link(gen_obj)
                # remove from deault scene collection
                default_collection = bpy.data.collections["Collection"]
                default_collection.objects.unlink(gen_obj)
            gen_obj.dimensions = bbox
            gen_obj.description = obj_desc
            gen_obj.location = location
            gen_obj.rotation_euler = [math.radians(90), 0, angles]
        return {"FINISHED"}


# update layout bboxes
class SceneGen_OT_updatebbox(bpy.types.Operator):
    bl_idname = "scenegen.updatebbox"
    bl_label = "UpdateBBox"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        for obj_bbox in bpy.data.collections["layout_bbox"].objects:
            obj_name = obj_bbox.name
            gen_object = bpy.data.objects[f"gen_{obj_name}"]
            obj_bbox.dimensions = gen_object.dimensions
            obj_bbox.location = gen_object.location
            obj_bbox.rotation_euler = gen_object.rotation_euler

        return {"FINISHED"}


# add object by asking LLM
class SceneGen_OT_addobject(bpy.types.Operator):
    bl_idname = "scenegen.addobject"
    bl_label = "AddObject"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene_layout = Layout.export()
        new_object_name = context.scene.addobj_name
        newobject_dict = ask_newobject(new_object_name, f"{scene_layout}")

        Layout.add_object(newobject_dict)
        return {"FINISHED"}


class SceneGen_OT_addcube(bpy.types.Operator):
    bl_idname = "scenegen.addcube"
    bl_label = "TestGenerator"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        return {"FINISHED"}


# read json file operator from filebrowser
class SceneGen_OT_readjson(bpy.types.Operator, ImportHelper):
    bl_idname = "scenegen.readjson"
    bl_label = "Read JSON"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".json"

    def execute(self, context):
        # read json
        with open(self.filepath, "r") as f:
            # read layout
            context.scene.layout = str(json.load(f))
            self.report(
                {"INFO"},
                "JSON file loaded successfully \n"
                f" {Layout(context.scene.layout).objects}",
            )
        # update json file path
        context.scene.json_path = self.filepath
        return {"FINISHED"}


# export json file
class SceneGen_OT_exportjson(bpy.types.Operator, ImportHelper):
    bl_idname = "scenegen.exportjson"
    bl_label = "Export JSON"
    bl_options = {"REGISTER", "UNDO"}

    filename_ext = ".json"

    def execute(self, context):
        # export json and auto add extension
        with open(self.filepath, "w") as f:
            # read layout
            data = Layout.export()
            json.dump(data, f, indent=4)
            self.report({"INFO"}, f"JSON file exported successfully \n {data}")
        # update json file path
        context.scene.json_path = self.filepath
        return {"FINISHED"}
