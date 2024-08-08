# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from .operators import (
    SceneGen_OT_addcube,
    SceneGen_OT_readjson,
    SceneGen_OT_initbbox,
    SceneGen_OT_exportjson,
    SceneGen_OT_addobject,
)

bl_info = {
    "name": "Scenegen",
    "author": "yanxinhao",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}


class OBJECT_PT_property(bpy.types.Panel):
    bl_label = "Semantic Property"
    bl_idname = "OBJECT_PT_property"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        layout.prop(obj, "name")
        layout.prop(obj, "description")
        layout.prop(obj, "dimensions")


class SceneGenPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_scenegen"
    bl_label = "SceneGen"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SceneGen"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Load the layout json file:")
        row = layout.row()
        # get scene file from file browser and update json file path
        row.prop(context.scene, "json_path")
        row.operator("scenegen.readjson", text="Read JSON")

        # show bbox
        row.operator("scenegen.initbbox", text="Init BBox")

        # export json file
        layout.label(text="Add object by name:")
        row = layout.row()
        row.prop(context.scene, "addobj_name")
        row.operator("scenegen.addobject", text="Add Object")

        layout.operator("scenegen.addcube", text="Generate cube")
        layout.operator("scenegen.exportjson", text="Export JSON")


classes = [
    SceneGen_OT_addcube,
    OBJECT_PT_property,
    SceneGenPanel,
    SceneGen_OT_readjson,
    SceneGen_OT_exportjson,
    SceneGen_OT_initbbox,
    SceneGen_OT_addobject,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # add object description and size vector property
    bpy.types.Object.description = bpy.props.StringProperty(
        name="Description",
        description="Description of this object",
        default="test description",
    )
    # add scene json file path
    bpy.types.Scene.json_path = bpy.props.StringProperty(
        name="JSON Path", description="JSON file path", default="test.json"
    )

    bpy.types.Scene.layout = bpy.props.StringProperty(
        name="Layout", description="Layout of the scene", default="{}"
    )

    bpy.types.Scene.addobj_name = bpy.props.StringProperty(
        name="Object Name",
        description="the name of the added object",
        default="test_cube",
    )


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
