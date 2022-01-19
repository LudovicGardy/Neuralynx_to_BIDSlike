"""
Creation date: 13/01/2022
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""

import os
import shutil
import pandas as pd
import numpy as np

def path_to_BIDSlikepath(patient_num, sess_num, run_num, BIDSlike_folderpath, task_name):
    ### Check if the name task has the good writting
    if task_name not in possible_tasknames:
        print("Raise Error (add later)")

    ### Setting up the different elements of the BIDS-like tree
    BIDS_full_name = "sub-{:03}_ses-NcsNlx{:02}_task-{}_run-{:02}".format(patient_num, sess_num, task_name, run_num)
    BIDS_tree_ncs = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-NcsNlx{:02}".format(run_num), "ieeg")
    BIDS_tree_rawdata = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-RawdataNlx{:02}".format(run_num), "ieeg")
    BIDS_tree_TRC = os.path.join(BIDSlike_folderpath, "sub-{:03}".format(patient_num), "ses-MacroMicromed{:02}".format(run_num), "ieeg")

    ### Save informations into a dictionnary
    path_info_dict = {"BIDSlike_folderpath":BIDSlike_folderpath,
                      "BIDS_full_name":BIDS_full_name,
                      "BIDS_tree_ncs":BIDS_tree_ncs,
                      "BIDS_tree_rawdata":BIDS_tree_rawdata,
                      "BIDS_tree_TRC":BIDS_tree_TRC}

    print("Path info:")
    for key in path_info_dict:
        print("   - {}: {}".format(key, path_info_dict[key]))

    return(path_info_dict)

def ncs_to_BIDSlike(current_path, path_info_dict, micro_identifier, process = False):
    ### Split the original file path
    root = os.path.split(current_path)[0]
    current_folder_name = os.path.split(current_path)[1]

    ### Print electrode names and scales
    electrodes_scales_tsv_filepath = os.path.join(current_path,'Electrodes names and scales matching.tsv')
    electrodes_names_and_scales_matching_dict = pd.read_csv(electrodes_scales_tsv_filepath, sep='\t')
    micro_idx_list = np.where(electrodes_names_and_scales_matching_dict["scale"] == "micro")[0]
    macro_idx_list = np.where(electrodes_names_and_scales_matching_dict["scale"] == "macro")[0]
    micro_names_list = []
    macro_names_list = []

    if len(micro_idx_list)>=1:
        print("EEG-micro channels:")
        for micro_idx in micro_idx_list:
            print(f"   - {electrodes_names_and_scales_matching_dict['electrode name'][micro_idx]}")
            micro_names_list.append(electrodes_names_and_scales_matching_dict['electrode name'][micro_idx])
    else:
        print("No EEG-micro channels detected")

    if len(macro_idx_list)>=1:
        print("EEG-macro channels:")
        for macro_idx in macro_idx_list:
            print(f"   - {electrodes_names_and_scales_matching_dict['electrode name'][macro_idx]}")
            macro_names_list.append(electrodes_names_and_scales_matching_dict['electrode name'][macro_idx])
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
        if filename[:micro_identifier_length] == micro_identifier and filename_nodigit.replace(".ncs","") in micro_names_list:
            ncs_renamed_list.append(f"micro {filename[micro_identifier_length:]}")
            print(f"< {filename} > renamed as: < micro {filename[micro_identifier_length:]} >")
        else:
            ncs_renamed_list.append(f"macro {filename}")
            print(f"< {filename} > renamed as: < macro {filename} >")

    ### Rename all the channel names in the containing folder
    for original_filname, renamed_filename in zip(ncs_filenames_list,ncs_renamed_list):
        if process and ("macro" not in original_filname) and ("micro" not in original_filname):
            os.rename(os.path.join(current_path, original_filname),os.path.join(current_path,renamed_filename))
            print("{} was changed to:    {}".format(original_filname,renamed_filename))
        else:
            print("{} was NOT changed to:    {}".format(original_filname,renamed_filename))

    ### Search or create tree structure
    if process:
        if os.path.join(root, current_folder_name) != os.path.join(root,path_info_dict["BIDS_full_name"]):
            os.rename(os.path.join(root, current_folder_name),os.path.join(root,path_info_dict["BIDS_full_name"]))
        else:
            print("folder name already exists")

        if not os.path.exists(path_info_dict["BIDS_tree_ncs"]):
            os.makedirs(path_info_dict["BIDS_tree_ncs"])
        else:
            print("Path already exists. Overwrite = False")

    ### Affect channels data to the good place in our tree structure
    source = os.path.join(root, path_info_dict["BIDS_full_name"])
    destination = os.path.join(path_info_dict["BIDS_tree_ncs"], path_info_dict["BIDS_full_name"])

    if process:
        if not os.path.exists(destination):
            shutil.move(source, destination)
        else:
            print("Folder already exists. Overwrite = False")

    return(destination)

def rawdata_to_BIDSlike(current_path, path_info_dict, process = False):
    ### Rename all the channel names in the containing folder
    ext = ".nrd"
    root = os.path.split(current_path)[0]
    current_filename = os.path.split(current_path)[1]
    renamed_filename = path_info_dict["BIDS_full_name"] + ext
    renamed_filepath = os.path.join(root, renamed_filename)

    destination = os.path.join(path_info_dict["BIDS_tree_rawdata"], renamed_filename)

    if process:
        ### Rename file
        os.rename(current_path,renamed_filepath)

        ### Create folder path
        if not os.path.exists(path_info_dict["BIDS_tree_rawdata"]):
            os.makedirs(path_info_dict["BIDS_tree_rawdata"])
        else:
            print("Path already exists. Overwrite = False")

        ### Cut / paste in the good location of our BIDS-like tree
        if not os.path.isfile(destination):
            shutil.move(renamed_filepath, destination)
        else:
            print("File already exists. Overwrite = False")

    return(destination)

def TRC_to_BIDSlike(current_path, path_info_dict, process = False):
    ### Rename all the channel names in the containing folder
    ext = ".TRC"
    root = os.path.split(current_path)[0]
    current_filename = os.path.split(current_path)[1]
    renamed_filename = path_info_dict["BIDS_full_name"] + ext
    renamed_filepath = os.path.join(root, renamed_filename)

    destination = os.path.join(path_info_dict["BIDS_tree_TRC"], renamed_filename)

    if process:
        ### Rename file
        os.rename(current_path,renamed_filepath)

        ### Create folder path
        if not os.path.exists(path_info_dict["BIDS_tree_TRC"]):
            os.makedirs(path_info_dict["BIDS_tree_TRC"])
        else:
            print("Path already exists. Overwrite = False")

        ### Cut / paste in the good location of our BIDS-like tree
        if not os.path.isfile(destination):
            shutil.move(renamed_filepath, destination)
        else:
            print("File already exists. Overwrite = False")

    return(destination)

if __name__ == "__main__":

    possible_tasknames = ["Stimic", "Imagery", "EPIFAR", "SAB", "Oddball"]

    ### Set parameters
    patient_num = 69
    sess_num = 1
    run_num = 1

    task_name = "Stimic"
    micro_identifier = "t"

    BIDSlike_folderpath = r"\\srv-data\public\Simona\Neuralynx_to_BIDSlike\srv-data-example\BIDS-like_Nlx"

    ### Process
    #- Get path info and define BIDS-like path
    path_info_dict = path_to_BIDSlikepath(patient_num, sess_num, run_num, BIDSlike_folderpath, task_name)

    #- From current .ncs structure to BIDS-like .ncs structure
    ncs_folderpath = r"\\srv-data\public\Simona\Neuralynx_to_BIDSlike\srv-data-example\donnees patients\69 JJ45\epifar jour 1"
    ncs_destination = ncs_to_BIDSlike(ncs_folderpath, path_info_dict, micro_identifier, process = True)

    #- From current .nrd structure to BIDS-like .nrd structure
    rawdata_filepath = r"\\srv-data\public\Simona\Neuralynx_to_BIDSlike\srv-data-example\donnees patients\69 JJ45\epifar j1.nrd"
    rawdata_destination = rawdata_to_BIDSlike(rawdata_filepath, path_info_dict, process = True)

    #- From current .TRC structure to BIDS-like .TRC structure
    TRC_filepath = r"\\srv-data\public\Simona\Neuralynx_to_BIDSlike\srv-data-example\donnees patients\69 JJ45\EPIFARjour1.TRC"
    TRC_destination = TRC_to_BIDSlike(TRC_filepath, path_info_dict, process = True)
