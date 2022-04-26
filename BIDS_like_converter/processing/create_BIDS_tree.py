"""
Creation date: 2022, January 13
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""

import os
import shutil
import pandas as pd
import numpy as np
import json
import sys

from BIDS_like_converter.processing.create_BIDS_files import (create_dataset_description_json, create_participants_json, create_info_json, create_participants_tsv, create_session_tsv, create_scans_tsv, create_channels_tsv, create_events_tsv)


def create_BIDS_name(patient_num, sess_num, run_num, BIDSlike_folderpath, task_name):
    ### Setting up the different elements of the BIDS-like tree
    BIDS_full_name = "sub-{:03}_ses-NcsNlx{:02}_task-{}_run-{:02}".format(patient_num, sess_num, task_name, run_num)
    BIDS_tree_ncs = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-NcsNlx{:02}".format(run_num), "ieeg")
    BIDS_tree_rawdata = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-RawdataNlx{:02}".format(run_num), "ieeg")
    BIDS_tree_TRC = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-MacroMicromed{:02}".format(run_num), "ieeg")

    ### Save informations into a dictionnary
    path_info_dict = {"BIDSlike_folderpath": BIDSlike_folderpath,
                      "BIDS_full_name": BIDS_full_name,
                      "BIDS_tree_ncs": BIDS_tree_ncs,
                      "BIDS_tree_nrd": BIDS_tree_rawdata,
                      "BIDS_tree_trc": BIDS_tree_TRC}

    print("Path info:")
    for key in path_info_dict:
        print("   - {}: {}".format(key, path_info_dict[key]))

    return(path_info_dict)


def ncs_to_BIDSlike(current_path, path_info_dict, micro_identifier, proceed=False):
    ### Initialize variables
    electrodes_names_and_scales_matching_dict = {"electrode_name": [], "recording_scale": []}
    micro_names_list = []
    macro_names_list = []
    micro_idx_list = []
    macro_idx_list = []

    ### Split the original file path
    root = os.path.split(current_path)[0]
    current_folder_name = os.path.split(current_path)[1]

    ### Print electrode names and scales
    electrodes_scales_tsv_filepath = os.path.join(current_path, 'Electrodes names and scales matching.tsv')

    if os.path.isfile(electrodes_scales_tsv_filepath):
        electrodes_names_and_scales_matching_dict = pd.read_csv(electrodes_scales_tsv_filepath, sep='\t')
        micro_idx_list = np.where(electrodes_names_and_scales_matching_dict["recording_scale"] == "micro")[0]
        macro_idx_list = np.where(electrodes_names_and_scales_matching_dict["recording_scale"] == "macro")[0]
        is_tsv_matching_file = True
    else:
        is_tsv_matching_file = False
        proceed = False
        print("The << Electrodes names and scales matching.tsv >> file that should be inside the Neuralynx ncs folder is missing. See example dataset provided with this program for more information.")

    if len(micro_idx_list) >= 1:
        print("EEG-micro channels:")
        for micro_idx in micro_idx_list:
            print(f"   - {electrodes_names_and_scales_matching_dict['electrode_name'][micro_idx]}")
            micro_names_list.append(electrodes_names_and_scales_matching_dict['electrode_name'][micro_idx])
    else:
        print("No EEG-micro channels detected")

    if len(macro_idx_list) >= 1:
        print("EEG-macro channels:")
        for macro_idx in macro_idx_list:
            print(f"   - {electrodes_names_and_scales_matching_dict['electrode_name'][macro_idx]}")
            macro_names_list.append(electrodes_names_and_scales_matching_dict['electrode_name'][macro_idx])
    else:
        print("No EEG-macro channels detected")

    ### Rename channels (add 'micro' or 'macro' the the name)
    ncs_filenames_list = []
    for filename in os.listdir(current_path):
        if ".ncs" in filename:
            ncs_filenames_list.append(filename)

    ncs_renamed_list = []
    micro_identifier_length = len(micro_identifier)
    for filename in ncs_filenames_list:
        filename_nodigit = ''.join([i for i in filename if not i.isdigit()])
        if filename[:micro_identifier_length] == micro_identifier and filename_nodigit.replace(".ncs", "") in micro_names_list:
            ncs_renamed_list.append(f"micro {filename[micro_identifier_length:]}")
            print(f"< {filename} > renamed as: < micro {filename[micro_identifier_length:]} >")
        else:
            ncs_renamed_list.append(f"macro {filename}")
            print(f"< {filename} > renamed as: < macro {filename} >")

    ### Rename all the channel names in the containing folder
    for original_filname, renamed_filename in zip(ncs_filenames_list, ncs_renamed_list):
        if proceed and ("macro" not in original_filname) and ("micro" not in original_filname):
            os.rename(os.path.join(current_path, original_filname), os.path.join(current_path, renamed_filename))
            print("{} was changed to:    {}".format(original_filname, renamed_filename))
        else:
            print("{} was NOT changed to:    {}".format(original_filname, renamed_filename))

    ### Search or create tree structure
    if proceed:
        if os.path.join(root, current_folder_name) != os.path.join(root, path_info_dict["BIDS_full_name"]):
            os.rename(os.path.join(root, current_folder_name), os.path.join(root, path_info_dict["BIDS_full_name"]))
        else:
            print("Folder name already exists. Overwrite = False.")

        if not os.path.exists(path_info_dict["BIDS_tree_ncs"]):
            os.makedirs(path_info_dict["BIDS_tree_ncs"])
        else:
            print("Path already exists. Overwrite = False.")

    ### Affect channels data to the good place in our tree structure
    source = os.path.join(root, path_info_dict["BIDS_full_name"])
    destination = os.path.join(path_info_dict["BIDS_tree_ncs"], path_info_dict["BIDS_full_name"])

    if proceed:
        if not os.path.exists(destination):
            shutil.move(source, destination)
            write_BIDS_files(path_info_dict, format="ncs")
        else:
            print("Folder already exists. Overwrite = False.")

    return(ncs_renamed_list, destination, is_tsv_matching_file)


def write_BIDS_files(path_info_dict, format, write=True):
    ### Split path
    path_components = []
    path = path_info_dict[f"BIDS_tree_{format.lower()}"]
    path = os.path.normpath(path)
    path = path.split(os.sep)
    [path_components.append(_comp) for _comp in path if _comp]

    ### Root part (level 1) of the BIDS directory
    BIDS_depth = 5  # levels
    full_path_depth = len(path_components)  # levels
    BIDS_root_position = full_path_depth - BIDS_depth + 2
    BIDS_root_path = "/".join(path_components[0:BIDS_root_position])
    if os.name != "nt":
        BIDS_root_path = f"{'/'}{BIDS_root_path}"

    BIDS_root_listdir = next(os.walk(BIDS_root_path))[1]  # (dirnames, filenames)

    create_dataset_description_json(BIDS_root_path, write)
    create_participants_json(BIDS_root_path, write)
    create_participants_tsv(BIDS_root_path, BIDS_root_listdir, write)

    ### Level 2 of the BIDS directory
    create_session_tsv(BIDS_root_path, BIDS_root_listdir, write)

    ### Level 3 of the BIDS directory
    create_scans_tsv(BIDS_root_path, BIDS_root_listdir, write)

    ### Level 5 of the BIDS directory (skip level 4, it is just always "ieeg" for the moment)
    json_level5_path, foldername_level4, channels_dict = create_channels_tsv(BIDS_root_path, BIDS_root_listdir, write)
    create_info_json(json_level5_path, foldername_level4, format, write)


def rawdata_to_BIDSlike(current_path, path_info_dict, proceed=False):
    ### Rename all the channel names in the containing folder
    ext = ".nrd"
    root = os.path.split(current_path)[0]
    current_filename = os.path.split(current_path)[1]
    renamed_filename = path_info_dict["BIDS_full_name"] + ext
    renamed_filepath = os.path.join(root, renamed_filename)

    destination = os.path.join(path_info_dict["BIDS_tree_nrd"], renamed_filename)

    if proceed:
        ### Rename file
        os.rename(current_path, renamed_filepath)

        ### Create folder path
        if not os.path.exists(path_info_dict["BIDS_tree_nrd"]):
            os.makedirs(path_info_dict["BIDS_tree_nrd"])
        else:
            print("Path already exists. Overwrite = False.")

        ### Cut / paste in the good location of our BIDS-like tree
        if not os.path.isfile(destination):
            shutil.move(renamed_filepath, destination)
        else:
            print("File already exists. Overwrite = False.")

    return(destination)


def TRC_to_BIDSlike(current_path, path_info_dict, proceed=False):
    ### Rename all the channel names in the containing folder
    ext = ".TRC"
    root = os.path.split(current_path)[0]
    current_filename = os.path.split(current_path)[1]
    renamed_filename = path_info_dict["BIDS_full_name"] + ext
    renamed_filepath = os.path.join(root, renamed_filename)

    destination = os.path.join(path_info_dict["BIDS_tree_trc"], renamed_filename)

    if proceed:
        ### Rename file
        os.rename(current_path, renamed_filepath)

        ### Create folder path
        if not os.path.exists(path_info_dict["BIDS_tree_trc"]):
            os.makedirs(path_info_dict["BIDS_tree_trc"])
        else:
            print("Path already exists. Overwrite = False")

        ### Cut / paste in the good location of our BIDS-like tree
        if not os.path.isfile(destination):
            shutil.move(renamed_filepath, destination)
        else:
            print("File already exists. Overwrite = False")

    return(destination)


if __name__ == "__main__":

    root_path = r"F:\GardyL\Python\BIDS_like_converter"
    sys.path.append(root_path)
    from create_BIDS_files import (create_dataset_description_json, create_participants_json, create_info_json, create_participants_tsv, create_session_tsv, create_scans_tsv, create_channels_tsv, create_events_tsv)

    ### Load config file
    config_file_path = r"F:\GardyL\Python\BIDS_like_converter\config_file.json"
    json_dict = json.load(open(config_file_path))
    possible_tasknames = json_dict["possible_tasknames"]
    print(f"Possible task names: {possible_tasknames}")

    ### Set parameters
    patient_num = 70
    sess_num = 1
    run_num = 1

    task_name = "Stimic"
    micro_identifier = "t"

    BIDSlike_folderpath = r"F:\GardyL\Python\BIDS_like_converter\srv-data-example\BIDSlike_database"

    ### proceed
    #- Get path info and define BIDS-like path
    path_info_dict = create_BIDS_name(patient_num, sess_num, run_num, BIDSlike_folderpath, task_name)

    #- From current .ncs structure to BIDS-like .ncs structure
    ncs_folderpath = r"F:\GardyL\Python\BIDS_like_converter\srv-data-example\donnees patients\example 2\epifar jour 1"
    ncs_renamed_list, ncs_destination, is_tsv_matching_file = ncs_to_BIDSlike(ncs_folderpath, path_info_dict, micro_identifier, proceed=True)

    #- From current .nrd structure to BIDS-like .nrd structure
    rawdata_filepath = r"F:\GardyL\Python\BIDS_like_converter\srv-data-example\donnees patients\example 2\epifar j1.nrd"
    rawdata_destination = rawdata_to_BIDSlike(rawdata_filepath, path_info_dict, proceed=True)

    #- From current .TRC structure to BIDS-like .TRC structure
    TRC_filepath = r"F:\GardyL\Python\BIDS_like_converter\srv-data-example\donnees patients\example 2\EPIFARjour1.TRC"
    TRC_destination = TRC_to_BIDSlike(TRC_filepath, path_info_dict, proceed=True)
