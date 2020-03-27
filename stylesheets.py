import sys
import re
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QGridLayout, QApplication, QSizePolicy, QTextBrowser, \
    QStackedLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit
from lib.folder import Folder

dark = """
            font-size: 14pt;
            color: white;
            background-color: rgba(0,0,0,0.4);
            """

light = """
            font-size: 14pt;
            font-weight: bold;
            color: rgb(225,225,225);
            background-color: rgba(255,255,255,0.4);
            """

entry_layout = """
            font-size: 10pt;
            font-weight: normal;
            background-color: rgba(255,255,255,0.3);
            """

mouse_hover = """
                border: 2px solid rgb(255, 255, 255);
                color: white;
                """

entry_mouse_hover = """
                border: 1px solid rgb(255, 255, 255);
                color: white;
                border-radius: 5px;
                """

mouse_click = """
        color: white;
        background-color: rgba(255, 255, 255, 0.5);
"""
examples = """
        font-size: 8pt;
        color: white;
        background-color: rgba(255, 255, 255, 0.0);
        margin: 10px;
        """



