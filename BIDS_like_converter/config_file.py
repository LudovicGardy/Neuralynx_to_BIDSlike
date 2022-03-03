import os

def get_config():

    json_dict = {
        "info": "This file lists the experimental task names that can be used in the GUI to name BIDS or BIDS-like files.",
        "possible_tasknames": ["Stimic", "Imagery", "EPIFAR", "SAB", "Oddball"],
        "possible_ext": [".ncs",".nrd",".trc"]
    }

    return(json_dict)

def get_path():

    root = os.getcwd()

    path_dict = {

        "root" : root,
        "icon_path" : os.path.join(root, "BIDS_like_converter", "static", "icones")
    }

    return path_dict
