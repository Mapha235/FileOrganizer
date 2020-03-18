from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush
from PyQt5.QtWidgets import QApplication, QFileDialog, QGridLayout, QWidget, QSizePolicy, QTextBrowser, QLabel
import sys
from stylesheets import *


class TheWindow(QWidget):

    def __init__(self):
        super(TheWindow, self).__init__()

        self.x = 960
        self.y = 200
        self.my_width = 800
        self.my_height = 500

        # Background image
        QWidget.__init__(self)
        bg = QImage("C:/Dev/python/FileOrganizer/data/bg.png")
        scaled_bg = bg.scaled(QSize(self.my_width, self.my_height))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))  # 10 = Windowrole
        self.setPalette(palette)
        self.show()

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create new entry", self)

        # used for mouse hover event
        self.create_entry_button.installEventFilter(self)
        self.settings_button.installEventFilter(self)

        # Text fields
        self.source_text_browser = QTextBrowser()
        self.target_text_browser = QTextBrowser()
        self.keyword_text_browser = QTextBrowser()

        # set window size
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)

        self.setWindowTitle("File Organizer")
        self.initUI()

    def initUI(self):
        buttons = []

        # Design of the settings button
        self.settings_button.setFixedWidth(70)
        self.settings_button.setIcon(QtGui.QIcon("C:/Dev/python/FileOrganizer/data/Settings2.png"))
        self.settings_button.setIconSize(QtCore.QSize(60, 60))
        self.settings_button.clicked.connect(self.open_dialog_box)
        buttons.append(self.settings_button)
        buttons.append(self.create_entry_button)

        # assign design layout to all widgets
        self.settings_button.setStyleSheet(layout1)
        self.create_entry_button.setStyleSheet(layout1)
        self.source_text_browser.setStyleSheet(layout1)
        self.target_text_browser.setStyleSheet(layout1)
        self.keyword_text_browser.setStyleSheet(layout1)

        layout_grid = QGridLayout()

        self.setLayout(layout_grid)
        layout_grid.setSpacing(10)

        for button in buttons:
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_grid.addWidget(self.settings_button, 0, 0)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 7)

        layout_grid.addWidget(self.keyword_text_browser, 1, 0, 1, 8)
        layout_grid.addWidget(self.source_text_browser, 2, 0, 1, 4)
        layout_grid.addWidget(self.target_text_browser, 2, 4, 1, 4)

    def clicked(self):
        self.label.setText("you pressed THE button")

    def setStyleSheet(self, styleSheet: str):
        for widgets in self.widgets:
            widgets.super(self).setStyleSheet(styleSheet)

    def eventFilter(self, obj, event):
        if obj == self.settings_button:
            button = self.settings_button
        elif obj == self.create_entry_button:
            button = self.create_entry_button
        else:
            return

        if event.type() == QtCore.QEvent.HoverEnter:
            self.onHovered(button)

        return super(TheWindow, self).eventFilter(obj, event)

    def onHovered(self, btn):
        btn.setStyleSheet(mouse_hover)

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName(self)
        print(filename)

    def my_print(self):
        print(self.height)

    def update(self):
        # self.x = self.x()
        # self.y = self.y()
        self.my_width = self.width()
        self.my_height = self.height()

        self.my_print()


# QTextEdit


def window():
    app = QApplication(sys.argv)
    win = TheWindow()

    win.show()
    sys.exit(app.exec_())


window()
