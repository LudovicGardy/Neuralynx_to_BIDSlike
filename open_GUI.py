# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:54:14 2019

@author: gardy
"""
import os
import sys
import json
import numpy as np
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QStyle, QErrorMessage,
    QTextEdit, QGridLayout, QApplication, QDialog, QPushButton,
    QVBoxLayout, QMainWindow, QMenu, QMessageBox, QSizePolicy, QAction,
    QComboBox, QHBoxLayout, QFrame, QCheckBox, QFileDialog, QTextBrowser)
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
import time

sys.path.append(r"G:\GardyL\Data_storage\EPIFAR_storage\BIDS_data\derivatives\Neuralynx_to_BIDSlike")
from create_neuralynx_BIDSlike import path_to_BIDSlikepath

class empty_win(QWidget):
    def __init__(self):
        super().__init__()

        self.init_GUI()

        self.show()

    def init_GUI(self):
        ### Def window size
        left = 200
        top = 100
        width = 600
        height = 150

        self.setGeometry(left, top, width, height)
        self.setWindowTitle('BIDS like architecture maker')

        ### BIDS naming frame
        BIDSnaming_frame = QFrame()
        BIDSnaming_layout = QHBoxLayout()
        BIDSnaming_frame.setLayout(BIDSnaming_layout)
        BIDSnaming_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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

        json_dict = json.load(open("task_names.json"))
        possible_tasknames = json_dict["possible_tasknames"]
        possible_tasknames.append("Other")

        task_label = QLabel("  Task-")
        self.taskname_ComboBox = QComboBox()
        [self.taskname_ComboBox.addItem(taskname) for taskname in possible_tasknames]
        self.taskname_ComboBox.setCurrentIndex(1)
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
        input_format_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_format_frame.setFixedHeight(30)
        input_format_layout.setContentsMargins(0, 0, 0, 0)
        input_format_layout.setSpacing(0)

        self.input_format_label = QLabel("Input format: ")

        self.input_cbox_ncs = QCheckBox(".ncs")
        self.input_cbox_ncs.setStatusTip("--")
        self.input_cbox_ncs.setChecked(False)
        self.input_cbox_ncs.stateChanged.connect(self.input_cbox_fun)

        self.input_cbox_nrd = QCheckBox(".nrd")
        self.input_cbox_nrd.setStatusTip("--")
        self.input_cbox_nrd.setChecked(False)
        self.input_cbox_nrd.stateChanged.connect(self.input_cbox_fun)

        self.input_cbox_trc = QCheckBox(".trc")
        self.input_cbox_trc.setStatusTip("--")
        self.input_cbox_trc.setChecked(False)
        self.input_cbox_trc.stateChanged.connect(self.input_cbox_fun)

        input_format_layout.addWidget(self.input_format_label)
        input_format_layout.addWidget(self.input_cbox_ncs)
        input_format_layout.addWidget(self.input_cbox_nrd)
        input_format_layout.addWidget(self.input_cbox_trc)

        ### Input data path frame
        input_path_frame = QFrame()
        input_path_layout = QHBoxLayout()
        input_path_frame.setLayout(input_path_layout)
        input_path_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_path_frame.setFixedHeight(30)
        input_path_layout.setContentsMargins(0, 0, 0, 0)
        input_path_layout.setSpacing(0)

        input_infoButton = QPushButton("")
        input_infoButton.clicked.connect(self.input_infoButton_fun)
        input_infoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_infoButton.setFixedWidth(50)
        input_infoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        input_browseButton = QPushButton("Browse...")
        input_browseButton.clicked.connect(self.input_browseButton_fun)
        input_browseButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        input_browseButton.setFixedWidth(100)

        self.input_path_edit = QLineEdit()
        self.input_path_edit.setText("")
        self.input_path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_ext_edit = QLineEdit()
        self.input_ext_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.input_ext_edit.setText("")
        self.input_ext_edit.setFixedWidth(50)
        self.input_ext_edit.setStyleSheet("background-color: lightgray")

        input_path_layout.addWidget(input_infoButton)
        input_path_layout.addWidget(input_browseButton)
        input_path_layout.addWidget(self.input_path_edit)
        input_path_layout.addWidget(self.input_ext_edit)

        ### Output data path frame
        output_path_frame = QFrame()
        output_path_layout = QHBoxLayout()
        output_path_frame.setLayout(output_path_layout)
        output_path_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_path_frame.setFixedHeight(30)
        output_path_layout.setContentsMargins(0, 0, 0, 0)
        output_path_layout.setSpacing(0)

        output_infoButton = QPushButton("")
        output_infoButton.clicked.connect(self.output_infoButton_fun)
        output_infoButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_infoButton.setFixedWidth(50)
        output_infoButton.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))

        output_browseButton = QPushButton("Browse...")
        output_browseButton.clicked.connect(self.output_browseButton_fun)
        output_browseButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        output_browseButton.setFixedWidth(100)

        self.output_path_edit = QLineEdit()
        self.output_path_edit.setText("")
        self.output_path_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        output_path_layout.addWidget(output_infoButton)
        output_path_layout.addWidget(output_browseButton)
        output_path_layout.addWidget(self.output_path_edit)

        ### Validation Frame
        self.description_textbox = QTextBrowser(self)
        self.description_textbox.setObjectName("description_textbox")
        self.description_textbox.setStyleSheet("QTextBrowser#description_textbox {background: white ;border: 2px solid #000000;}")
        self.description_textbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        validation_frame = QFrame()
        validation_layout = QVBoxLayout()
        validation_frame.setLayout(validation_layout)
        validation_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_check = QPushButton("Check information before final validation")
        button_check.setShortcut(QtCore.Qt.Key_Return)
        button_check.clicked.connect(self.button_check_fun)
        button_check.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_check.setFixedHeight(30)

        button_OK = QPushButton("OK")
        button_OK.clicked.connect(self.button_OK_fun)
        button_OK.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_OK.setFixedHeight(30)
        button_OK.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))

        validation_layout.addWidget(self.description_textbox)
        validation_layout.addWidget(button_check)
        validation_layout.addWidget(button_OK)

        # Set global layout
        GLOBAL_layout = QVBoxLayout(self)

        GLOBAL_layout.addWidget(BIDSnaming_frame)
        GLOBAL_layout.addWidget(input_format_frame)
        GLOBAL_layout.addWidget(input_path_frame)
        GLOBAL_layout.addWidget(output_path_frame)
        GLOBAL_layout.addWidget(validation_frame)

    def taskname_ComboBox_fun(self):
        if self.taskname_ComboBox.currentText() == "Other":
            error_dialog.setWindowTitle("Information")
            error_dialog = QErrorMessage()
            error_dialog.showMessage('If you want to add a new task name, you need to add it in the "task_names.json" file, which you can find in the root folder of this program.')            
            error_dialog.exec()

    def input_cbox_fun(self, callback):

        cbox_ncs_state = self.input_cbox_ncs.isChecked()
        cbox_nrd_state = self.input_cbox_nrd.isChecked()
        cbox_trc_state = self.input_cbox_trc.isChecked()

        if int(cbox_ncs_state) + int(cbox_nrd_state) + int(cbox_trc_state) > 1:
            self.input_cbox_ncs.setChecked(False)
            self.input_cbox_nrd.setChecked(False)
            self.input_cbox_trc.setChecked(False)
            self.input_ext_edit.setText("")
        else:
            if self.input_cbox_ncs.isChecked():
                self.input_ext_edit.setText(".ncs")
            elif self.input_cbox_nrd.isChecked():
                self.input_ext_edit.setText(".nrd")
            elif self.input_cbox_trc.isChecked():
                self.input_ext_edit.setText(".trc")

    def input_infoButton_fun(self):
        input_infoButton_dialog = QErrorMessage()
        input_infoButton_dialog.setWindowTitle("Input path information")
        input_infoButton_dialog.showMessage('Search or paste the path to the data you want to turn into a BIDS-like. For .ncs choose the folder, for .trc and .nrd choose the file.')            
        input_infoButton_dialog.exec()

    def input_browseButton_fun(self):
        selected_path = ""
        if self.input_cbox_trc.isChecked() or self.input_cbox_nrd.isChecked():
            selected_path = QFileDialog.getOpenFileName(None, "Select an EEG file:".format(True), fpath, "EEG files (*.trc *.nrd)")[0]
        elif self.input_cbox_ncs.isChecked():
            selected_path = QFileDialog.getExistingDirectory(None, 'Select a Neuralynx EEG folder', '~', QFileDialog.ShowDirsOnly)

        self.input_path_edit.setText(selected_path)

    def output_infoButton_fun(self):
        output_infoButton_dialog = QErrorMessage()
        output_infoButton_dialog.setWindowTitle("Output path information")
        output_infoButton_dialog.showMessage('Search or paste the path to your BIDS-like folder.')            
        output_infoButton_dialog.exec()

    def output_browseButton_fun(self):
        selected_path = ""
        selected_path = QFileDialog.getExistingDirectory(None, 'Select your BIDS-like root folder', '~', QFileDialog.ShowDirsOnly)
        self.output_path_edit.setText(selected_path)

    def button_check_fun(self):

        ### Get ext
        ext = self.input_ext_edit.text().replace(".","")

        ### Get BIDS like folder path and file names
        path_info_dict = path_to_BIDSlikepath(int(self.patient_edit.text()), int(self.sess_edit.text()), int(self.run_edit.text()), self.output_path_edit.text(), self.taskname_ComboBox.currentText())

        ### Split path
        path_components = []
        path = os.path.normpath(path_info_dict[f"BIDS_tree_{ext.lower()}"])
        path = path.split(os.sep)
        [path_components.append(_comp) for _comp in path if _comp]
        path_components.append(path_info_dict["BIDS_full_name"])

        ### Print BIDS path tree
        self.description_textbox.append("")
        self.description_textbox.append("Original filepath:")
        self.description_textbox.append(self.input_path_edit.text())
        self.description_textbox.append("BIDS-like filepath:")
        self.description_textbox.append(self.output_path_edit.text())

        self.description_textbox.append("")
        self.description_textbox.append("BIDS-like tree:")
        tree_level = 1
        for _comp in path_components:
            self.description_textbox.append("{} {}".format( "-"*tree_level,_comp ))
            tree_level+=2

    def button_OK_fun(self):
        print("OK")

if __name__ == "__main__":

    # Avoid python kernel from dying
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # run
    mywindow = empty_win()
    sys.exit(app.exec_())
