import bpy
import numpy as np

class Layout(object):
    def __init__(self,json_str: str) -> None:
        """scene layout

        Args:
            json_str (str): layout string
        """        
        self.objects:dict=eval(json_str)


    def init_bbox(self):
        for (obj_name,obj) in self.objects.items():
            
            prompt=obj["description"]
            bbox=np.array(obj["sizes"]).astype(np.float32)
            translation=np.array(obj["translations"]).astype(np.float32)
            translation[1]+=bbox[1]/2.0
            angles=np.array(obj["angles"])

            bpy.ops.mesh.primitive_cube_add(size=1,location=translation,scale=bbox,rotation=[0,angles,0])
            cube = bpy.context.selected_objects[0]
            # change name
            cube.name = obj_name
            # change description 
            cube["description"] = prompt

    @classmethod
    def export(cls) -> dict:
        objects={}
        for b_obj in bpy.data.objects:
            obj_name=b_obj.name
            f_obj={}
            f_obj["description"]=b_obj.description
            f_obj["sizes"]=list(b_obj.dimensions)
            f_obj["translations"]=list(b_obj.location)
            f_obj["translations"][1]-=b_obj.dimensions[1]/2.0
            f_obj["angles"]=b_obj.rotation_euler.y
            objects[obj_name]=f_obj
        return objects