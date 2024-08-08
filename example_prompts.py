max_objs = 20

image2layout_prompt = (
    "I want to construct a 3D scene dataset which consists of different scenes of"
    " various scale levels, like mountain, city, road, river, room and desktop etc."
    " Each scene consists of two parts : 1. objects (like chair, human, boat, building"
    ' etc ) as the main data of a scene 2. the whole "terrain"(like a plane, a bevel,'
    " an arc, and a wall on four sides) as the background. Please give me one scene"
    " which should be in the JSON format and contain layout parameters and description"
    " for image generation. There must not be any collision between objects."
    " Translations is the location of object which means the center point of the bottom"
    " of the bounding box. Sizes means the real size of objects (the unit is meter)."
    " Angles means the Rotation angle around the vertical axis. The order of elements"
    " in translation, sizes follows x-y-z sequence. The ground plane's y coordination"
    " is 0. Please do not describe the background or atmosphere, like cloud, sky,"
    " plane, mountain,ground,etc. Just consider object-level things. And the"
    " description for each element only describe the single object itself, not"
    " including the infomation of position relations. And the description should be"
    " accurate and typical. The number of objects in each scene should not be more than"
    " {max_objs}. Remember that it must not be any collision between objects. Put all"
    " objects on the ground (the y coordinate of translation must be 0,equal to"
    " ground)!"
)

add_object_prompt = (
    lambda object_name, scene_info: (
        f"You are a 3d scene designer in CG. Here is a scene layout : {scene_info}."
        " Translations is the location of object which means the center point of the"
        " bottom of the bounding box. Sizes means the real size of objects (the unit"
        " is meter). Angles means the Rotation angle around the vertical axis. The"
        " order of elements in translation, sizes follows x-y-z sequence. Ensure that"
        " the object is one the ground (The ground plane y coordination is 0). I will"
        " give you a new object name. Please give me the layout dict of the new object"
        f" and just return its layout in json format. The new object is : {object_name}"
    )
)

next_object_prompt = ""
