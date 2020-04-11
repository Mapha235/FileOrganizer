import sys
import re
import os
from itertools import count
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor, QKeySequence
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QGridLayout, QApplication, QSizePolicy, QTextBrowser, \
    QStackedLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QCheckBox, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QShortcut
from lib.folder import Folder


dark = """
            font-size: 14pt;
            color: white;
            background-color: rgba(0,0,0,0.3);
            """

light = """
            font-size: 14pt;
            font-weight: bold;
            color: rgb(70,70,70);
            background-color: rgba(255,255,255,0.4);
            """

entry_layout = """
            color: black;
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

