import sys
import re
import os
from itertools import count
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSignal, QSize, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QImage, QPalette, QBrush, QColor, QKeySequence, QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget, QGridLayout, QApplication, QSizePolicy, QTextBrowser, \
    QStackedLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QScrollArea, QLineEdit, QCheckBox, QLabel, QTableWidget, QTableWidgetItem, QAbstractItemView, QShortcut
from lib.folder import Folder
from settings import Settings


default = """ """

dark = """
            color: white;
            background-color: rgba(0,0,0,0.2);
            """

light = """
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

mouse_click = """
        color: white;
        background-color: rgba(255, 255, 255, 0.5);
"""

examples = """
        font-size: 8pt;
        background-color: rgba(255, 255, 255, 0.0);
        margin: 10px;
        """


