import bpy
import numpy as np
import math

degrees2radians = lambda rotation_degrees: tuple(math.radians(angle) for angle in rotation_degrees)
class Layout(object):
    def __init__(self,json_str: str) -> None:
        """scene layout

        Args:
            json_str (str): layout string
        """        
        self.objects:dict=eval(json_str)


    def init_bbox(self,y_vertical=True):
        # front face color
        if "RedMaterial" in list(bpy.data.materials.keys()):
            red_material = bpy.data.materials["RedMaterial"]
        else:
            red_material = bpy.data.materials.new(name="RedMaterial")
            red_material.diffuse_color = (1, 0, 0, 1)  # 设置为红色 (RGBA)
        for (obj_name,obj) in self.objects.items():
            
            prompt=obj["description"]
            bbox=np.array(obj["sizes"]).astype(np.float32)
            translation=np.array(obj["translations"]).astype(np.float32)
            translation[1]+=bbox[1]/2.0
            angles=np.array(obj["angles"])
            if y_vertical:
            # change to z vertical
                rotations=degrees2radians([0,0,angles])
                translation=[translation[0],-translation[2],translation[1]]
                bbox=[bbox[0],bbox[2],bbox[1]]
            else:
                rotations=degrees2radians([0,angles,0])

            bpy.ops.mesh.primitive_cube_add(size=1,location=translation,scale=bbox,rotation=rotations)
            cube = bpy.context.selected_objects[0]

            # set the frontal face in red
            if not cube.data.materials:
                cube.data.materials.append(bpy.data.materials["Material"])
            cube.data.materials.append(red_material)
            cube.data.polygons[3].material_index=1

            # change name
            cube.name = obj_name
            # change description 
            cube["description"] = prompt
        # add plane
        bpy.ops.mesh.primitive_plane_add(size=1,location=[0,0,0])
        plane = bpy.context.selected_objects[0]
        plane.name = "plane"
        plane.dimensions = [50,50,0]

    @classmethod
    def export(cls,y_vertical=True ) -> dict:
        objects={}
        for b_obj in bpy.data.objects:
            obj_name=b_obj.name
            f_obj={}
            f_obj["description"]=b_obj.description
            if y_vertical:
                sizes=[b_obj.dimensions[0],b_obj.dimensions[2],b_obj.dimensions[1]]
                translations=[b_obj.location[0],b_obj.location[2],-b_obj.location[1]]
                translations[1]-=sizes[1]/2.0
            else:
                sizes=list(b_obj.dimensions)
                translations=list(b_obj.location)
                translations[2]-=b_obj.dimensions[2]/2.0
            angles=math.degrees(b_obj.rotation_euler.z)
            f_obj["sizes"]=sizes
            f_obj["translations"]=translations
            f_obj["angles"]=angles
            objects[obj_name]=f_obj
        return objects