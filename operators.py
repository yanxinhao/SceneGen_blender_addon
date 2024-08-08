import json
import bpy

from bpy_extras.io_utils import ImportHelper
from .scene import Layout
from .llm_utils import ask_newobject, ask_nextobject


class SceneGen_OT_initbbox(bpy.types.Operator):
    bl_idname = "scenegen.initbbox"
    bl_label = "Init BBox"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # first, remove all objects
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
        Layout(context.scene.layout).init_bbox()
        return {"FINISHED"}


# add object by asking LLM
class SceneGen_OT_addobject(bpy.types.Operator):
    bl_idname = "scenegen.addobject"
    bl_label = "AddObject"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene_layout = Layout.export()
        new_object_name = context.scene.addobj_name
        newobject_dict = {
            new_object_name: ask_newobject(new_object_name, f"{scene_layout}")
        }

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
