import rpyc
import io
import trimesh


class ObjectGeneratorBase(object):
    def __init__(self, *args):
        super(ObjectGeneratorBase, self).__init__(*args)

    def generate(self, *args, **argvs):
        raise NotImplementedError


class ClayAPI(object):
    def __init__(self, *args):
        super(ClayAPI, self).__init__(*args)
        conn = rpyc.connect(
            "10.15.89.180",
            18812,
            config={"allow_all_attrs": True, "allow_pickle": True},
        )
        self.remote = conn.root

    def _infer_one(self, prompt, bbox):
        _, glb = self.remote.inference(
            conditions=[
                # ["bbox", [1, 0.5, 1], True],
                ["bbox", bbox, True],
                # ["voxel", voxel, True],
                # ["pcd", surface_sample, True, 0.05],
            ],
            condition_scales=[
                1,
            ],
            prompt=prompt,
        )
        glb_io = io.BytesIO(glb)
        mesh = trimesh.load(glb_io, file_type="glb", force="mesh")
        return mesh

    def generate_by_text_bbox(self, prompts, boxes):
        meshes = []
        for prompt, bbox in zip(prompts, boxes):
            bbox = [x / max(bbox) for x in bbox]
            meshes.append(self._infer_one(prompt, bbox))
        return meshes


def get_generator(generator: str, config=None) -> ObjectGeneratorBase:
    if generator == "ClayAPI":
        return ClayAPI()
    elif generator == "Direct3D":
        raise NotImplementedError("Direct3D method not support")
    elif generator == "Unique3D":
        raise NotImplementedError("Unique3D method not support")
