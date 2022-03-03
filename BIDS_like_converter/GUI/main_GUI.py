"""
Creation date: 2022, January 27
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""

import os
import sys
import json
import numpy as np
import traceback

from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QStyle, QErrorMessage,
    QTextEdit, QGridLayout, QApplication, QDialog, QPushButton,
    QVBoxLayout, QMainWindow, QMenu, QMessageBox, QSizePolicy,
    QComboBox, QHBoxLayout, QFrame, QCheckBox, QFileDialog, QTextBrowser)
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QIcon, QAction

from BIDS_like_converter.processing.create_BIDS_tree import (create_BIDS_name, ncs_to_BIDSlike, rawdata_to_BIDSlike, TRC_to_BIDSlike)
from BIDS_like_converter.config_file import (get_config, get_path)
from BIDS_like_converter.messageBox_popup import messageBox_popup

path_dict = get_path()

class BIDSlike_creator_win(QWidget):
    def __init__(self):
        super().__init__()

        self.init_GUI()
        self.show()


    def init_GUI(self):
        ### Def window size
        left = 200
        top = 100
        width = 700
        height = 700

        self.setGeometry(left, top, width, height)
        self.setWindowTitle('BIDS-like architecture creator')

        self.path_info_dict = {}

        ### BIDS naming frame
        BIDSnaming_frame = QFrame()
        BIDSnaming_layout = QHBoxLayout()
        BIDSnaming_frame.setLayout(BIDSnaming_layout)
        BIDSnaming_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        BIDSnaming_frame.setFixedHeight(30)
        BIDSnaming_layout.setContentsMargins(0, 0, 0, 0)
        BIDSnaming_layout.setSpacing(0)

        patient_label = QLabel("  Patient-")
        self.patient_edit = QLineEdit("")
        self.patient_edit.setText("000")

        sess_label = QLabel("  Session-")
        self.sess_edit = QLineEdit()
        self.sess_edit.setText("00")

        run_label = QLabel("  Run-")
        self.run_edit = QLineEdit()
        self.run_edit.setText("00")

        json_dict = get_config()
        possible_tasknames = json_dict["possible_tasknames"]
        possible_ext = json_dict["possible_ext"]
        possible_tasknames.append("Other")

        task_label = QLabel("  Task-")
        self.taskname_ComboBox = QComboBox()
        [self.taskname_ComboBox.addItem(taskname) for taskname in possible_tasknames]
        self.taskname_ComboBox.setCurrentIndex(0)
        self.taskname_ComboBox.currentIndexChanged.connect(self.taskname_ComboBox_fun)

        BIDSnaming_layout.addWidget(patient_label)
        BIDSnaming_layout.addWidget(self.patient_edit)
        BIDSnaming_layout.addWidget(sess_label)
        BIDSnaming_layout.addWidget(self.sess_edit)
        BIDSnaming_layout.addWidget(run_label)
        BIDSnaming_layout.addWidget(self.run_edit)
        BIDSnaming_layout.addWidget(task_label)
        BIDSnaming_layout.addWidget(self.taskname_ComboBox)

        ### Input data type frame
        input_format_frame = QFrame()
        input_format_layout = QHBoxLayout()
        input_format_frame.setLayout(input_format_layout)
        input_format_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_format_frame.setFixedHeight(50)
        input_format_layout.setContentsMargins(0, 0, 0, 0)
        input_format_layout.setSpacing(0)

        ##- Input data type subframe 1
        input_format_subframe1 = QFrame()
        input_format_sublayout1 = QHBoxLayout()
        input_format_subframe1.setLayout(input_format_sublayout1)
        input_format_subframe1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_format_subframe1.setFixedHeight(30)
        input_format_sublayout1.setContentsMargins(0, 0, 0, 0)
        input_format_sublayout1.setSpacing(0)

        input_format_label = QLabel("Input format: ")
        self.ext_ComboBox = QComboBox()
        [self.ext_ComboBox.addItem(ext) for ext in possible_ext]
        self.ext_ComboBox.setCurrentIndex(0)
        self.ext_ComboBox.currentIndexChanged.connect(self.ext_ComboBox_fun)
        self.ext_ComboBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        input_format_sublayout1.addWidget(input_format_label)
        input_format_sublayout1.addWidget(self.ext_ComboBox)

        ##- Input data type subframe 2
        input_format_subframe2 = QFrame()
        input_format_sublayout2 = QHBoxLayout()
        input_format_subframe2.setLayout(input_format_sublayout2)
        input_format_subframe2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_format_subframe2.setFixedHeight(30)
        input_format_sublayout2.setContentsMargins(0, 0, 0, 0)
        input_format_sublayout2.setSpacing(0)

        microID_label = QLabel("                micro ID: ")
        self.microID_edit = QLineEdit("")
        self.microID_edit.setText("t")
        self.microID_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        microID_infoButton = QPushButton("")
        microID_infoButton.clicked.connect(self.microID_infoButton_fun)
        microID_infoButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        microID_infoButton.setFixedWidth(50)
        microID_infoButton.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-info-squared-96.png")))

        input_format_sublayout2.addWidget(microID_label)
        input_format_sublayout2.addWidget(self.microID_edit)
        input_format_sublayout2.addWidget(microID_infoButton)

        input_format_layout.addWidget(input_format_subframe1)
        input_format_layout.addWidget(input_format_subframe2)

        ### Input data path frame
        input_path_frame = QFrame()
        input_path_layout = QHBoxLayout()
        input_path_frame.setLayout(input_path_layout)
        input_path_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_path_frame.setFixedHeight(30)
        input_path_layout.setContentsMargins(0, 0, 0, 0)
        input_path_layout.setSpacing(0)

        input_infoButton = QPushButton("")
        input_infoButton.clicked.connect(self.input_infoButton_fun)
        input_infoButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_infoButton.setFixedWidth(50)
        input_infoButton.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-info-squared-96.png")))

        input_browseButton = QPushButton("Browse...")
        input_browseButton.clicked.connect(self.input_browseButton_fun)
        input_browseButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        input_browseButton.setFixedWidth(100)

        self.input_path_edit = QLineEdit()
        self.input_path_edit.setText("")
        self.input_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.input_ext_edit = QLabel() #QLineEdit()
        self.input_ext_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.input_ext_edit.setText(self.ext_ComboBox.currentText())
        self.input_ext_edit.setFixedWidth(50)
        #self.input_ext_edit.setStyleSheet("background-color: lightgray")
        self.input_ext_edit.setStyleSheet("background: #636363 ;color: #ffffff;border: 2px solid #1f48cf;")

        input_path_layout.addWidget(input_infoButton)
        input_path_layout.addWidget(input_browseButton)
        input_path_layout.addWidget(self.input_path_edit)
        input_path_layout.addWidget(self.input_ext_edit)

        ### Output data path frame
        output_path_frame = QFrame()
        output_path_layout = QHBoxLayout()
        output_path_frame.setLayout(output_path_layout)
        output_path_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        output_path_frame.setFixedHeight(30)
        output_path_layout.setContentsMargins(0, 0, 0, 0)
        output_path_layout.setSpacing(0)

        output_infoButton = QPushButton("")
        output_infoButton.clicked.connect(self.output_infoButton_fun)
        output_infoButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        output_infoButton.setFixedWidth(50)
        output_infoButton.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-info-squared-96.png")))

        output_browseButton = QPushButton("Browse...")
        output_browseButton.clicked.connect(self.output_browseButton_fun)
        output_browseButton.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        output_browseButton.setFixedWidth(100)

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText("")
        self.output_path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.output_folder_edit = QLabel() #QLineEdit()
        self.output_folder_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.output_folder_edit.setText("")
        self.output_folder_edit.setFixedWidth(150)
        self.output_folder_edit.setStyleSheet("background: #636363 ;color: #ffffff;border: 2px solid #1f48cf;")

        output_path_layout.addWidget(output_infoButton)
        output_path_layout.addWidget(output_browseButton)
        output_path_layout.addWidget(self.output_path_edit)
        output_path_layout.addWidget(self.output_folder_edit)

        ### Validation Frame
        self.description_textbox = QTextBrowser(self)
        self.description_textbox.setObjectName("description_textbox")
        self.description_textbox.setStyleSheet("QTextBrowser#description_textbox {background: white ;border: 2px solid #000000;}")
        self.description_textbox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        validation_frame = QFrame()
        validation_layout = QVBoxLayout()
        validation_frame.setLayout(validation_layout)
        validation_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        button_check = QPushButton("Check information before final validation")
        button_check.setShortcut("Return")
        button_check.clicked.connect(self.button_check_fun)
        button_check.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button_check.setFixedHeight(30)

        button_OK = QPushButton("OK")
        button_OK.clicked.connect(self.button_OK_fun)
        button_OK.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button_OK.setFixedHeight(30)
        button_OK.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-data-quality-96.png")))

        validation_layout.addWidget(self.description_textbox)
        validation_layout.addWidget(button_check)
        validation_layout.addWidget(button_OK)

        # Set global layout
        title1 = QLabel("DATA STRUCTURE")
        title1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title1.setStyleSheet("background: #636363 ;border: 2px solid #000000;font-weight: bold;font-size: 18pt;color: #ffffff;")

        title2 = QLabel("DATA PATH")
        title2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title2.setStyleSheet("background: #636363 ;border: 2px solid #000000;font-weight: bold;font-size: 18pt;color: #ffffff;")

        GLOBAL_layout = QVBoxLayout(self)

        GLOBAL_layout.addWidget(title1)
        GLOBAL_layout.addWidget(BIDSnaming_frame)
        GLOBAL_layout.addWidget(input_format_frame)
        GLOBAL_layout.addWidget(title2)
        GLOBAL_layout.addWidget(input_path_frame)
        GLOBAL_layout.addWidget(output_path_frame)
        GLOBAL_layout.addWidget(validation_frame)

    def taskname_ComboBox_fun(self):
        if self.taskname_ComboBox.currentText() == "Other":
            error_dialog.setWindowTitle("Information")
            error_dialog = QErrorMessage()
            error_dialog.showMessage('If you want to add a new task name, you need to add it in the "task_names.json" file, which you can find in the root folder of this program.')
            error_dialog.exec()

    def ext_ComboBox_fun(self, callback):
        self.input_path_edit.setText("")
        self.input_ext_edit.setText(self.ext_ComboBox.currentText())

    def microID_infoButton_fun(self):
        microID_infoButton_dialog = QErrorMessage()
        microID_infoButton_dialog.setWindowTitle("Information about the 'micro ID' parameter")
        microID_infoButton_dialog.showMessage('This parameter is only necessary if the dataset include micro-electrodes. If that is the case, enter the letter(s) used to differenciate micro-channels from macro-channels.')
        microID_infoButton_dialog.exec()

    def input_infoButton_fun(self):
        input_infoButton_dialog = QErrorMessage()
        input_infoButton_dialog.setWindowTitle("Input path information")
        input_infoButton_dialog.showMessage('Search or paste the path to the data you want to turn into a BIDS-like. For .ncs choose the folder, for .trc and .nrd choose the file.')
        input_infoButton_dialog.exec()

    def input_browseButton_fun(self):
        selected_path = ""
        if ".nrd" in self.ext_ComboBox.currentText().lower() or ".trc" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getOpenFileName(self, self.tr("Select an EEG file"), '~', self.tr("EEG files (*.trc *.nrd)"))[0]
        elif ".ncs" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getExistingDirectory(self, 'Select a Neuralynx EEG folder', '~')

        if selected_path:
            self.input_path_edit.setText(selected_path)
            self.description_textbox.append("")
            self.description_textbox.append(f"Input data --------------------------> {os.path.split(selected_path)[-1]}")

    def output_infoButton_fun(self):
        output_infoButton_dialog = QErrorMessage()
        output_infoButton_dialog.setWindowTitle("Output path information")
        output_infoButton_dialog.showMessage('Search or paste the path to your BIDS-like folder.')
        output_infoButton_dialog.exec()

    def output_browseButton_fun(self):
        selected_path = ""
        selected_path = QFileDialog.getExistingDirectory(self, 'Select your BIDS-like root folder', '~')
        self.output_path_edit.setText(selected_path)

        if selected_path:
            self.output_folder_edit.setText(os.path.split(selected_path)[-1])
            self.description_textbox.append("")
            self.description_textbox.append(f"Output (BIDS-like root) folder ---> {os.path.split(selected_path)[-1]}")

    def button_check_fun(self):
        self.display_error_pathExists = False
        self.display_error_noTsvMatchingFile = False
        self.destination = ""

        ### Get ext
        ext = self.input_ext_edit.text().replace(".","")

        ### Get BIDS like folder path and file names
        self.path_info_dict = create_BIDS_name(int(self.patient_edit.text()), int(self.sess_edit.text()), int(self.run_edit.text()), self.output_path_edit.text(), self.taskname_ComboBox.currentText())

        ### Split path
        path_components = []
        path = self.path_info_dict[f"BIDS_tree_{ext.lower()}"]
        path = os.path.normpath(path)
        path = path.split(os.sep)
        [path_components.append(_comp) for _comp in path if _comp]
        path_components.append(self.path_info_dict["BIDS_full_name"])

        ### Display channels name and recording scale
        if ".ncs" in self.ext_ComboBox.currentText().lower():
            ncs_renamed_list, self.destination, is_tsv_matching_file = ncs_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed = False)

            self.description_textbox.append("\n#---------------------------\n# macro-EEG channels:\n#---------------------------")
            [self.description_textbox.append("# {}".format(chan_name.replace("macro",""))) for chan_name in ncs_renamed_list if "macro" in chan_name]

            self.description_textbox.append("\n#---------------------------\n# micro-EEG channels:\n#---------------------------")
            [self.description_textbox.append("# {}".format(chan_name.replace("micro",""))) for chan_name in ncs_renamed_list if "micro" in chan_name]

            if os.path.exists(self.destination): self.display_error_pathExists = True
            if not is_tsv_matching_file : self.display_error_noTsvMatchingFile = True

        ### Set display_error_pathExists if path already exists. Will be displayed to the user later.
        elif ".nrd" in self.ext_ComboBox.currentText().lower():
            self.destination = nrd_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed = False)
            if os.path.isfile(self.destination): self.display_error_pathExists = True
        elif ".trc" in self.ext_ComboBox.currentText().lower():
            self.destination = trc_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed = False)
            if os.path.isfile(self.destination): self.display_error_pathExists = True

        ### Display BIDS path tree
        self.description_textbox.append("")
        self.description_textbox.append("Original path:")
        self.description_textbox.append(self.input_path_edit.text())
        self.description_textbox.append("")
        self.description_textbox.append("BIDS-like root (destination):")
        self.description_textbox.append(self.output_path_edit.text())

        self.description_textbox.append("")
        self.description_textbox.append("BIDS-like tree:")
        tree_level = 1
        for _comp in path_components:
            self.description_textbox.append("{} {}".format( "_"*tree_level,_comp ))
            tree_level+=2

        ### Check if path exists
        if self.display_error_pathExists:
            text = "This destination folder/file path already exists: \n\n<< {} >>\n\n Nothing will happen (overwrite = False).".format(self.destination.replace("\\","/"))
            messageBox_popup("Warning [1]", text, QMessageBox.Critical, cancel_option = False) #QMessageBox.Warning

        if self.display_error_noTsvMatchingFile:
            text = "The << Electrodes names and scales matching.tsv >> file that should be inside the Neuralynx ncs folder is missing. See example dataset provided with this program for more information."
            messageBox_popup("tsv matching file not found", text, QMessageBox.Critical, cancel_option = False) #QMessageBox.Warning

    def button_OK_fun(self):

        self.button_check_fun()

        if not self.display_error_pathExists and not self.display_error_noTsvMatchingFile:
            _dest = self.destination.replace("\\","/")
            _BIDSname_text = f"#------------------------------------------------\n# {os.path.split(_dest)[-1]}\n#------------------------------------------------"
            text = f"{_BIDSname_text} \n\nFormat: {self.ext_ComboBox.currentText().lower()} \n\nOrigin: {self.input_path_edit.text()} \n\nDestination: {_dest} \n\nThis action is definitive. If you cancel, nothing will happen."
            returnValue = messageBox_popup("Please confirm", text, QMessageBox.Icon.Question, cancel_option = True)

            if returnValue == QMessageBox.StandardButton.Ok:
                self.proceed_BIDSlike_architecture()
            else:
                returnValue = messageBox_popup("Aborted", "Procedure aborted. Nothing will happen.", QMessageBox.Icon.Information, cancel_option = False)
        else:
            if self.display_error_pathExists:
                text = "This destination folder/file path already exists: \n\n<< {} >>\n\n Nothing will happen (overwrite = False).".format(self.destination.replace("\\","/"))
                messageBox_popup("Warning [2]", text, QMessageBox.Critical, cancel_option = False) #QMessageBox.Warning
            elif self.display_error_noTsvMatchingFile:
                text = "The << Electrodes names and scales matching.tsv >> file that should be inside the Neuralynx ncs folder is missing. See example dataset provided with this program for more information."
                messageBox_popup("tsv matching file not found", text, QMessageBox.Critical, cancel_option = False) #QMessageBox.Warning

    def displayConfirm_and_resetInputPath(self):
            returnValue = messageBox_popup("Done", "Done! BIDS-like architecture created.", QMessageBox.Icon.Information, cancel_option = False)
            self.input_path_edit.setText("")

    def proceed_BIDSlike_architecture(self):
        self.description_textbox.append("")

        try:
            if ".ncs" in self.ext_ComboBox.currentText().lower():
                ncs_renamed_list, destination, is_tsv_matching_file = ncs_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed = True)
                self.description_textbox.append("\nNeuralynx [ncs] data proceeded. Data were sent to destination path.")
            elif ".nrd" in self.ext_ComboBox.currentText().lower():
                destination = rawdata_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed = True)
                self.description_textbox.append("\nNeuralynx [nrd] data processed. Data were sent to destination path.")
            elif ".trc" in self.ext_ComboBox.currentText().lower():
                destination = TRC_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed = True)
                self.description_textbox.append("\nNeuralynx [trc] data processed. Data were sent to destination path.")

            self.displayConfirm_and_resetInputPath()

        except:
            var = traceback.format_exc()
            self.description_textbox.append(var)
