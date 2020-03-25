import re

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSignal

from app import *

from stylesheets import *


class EntryWindow(QWidget):
    send_data = pyqtSignal([])
    def __init__(self, x, y):
        super(EntryWindow, self).__init__()
        self.data = [None]*3
        self.x = x
        self.y = y

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        # set Background Image
        self.bg = QImage("C:/Dev/python/FileOrganizer/data/bg4.jpg")

        self.source_button = QtWidgets.QPushButton("Browse Source Folder", self)
        self.source_button.setObjectName("0")
        self.target_button = QtWidgets.QPushButton("Browse Target Folder", self)
        self.target_button.setObjectName("1")

        self.add_button = QtWidgets.QPushButton("Add", self)
        self.cancel_button = QtWidgets.QPushButton("Cancel", self)

        self.buttons = []
        self.buttons.append(self.target_button)
        self.buttons.append(self.source_button)
        self.buttons.append(self.add_button)
        self.buttons.append(self.cancel_button)

        self.label = QtWidgets.QLabel("Example: urlaub//.pdf//5e-43c5")

        self.keyword_text_field = QtWidgets.QLineEdit(self)
        self.keyword_text_field.setPlaceholderText("Enter keyword(s)")
        self.initUI()

    def initUI(self):

        self.setWindowTitle("Add New Entry")
        self.setFixedSize(400, 100)
        self.setGeometry(self.x, self.y, self.width(), self.height())

        for button in self.buttons:
            button.installEventFilter(self)
            button.setFixedHeight(18)
        self.buttons.clear()
        self.source_button.setFixedSize(int(self.width() / 2) - 6, 18)

        self.setStyleSheet(entry_layout + "color: white")
        self.label.setStyleSheet(examples)

        self.createGridLayout()

    def createGridLayout(self):
        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(3)

        layout_grid.addWidget(self.source_button, 0, 0, 1, 4)
        layout_grid.addWidget(self.target_button, 0, 4, 1, 4)
        layout_grid.addWidget(self.keyword_text_field, 1, 0, 1, 8)

        layout_grid.addWidget(self.label, 2, 0, 1, 4)
        layout_grid.addWidget(self.add_button, 2, 4, 1, 2)
        layout_grid.addWidget(self.cancel_button, 2, 6, 1, 2)

    def eventFilter(self, obj, event):
        """if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(entry_mouse_hover)
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(entry_mouse_hover + mouse_click)"""
        if event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            if obj == self.source_button or obj == self.target_button:
                self.open_dialog_box(obj)
            elif obj == self.cancel_button:
                self.close()
            elif obj == self.add_button:
                self.get_keyword()
                self.close()
            """obj.setStyleSheet(entry_mouse_hover)
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(entry_layout)"""
        return super(EntryWindow, self).eventFilter(obj, event)

    def open_dialog_box(self, btn: QtWidgets.QPushButton):
        path_name = QFileDialog.getExistingDirectory(self)
        counter = 0
        shortened_path_name = ""

        # shortened_path_name = re.search(r'/(.*)/', path_name)
        # shortens the path to the last two folders

        self.data[int(btn.objectName())] = path_name

        for i in reversed(path_name):
            if counter >= 2:
                break
            elif i == '/':
                counter += 1
            shortened_path_name += i

        shortened_path_name = shortened_path_name[::-1]
        if shortened_path_name != "":
            btn.setText("..." + shortened_path_name)
        print(shortened_path_name)

    def get_keyword(self):
        self.data[2] = self.keyword_text_field.text()
        print("Entry: " + self.data[2])

    def resizeBG(self):
        # set background image
        scaled_bg = self.bg.scaled(QSize(self.width(), self.height()))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeBG()
