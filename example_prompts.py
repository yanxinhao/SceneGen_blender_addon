import json

max_objs = 20
single_object_template = (
    {
        "building": {
            "description": (
                "A tall skyscraper with visible neon lights outlining its structure."
            ),
            "translations": [0.0, 0.0, -9.788150787353516],
            "sizes": [2.0, 8.0, 2.0],
            "angles": 0.0,
        }
    },
)
image2layout_prompt = (
    "I want to build a 3D Scene look like this image but in 3D style. Please list the"
    " 3D Assets which should be in the JSON format and contain layout parameters and"
    " description. There must not be any collision between objects. Translations is"
    " the location of object which means the center point of the bottom of the"
    " bounding box. Sizes means the real size of objects (the unit is meter). Angles"
    " means the Rotation angle around the vertical axis. The order of elements in"
    " translation and sizes follows x-y-z sequence. The ground plane's y coordination"
    " is 0. The object which is in the center of the scene is set to be the original"
    " point (translation is [0,0,0]). Please do not describe the background, terrain"
    " or atmosphere, like cloud, sky, water, etc. Just consider object-level things."
    " And the description for each element only describes the single object itself,"
    " not including the infomation of position relations. And the description should"
    " be accurate and typical. Remember that it must not be any collision between"
    " objects. Maybe most objects are on the ground (the y coordinate of translation"
    " is 0,equal to ground)! And each object's direction(angles) should be accurate."
    " Ignore the objects with extreme size proportions, such as paper,wall,fence,etc."
    f" The output number of objects in each scene should not be more than {max_objs},"
    " which means mainly consider the objects with larger sizes. The output example"
    " json is like this. Please strictly follow the format :"
    f" {json.load(open('./example.json','r'))}"
)

add_object_prompt = (
    lambda object_name, scene_info: (
        f"You are a 3d scene designer in CG. Here is a scene layout : {scene_info}."
        " Translations is the location of object which means the center point of the"
        " bottom of the bounding box. Sizes means the real size of objects (the unit"
        " is meter). Angles means the Rotation angle around the vertical axis. The"
        " order of elements in translation, sizes follows x-y-z sequence. I will give"
        " you a new object name. Please give me the layout dict of the new object and"
        f" just return its layout in json format like this {single_object_template}:."
        " Ensure that the object is on the ground (The y coordination of new object in"
        " translation should be as same as the ground plane whose y coordination is"
        " 0). And the size of the new object should follow the real world. The new"
        f" object is : {object_name}"
    )
)

next_object_prompt = ""
