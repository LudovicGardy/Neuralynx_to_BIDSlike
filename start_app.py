# -*- coding: utf-8 -*-
"""
Creation date: 2022, January 27
Author: L. Gardy
E-mail: ludovic.gardy@cnrs.fr
Encoding: UTF-8
"""
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication
import sys

from BIDS_like_converter.GUI.main_GUI import BIDSlike_creator_win

if __name__ == "__main__":

    # Avoid python kernel from dying
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # run
    mywindow = BIDSlike_creator_win()
    sys.exit(app.exec())
