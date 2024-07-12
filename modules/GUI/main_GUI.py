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

from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QErrorMessage,
                             QPushButton, QVBoxLayout, QMessageBox, QSizePolicy,
                             QComboBox, QHBoxLayout, QFrame, QFileDialog, QTextBrowser)
from PyQt6 import QtCore, QtGui

from modules.processing.create_BIDS_tree import (create_BIDS_name, ncs_to_BIDSlike, rawdata_to_BIDSlike, TRC_to_BIDSlike)
from modules.config_file import get_config, get_path
from modules.messageBox_popup import messageBox_popup

path_dict = get_path()


class BIDSlikeCreatorWin(QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()
        self.show()

    def init_GUI(self):
        self.setGeometry(200, 100, 700, 700)
        self.setWindowTitle('BIDS-like architecture creator')

        self.path_info_dict = {}
        
        json_dict = get_config()
        possible_tasknames = json_dict["possible_tasknames"] + ["Other"]
        possible_ext = json_dict["possible_ext"]
        self.input_ext_edit = QLabel()
        self.output_folder_edit = QLabel()

        layout = QVBoxLayout(self)
        layout.addWidget(self.create_title("DATA STRUCTURE"))
        layout.addWidget(self.create_bids_naming_frame(possible_tasknames))
        layout.addWidget(self.create_input_format_frame(possible_ext))
        layout.addWidget(self.create_title("DATA PATH"))
        layout.addWidget(self.create_path_frame("Input", self.input_infoButton_fun, self.input_browseButton_fun, self.input_ext_edit))
        layout.addWidget(self.create_path_frame("Output", self.output_infoButton_fun, self.output_browseButton_fun, self.output_folder_edit))
        layout.addWidget(self.create_validation_frame())

    def create_title(self, text):
        title = QLabel(text)
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("background: #636363 ;border: 2px solid #000000;font-weight: bold;font-size: 18pt;color: #ffffff;")
        return title

    def create_bids_naming_frame(self, tasknames):
        frame = self.create_frame(30)
        layout = frame.layout()
        layout.addWidget(QLabel("  Patient-"))
        self.patient_edit = self.create_line_edit("000")
        layout.addWidget(self.patient_edit)
        layout.addWidget(QLabel("  Session-"))
        self.sess_edit = self.create_line_edit("00")
        layout.addWidget(self.sess_edit)
        layout.addWidget(QLabel("  Run-"))
        self.run_edit = self.create_line_edit("00")
        layout.addWidget(self.run_edit)
        layout.addWidget(QLabel("  Task-"))
        self.taskname_ComboBox = QComboBox()
        self.taskname_ComboBox.addItems(tasknames)
        self.taskname_ComboBox.currentIndexChanged.connect(self.taskname_ComboBox_fun)
        layout.addWidget(self.taskname_ComboBox)
        return frame

    def create_input_format_frame(self, extensions):
        frame = self.create_frame(50)
        layout = frame.layout()
        layout.addWidget(self.create_input_format_subframe1(extensions))
        layout.addWidget(self.create_input_format_subframe2())
        return frame

    def create_input_format_subframe1(self, extensions):
        frame = self.create_frame(30)
        layout = frame.layout()
        layout.addWidget(QLabel("Input format: "))
        self.ext_ComboBox = QComboBox()
        self.ext_ComboBox.addItems(extensions)
        self.ext_ComboBox.currentIndexChanged.connect(self.ext_ComboBox_fun)
        # self.ext_ComboBox.setCurrentIndex(0)
        layout.addWidget(self.ext_ComboBox)
        return frame

    def create_input_format_subframe2(self):
        frame = self.create_frame(30)
        layout = frame.layout()
        layout.addWidget(QLabel("                micro ID: "))
        self.microID_edit = self.create_line_edit("t")
        layout.addWidget(self.microID_edit)
        microID_infoButton = self.create_info_button(self.microID_infoButton_fun)
        layout.addWidget(microID_infoButton)
        return frame

    def create_path_frame(self, label, info_fun, browse_fun, ext_widget):
        frame = self.create_frame(30)
        layout = frame.layout()
        infoButton = self.create_info_button(info_fun)
        layout.addWidget(infoButton)
        browseButton = QPushButton("Browse...")
        browseButton.clicked.connect(browse_fun)
        browseButton.setFixedWidth(100)
        layout.addWidget(browseButton)
        path_edit = QLineEdit()
        path_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(path_edit)
        ext_widget = QLabel()
        ext_widget.setStyleSheet("background: #636363 ;color: #ffffff;border: 2px solid #1f48cf;")
        ext_widget.setFixedWidth(50)
        layout.addWidget(ext_widget)
        if label == "Input":
            self.input_path_edit = path_edit
            self.input_ext_edit = ext_widget
        else:
            self.output_path_edit = path_edit
            self.output_folder_edit = ext_widget
        return frame

    def create_validation_frame(self):
        frame = self.create_frame()
        layout = frame.layout()
        self.description_textbox = QTextBrowser(self)
        self.description_textbox.setObjectName("description_textbox")
        self.description_textbox.setStyleSheet("QTextBrowser#description_textbox {background: white ;border: 2px solid #000000;}")
        layout.addWidget(self.description_textbox)
        button_check = QPushButton("Check information before final validation")
        button_check.setShortcut("Return")
        button_check.clicked.connect(self.button_check_fun)
        button_check.setFixedHeight(30)
        layout.addWidget(button_check)
        button_OK = QPushButton("OK")
        button_OK.clicked.connect(self.button_OK_fun)
        button_OK.setFixedHeight(30)
        button_OK.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-data-quality-96.png")))
        layout.addWidget(button_OK)
        return frame

    def create_frame(self, height=0):
        frame = QFrame()
        layout = QHBoxLayout() if height else QVBoxLayout()
        frame.setLayout(layout)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        if height:
            frame.setFixedHeight(height)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
        return frame

    def create_line_edit(self, text):
        edit = QLineEdit(text)
        edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return edit

    def create_info_button(self, func):
        button = QPushButton("")
        button.clicked.connect(func)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.setFixedWidth(50)
        button.setIcon(QtGui.QIcon(os.path.join(path_dict["icon_path"], "icons8-info-squared-96.png")))
        return button

    def taskname_ComboBox_fun(self):
        if self.taskname_ComboBox.currentText() == "Other":
            error_dialog = QErrorMessage(self)
            error_dialog.setWindowTitle("Information")
            error_dialog.showMessage('If you want to add a new task name, you need to add it in the "task_names.json" file, which you can find in the root folder of this program.')
            error_dialog.exec()

    def ext_ComboBox_fun(self, callback):
        self.input_path_edit.setText("")
        self.input_ext_edit.setText(self.ext_ComboBox.currentText())

    def microID_infoButton_fun(self):
        self.show_error_message("Information about the 'micro ID' parameter", 
            "This parameter is only necessary if the dataset include micro-electrodes. "
            "If that is the case, enter the letter(s) used to differentiate micro-channels from macro-channels.")

    def input_infoButton_fun(self):
        self.show_error_message("Input path information", 
            "Search or paste the path to the data you want to turn into a BIDS-like. "
            "For .ncs choose the folder, for .trc and .nrd choose the file.")

    def input_browseButton_fun(self):
        selected_path = ""
        if ".nrd" in self.ext_ComboBox.currentText().lower() or ".trc" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getOpenFileName(self, "Select an EEG file", '~', "EEG files (*.trc *.nrd)")[0]
        elif ".ncs" in self.ext_ComboBox.currentText().lower():
            selected_path = QFileDialog.getExistingDirectory(self, "Select a Neuralynx EEG folder", '~')

        if selected_path:
            self.input_path_edit.setText(selected_path)
            self.description_textbox.append(f"\nInput data --------------------------> {os.path.split(selected_path)[-1]}")

    def output_infoButton_fun(self):
        self.show_error_message("Output path information", 
            "Search or paste the path to your BIDS-like folder.")

    def output_browseButton_fun(self):
        selected_path = QFileDialog.getExistingDirectory(self, "Select your BIDS-like root folder", '~')
        if selected_path:
            self.output_path_edit.setText(selected_path)
            self.output_folder_edit.setText(os.path.split(selected_path)[-1])
            self.description_textbox.append(f"\nOutput (BIDS-like root) folder ---> {os.path.split(selected_path)[-1]}")

    def button_check_fun(self):
        self.display_error_pathExists = False
        self.display_error_noTsvMatchingFile = False
        self.destination = ""

        ext = self.input_ext_edit.text().replace(".", "")
        self.path_info_dict = create_BIDS_name(int(self.patient_edit.text()), int(self.sess_edit.text()), int(self.run_edit.text()), self.output_path_edit.text(), self.taskname_ComboBox.currentText())
        path_components = self.split_path(self.path_info_dict[f"BIDS_tree_{ext.lower()}"])

        if ".ncs" in self.ext_ComboBox.currentText().lower():
            ncs_renamed_list, self.destination, is_tsv_matching_file = ncs_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed=False)
            self.display_channels("macro-EEG", ncs_renamed_list, "macro")
            self.display_channels("micro-EEG", ncs_renamed_list, "micro")
            self.display_error_pathExists = os.path.exists(self.destination)
            self.display_error_noTsvMatchingFile = not is_tsv_matching_file

        elif ".nrd" in self.ext_ComboBox.currentText().lower():
            self.destination = rawdata_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed=False)
            self.display_error_pathExists = os.path.isfile(self.destination)

        elif ".trc" in self.ext_ComboBox.currentText().lower():
            self.destination = TRC_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed=False)
            self.display_error_pathExists = os.path.isfile(self.destination)

        self.display_bids_path_tree(path_components)

        if self.display_error_pathExists:
            self.show_warning("Warning [1]", f"This destination folder/file path already exists: \n\n<< {os.path.normpath(self.destination).replace(os.sep, '/')} >>\n\n Nothing will happen (overwrite = False).")

        if self.display_error_noTsvMatchingFile:
            self.show_warning("tsv matching file not found", "The << Electrodes names and scales matching.tsv >> file that should be inside the Neuralynx ncs folder is missing. See example dataset provided with this program for more information.")

    def button_OK_fun(self):
        self.button_check_fun()
        if not self.display_error_pathExists and not self.display_error_noTsvMatchingFile:
            self.confirm_proceed()
        else:
            self.show_relevant_warning()

    def confirm_proceed(self):
        dest = self.destination.replace("\\", "/")
        text = (f"#------------------------------------------------\n# {os.path.split(dest)[-1]}\n#------------------------------------------------\n\n"
                f"Format: {self.ext_ComboBox.currentText().lower()}\n\nOrigin: {self.input_path_edit.text()}\n\n"
                f"Destination: {dest}\n\nThis action is definitive. If you cancel, nothing will happen.")
        if messageBox_popup("Please confirm", text, QMessageBox.Icon.Question, cancel_option=True) == QMessageBox.StandardButton.Ok:
            self.proceed_BIDSlike_architecture()
        else:
            messageBox_popup("Aborted", "Procedure aborted. Nothing will happen.", QMessageBox.Icon.Information, cancel_option=False)

    def proceed_BIDSlike_architecture(self):
        try:
            if ".ncs" in self.ext_ComboBox.currentText().lower():
                ncs_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, self.microID_edit.text(), proceed=True)
                self.description_textbox.append("\nNeuralynx [ncs] data proceeded. Data were sent to destination path.")
            elif ".nrd" in self.ext_ComboBox.currentText().lower():
                rawdata_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed=True)
                self.description_textbox.append("\nNeuralynx [nrd] data processed. Data were sent to destination path.")
            elif ".trc" in self.ext_ComboBox.currentText().lower():
                TRC_to_BIDSlike(self.input_path_edit.text(), self.path_info_dict, proceed=True)
                self.description_textbox.append("\nNeuralynx [trc] data processed. Data were sent to destination path.")
            self.displayConfirm_and_resetInputPath()
        except:
            self.description_textbox.append(traceback.format_exc())

    def displayConfirm_and_resetInputPath(self):
        messageBox_popup("Done", "Done! BIDS-like architecture created.", QMessageBox.Icon.Information, cancel_option=False)
        self.input_path_edit.setText("")

    def split_path(self, path):
        path = os.path.normpath(path)
        path_components = [comp for comp in path.split(os.sep) if comp]
        path_components.append(self.path_info_dict["BIDS_full_name"])
        return path_components

    def display_channels(self, label, channels, keyword):
        self.description_textbox.append(f"\n#---------------------------\n# {label} channels:\n#---------------------------")
        for chan_name in channels:
            if keyword in chan_name:
                self.description_textbox.append(f"# {chan_name.replace(keyword, '')}")

    def display_bids_path_tree(self, path_components):
        self.description_textbox.append("\nOriginal path:")
        self.description_textbox.append(self.input_path_edit.text())
        self.description_textbox.append("\nBIDS-like root (destination):")
        self.description_textbox.append(self.output_path_edit.text())
        self.description_textbox.append("\nBIDS-like tree:")
        for level, comp in enumerate(path_components, start=1):
            self.description_textbox.append(f"{'_'*level*2} {comp}")

    def show_error_message(self, title, message):
        error_dialog = QErrorMessage(self)
        error_dialog.setWindowTitle(title)
        error_dialog.showMessage(message)
        error_dialog.exec()

    def show_warning(self, title, message):
        messageBox_popup(title, message, QMessageBox.Icon.Critical, cancel_option=False)

    def show_relevant_warning(self):
        if self.display_error_pathExists:
            self.show_warning("Warning [2]", f"This destination folder/file path already exists: \n\n<< {os.path.normpath(self.destination).replace(os.sep, '/')} >>\n\n Nothing will happen (overwrite = False).")
        elif self.display_error_noTsvMatchingFile:
            self.show_warning("tsv matching file not found", "The << Electrodes names and scales matching.tsv >> file that should be inside the Neuralynx ncs folder is missing. See example dataset provided with this program for more information.")
