import folder_paths
import os
import json

# add path this directory to sys.path
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from nsfw_detector import predict

NSFW_MODEL = None


class Safety_Checker:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE",),
                "filename_prefix": ("STRING", {"default": "ComfyUI"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "BOOLEAN")
    RETURN_NAMES = ("images", "nsfws")
    FUNCTION = "nsfw_checker"

    CATEGORY = "image/postprocessing"

    def nsfw_checker(self, images, filename_prefix="ComfyUI"):
        global NSFW_MODEL

        if NSFW_MODEL is None:
            NSFW_MODEL = predict.load_model(os.path.join(folder_paths.models_dir, "nsfw_checker", "nsfw.299x299.h5"))

        nsfws = []
        preds_list = predict.classify(NSFW_MODEL, images, image_dim=299)
        for preds in preds_list:
            highest_key = max(preds, key=preds.get)
            if highest_key in ["hentai", "sexy", "porn"]:
                nsfws.append(True)
            else:
                nsfws.append(False)

        print("nsfws", nsfws)
        output_dir = folder_paths.get_output_directory()

        output_path = os.path.join(output_dir, f"{filename_prefix}_nsfw.json")

        json.dump(nsfws, open(output_path, "w+", encoding="utf-8"))

        return (images, nsfws)


NODE_CLASS_MAPPINGS = {
    "NSFWChecker": Safety_Checker,
}
