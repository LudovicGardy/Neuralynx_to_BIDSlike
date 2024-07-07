"""
Creation date: 2022, January 30
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""

import json
import os
import numpy as np
import pandas as pd

### When * is used, the following functions will be imported
__all__ = [
    'create_dataset_description_json', 
    'create_participants_json', 
    'create_info_json', 
    'create_participants_tsv', 
    'create_session_tsv', 
    'create_scans_tsv', 
    'create_channels_tsv', 
    'create_events_tsv'
]

### Create json files
def create_dataset_description_json(BIDS_root_path, write = False):
    '''
    ----------------------------------
    dest: BIDS_root
    ex: dataset_description.json
    ----------------------------------

    {
        "Name": " ",
        "BIDSVersion": "1.2.0"
    }
    '''

    dataset_description_json = {

        "Name": np.nan,
        "BIDSVersion": ""
    }

    output_filepath = os.path.join(BIDS_root_path, "dataset_description.json")

    if write and not os.path.isfile(output_filepath):
        json_output = json.dumps(dataset_description_json, indent=4)
        with open(output_filepath, 'w') as fid:
            fid.write(json_output)
            fid.write('\n')
    else:
        print("This path already exists. Nothing will happen (overwrite = False).")

    return(dataset_description_json, output_filepath)

def create_participants_json(BIDS_root_path, write = False):
    '''
    ----------------------------------
    dest: BIDS_root
    ex: participants.json
    ----------------------------------

    {
        "participant_id": {
            "Description": "Unique participant identifier"
        },
        "age": {
            "Description": "Age of the participant at time of testing",
            "Units": "years"
        },
        "sex": {
            "Description": "Biological sex of the participant",
            "Levels": {
                "F": "female",
                "M": "male"
            }
        }
    }
    '''

    participants_json = {
        "participant_id": {
            "Description": "Unique participant identifier"
        },
        "age": {
            "Description": "Age of the participant at time of testing",
            "Units": "years"
        },
        "sex": {
            "Description": "Biological sex of the participant",
            "Levels": {
                "F": "female",
                "M": "male"
            }
        }
    }

    output_filepath = os.path.join(BIDS_root_path, "participants.json")

    if write and not os.path.isfile(output_filepath):
        json_output = json.dumps(participants_json, indent=4)
        with open(output_filepath, 'w') as fid:
            fid.write(json_output)
            fid.write('\n')
    else:
        print("This path already exists. Nothing will happen (overwrite = False).")

    return(participants_json, output_filepath)

def create_info_json(json_level5_path, foldername_level4, format, write = False, **kwargs):
    '''
    ---------------------------------------------------------------
    dest: BIDS_root/sub-xxx/sess-xx/ieeg
    ex: sub-001_ses-Micro5khz01_task-EPIFAR_run-01_ieeg.json
    ---------------------------------------------------------------

    {
        "TaskName": "EPIFAR",
        "Manufacturer": "Blackrock",
        "PowerLineFrequency": 50,
        "SamplingFrequency": 5000.0,
        "SoftwareFilters": "n/a",
        "RecordingDuration": 600.9998,
        "RecordingType": "continuous",
        "EEGReference": "n/a",
        "EEGGround": "n/a",
        "EEGPlacementScheme": "n/a",
        "EEGChannelCount": 41,
        "EOGChannelCount": 0,
        "ECGChannelCount": 0,
        "EMGChannelCount": 0,
        "MiscChannelCount": 0,
        "TriggerChannelCount": 0
    }
    '''

    if "ncs" in format or "nrd" in format:
        manufacturer = "Neuralynx"

    info_json = {
        "TaskName": manufacturer,
        "Manufacturer": "",
        "PowerLineFrequency": np.nan,
        "SamplingFrequency": np.nan,
        "SoftwareFilters": "n/a",
        "RecordingDuration": np.nan,
        "RecordingType": "continuous",
        "EEGReference": "n/a",
        "EEGGround": "n/a",
        "EEGPlacementScheme": "n/a",
        "EEGChannelCount": np.nan,
        "EOGChannelCount": np.nan,
        "ECGChannelCount": np.nan,
        "EMGChannelCount": np.nan,
        "MiscChannelCount": np.nan,
        "TriggerChannelCount": np.nan
    }

    output_filepath = os.path.join(json_level5_path, f"{foldername_level4}.json")
    if write and not os.path.isfile(output_filepath):
        json_output = json.dumps(info_json, indent=4)
        with open(output_filepath, 'w') as fid:
            fid.write(json_output)
            fid.write('\n')
    else:
        print("This path already exists. Nothing will happen (overwrite = False).")

    return(info_json)

### Create tsv files
def create_participants_tsv(BIDS_root_path, BIDS_root_listdir, write = False):
    '''
    ----------------------------------
    dest: BIDS_root
    ex: participants.tsv
    ----------------------------------

    participant_id	age	sex
    sub-001	n/a	n/a
    sub-002	n/a	n/a
    sub-003	n/a	n/a
    sub-004	n/a	n/a
    sub-005	n/a	n/a
    sub-006	n/a	n/a
    sub-007	n/a	n/a
    sub-008	n/a	n/a
    sub-009	n/a	n/a
    sub-010	n/a	n/a
    sub-011	n/a	n/a
    sub-012	n/a	n/a
    sub-013	n/a	n/a
    '''

    participants_dict = {"participant_id": [], "age": [], "sex": []}

    for foldername in BIDS_root_listdir:
        if "sub" in foldername:
            participants_dict["participant_id"].append(foldername)
            participants_dict["age"].append("n/a")
            participants_dict["sex"].append("n/a")

    output_filepath = os.path.join(BIDS_root_path, "participants.tsv")
    if write and not os.path.isfile(output_filepath):
        df = pd.DataFrame.from_dict(participants_dict)
        df.to_csv(output_filepath, sep="\t", index = False)
    else:
        print("This path already exists. Nothing will happen (overwrite = False).")

    return(participants_dict, output_filepath)

def create_session_tsv(BIDS_root_path, BIDS_root_listdir, write = False):
    '''
    --------------------------
    dest: BIDS_root/sub-xxx
    ex: sub-xxx_sessions.tsv
    --------------------------

    session_id	acq_time	Comment
    mri	2017-08-10	N/A
    MacroBipolar01	N/A	N/A
    MacroBipolar02	N/A	N/A
    MacroBipolar03	N/A	N/A
    MacroBipolar04	N/A	N/A
    MacroBipolar05	N/A	N/A
    Micro5khz01	N/A	N/A
    Micro5khz02	N/A	N/A
    Micro5khz03	N/A	N/A
    Micro5khz04	N/A	N/A
    Micro5khz05	N/A	N/A
    '''

    print("")
    for foldername_root in BIDS_root_listdir:
        print("a-- ", BIDS_root_listdir)
        print("b-- ", foldername_root)
        if "sub" in foldername_root:
            print("c-- ", foldername_root)
            session_dict = {"session_id": [], "acq_time": [], "Comment": []}
            json_level2_path = os.path.join(BIDS_root_path,foldername_root)
            print("d-- ", json_level2_path)
            BIDS_level2_listdir = next(os.walk(json_level2_path))[1]
            print("e-- ", BIDS_level2_listdir)
            for foldername_level2 in BIDS_level2_listdir:
                if "ses" in foldername_level2:
                    print("f-- ", foldername_level2)
                    session_dict["session_id"].append(foldername_level2)
                    session_dict["acq_time"].append("n/a")
                    session_dict["Comment"].append("n/a")

            output_filepath = os.path.join(json_level2_path, f"{foldername_root}_sessions.tsv")
            if write and not os.path.isfile(output_filepath):
                df = pd.DataFrame.from_dict(session_dict)
                df.to_csv(output_filepath, sep="\t", index = False)
            else:
                print("This path already exists. Nothing will happen (overwrite = False).")

    return(session_dict)


def create_scans_tsv(BIDS_root_path, BIDS_root_listdir, write = False):
    '''
    ---------------------------------
    dest: BIDS_root/sub-xxx/sess-xx
    ex: sub-xxx_ses-xx_scans.tsv
    ---------------------------------

    filename	acq_time
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-01_ieeg.edf	2018-01-30T13:19:47
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-02_ieeg.edf	2018-01-30T13:21:52
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-03_ieeg.edf	2018-01-30T13:23:47
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-04_ieeg.edf	2018-01-30T13:25:41
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-05_ieeg.edf	2018-01-30T13:27:34
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-06_ieeg.edf	2018-01-30T13:29:27
    ieeg/sub-018_ses-Micro5khz01_task-EPIFAR_run-07_ieeg.edf	2018-01-30T13:30:09
    '''

    print("")
    for foldername_root in BIDS_root_listdir:
        print("a-- ", BIDS_root_listdir)
        print("b-- ", foldername_root)
        if "sub" in foldername_root:
            print("c-- ", foldername_root)
            session_dict = {"session_id": [], "acq_time": [], "Comment": []}
            json_level2_path = os.path.join(BIDS_root_path,foldername_root)
            print("d-- ", json_level2_path)
            BIDS_level2_listdir = next(os.walk(json_level2_path))[1]
            print("e-- ", BIDS_level2_listdir)
            for foldername_level2 in BIDS_level2_listdir:
                if "ses" in foldername_level2:
                    json_level3_path = os.path.join(BIDS_root_path,foldername_root,foldername_level2)
                    json_level4_path = os.path.join(BIDS_root_path,foldername_root,foldername_level2,"ieeg")
                    print("f-- ", foldername_level2)
                    BIDS_level4_listdir = next(os.walk(json_level4_path))[1] # Change to [2] for trc/nrd/edf... (files not folders contrary to ncs)
                    scans_dict = {"filename": [], "acq_time": []}
                    for foldername_level4 in BIDS_level4_listdir:
                        print("g-- ", foldername_level4)
                        scans_dict["filename"].append(foldername_level4)
                        scans_dict["acq_time"].append("n/a")

                    output_filepath = os.path.join(json_level3_path, f"{foldername_root}_{foldername_level2}_scans.tsv")
                    if write and not os.path.isfile(output_filepath):
                        df = pd.DataFrame.from_dict(scans_dict)
                        df.to_csv(output_filepath, sep="\t", index = False)
                    else:
                        print("This path already exists. Nothing will happen (overwrite = False).")

    return(scans_dict)

def create_channels_tsv(BIDS_root_path, BIDS_root_listdir, write = False):
    '''
    -------------------------------------------------------------
    dest: BIDS_root/sub-xxx/sess-xx/ieeg
    ex: sub-001_ses-Micro5khz05_task-EPIFAR_run-01_channels.tsv
    -------------------------------------------------------------

    name	type	units	low_cutoff	high_cutoff	description	sampling_frequency	status
    EEG a1	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a2	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a3	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a4	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a5	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a6	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a7	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a8	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a9	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a10	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    EEG a11	EEG	µV	0.0	2500.0	ElectroEncephaloGram	5000.0	good
    '''

    print("")
    for foldername_root in BIDS_root_listdir:
        print("a-- ", BIDS_root_listdir)
        print("b-- ", foldername_root)
        if "sub" in foldername_root:
            print("c-- ", foldername_root)
            session_dict = {"session_id": [], "acq_time": [], "Comment": []}
            json_level2_path = os.path.join(BIDS_root_path,foldername_root)
            print("d-- ", json_level2_path)
            BIDS_level2_listdir = next(os.walk(json_level2_path))[1]
            print("e-- ", BIDS_level2_listdir)
            for foldername_level2 in BIDS_level2_listdir:
                if "ses" in foldername_level2:
                    json_level3_path = os.path.join(BIDS_root_path,foldername_root,foldername_level2)
                    json_level4_path = os.path.join(BIDS_root_path,foldername_root,foldername_level2,"ieeg")
                    print("f-- ", foldername_level2)
                    BIDS_level4_listdir = next(os.walk(json_level4_path))[1] # Change to [2] for trc/nrd/edf... (files not folders contrary to ncs)
                    scans_dict = {"filename": [], "acq_time": []}
                    for foldername_level4 in BIDS_level4_listdir:
                        print("g-- ", foldername_level4)
                        channels_dict = {"name": [],	"type": [],	"units": [], "low_cutoff": [], "high_cutoff": [], "description": [], "sampling_frequency": [], "status": []}
                        scans_dict["filename"].append(foldername_level4)
                        scans_dict["acq_time"].append("n/a")
                        json_level5_path = os.path.join(BIDS_root_path,foldername_root,foldername_level2,"ieeg",foldername_level4)
                        BIDS_level5_listdir = next(os.walk(json_level5_path))[2]
                        BIDS_level5_listchans = []
                        print("h-- ", BIDS_level5_listdir)
                        [BIDS_level5_listchans.append(filename.replace(".ncs","")) for filename in  BIDS_level5_listdir if ".ncs" in filename]
                        print("i-- ", BIDS_level5_listchans)
                        for chan_name in BIDS_level5_listchans:
                            channels_dict["name"].append(chan_name)
                            channels_dict["type"].append("n/a")
                            channels_dict["units"].append("n/a")
                            channels_dict["low_cutoff"].append("n/a")
                            channels_dict["high_cutoff"].append("n/a")
                            channels_dict["description"].append("n/a")
                            channels_dict["sampling_frequency"].append("n/a")
                            channels_dict["status"].append("n/a")

                        output_filepath = os.path.join(json_level5_path, f"{foldername_level4}.tsv")
                        if write and not os.path.isfile(output_filepath):
                            df = pd.DataFrame.from_dict(channels_dict)
                            df.to_csv(output_filepath, sep="\t", index = False)
                        else:
                            print("This path already exists. Nothing will happen (overwrite = False).")

    return(json_level5_path, foldername_level4, channels_dict)


def create_events_tsv():
    pass # To develop
