from main import makeScrollable
from stylesheets import *
from entrywindow import EntryWindow
from entry import Entry
from settings import Settings


class TheWindow(QWidget):
    def __init__(self):
        super(TheWindow, self).__init__()
        self.scroll = QScrollArea()
        self.x = -1160
        self.y = 200
        self.my_width = 800
        self.my_height = 500

        self.entry_window = None
        self.settings_page = None

        self.entries = []

        # set Background Image
        self.bg = QImage("./data/bg4.jpg")

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create New Entry", self)
        self.run_script_button = QtWidgets.QPushButton(self)

        # list of all buttons
        self.buttons = []

        self.buttons.append(self.settings_button)
        self.buttons.append(self.create_entry_button)
        self.buttons.append(self.run_script_button)

        self.source_table = QTableWidget()
        self.source_table.setStyleSheet(entry_layout + "color: black;")
        self.source_table.setColumnCount(1)

        header = self.source_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.hide()

        self.target_table = QTableWidget(self)
        self.target_table.setStyleSheet(entry_layout + "color: black;")
        self.target_table.setColumnCount(1)

        header2 = self.target_table.horizontalHeader()
        header2.hide()
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.entry_box = QGroupBox(self)
        self.entry_box.setStyleSheet(
            "font-size: 14pt; color: rgb(225,225,225); background-color: rgba(255,255,255,0.0); ")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("File Organizer")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.setFixedSize(800, 500)

        # Design of the settings button
        self.settings_button.setFixedSize(70, 70)
        self.settings_button.setIcon(
            QtGui.QIcon("./data/Settings.png"))

        self.settings_button.setIconSize(QtCore.QSize(60, 60))

        self.run_script_button.setFixedWidth(70)
        self.run_script_button.setIcon(
            QtGui.QIcon("./data/arrow.png"))
        self.run_script_button.setIconSize(QtCore.QSize(60, 60))

        self.create_entry_button.setFixedHeight(70)

        for button in self.buttons:
            # used for mouse hover event
            button.installEventFilter(self)

        self.buttons.clear()

        # self.settings_button.clicked.connect(self.rotate)

        # assign design layout to all widgets
        self.scroll = makeScrollable(self.entry_box)
        self.setStyleSheet(light)
        self.createGridLayout()
        self.createBoxLayout()
        self.show()

    def createBoxLayout(self):
        self.trash_box = QVBoxLayout()

        self.trash_box.setAlignment(Qt.AlignTop)
        self.trash_box.setContentsMargins(0, 0, 0, 0)

        self.entry_box.setLayout(self.trash_box)

    def parse(self, data: list):
        if len(data) != 3:
            print("Error!")
        else:
            entry = Entry((((self.height() - 110) / 2) - 60) / 5, data[0], data[1], data[2])

            def run_task():
                if entry.get_check_box():
                    entry.script.move()

            self.run_script_button.clicked.connect(run_task)

            self.trash_box.addWidget(entry)
            entry.clicked_signal.connect(self.show_content)

    def show_content(self, source_data: list, target_data: list, keyword: str):
        self.source_table.setRowCount(len(source_data))
        self.target_table.setRowCount(len(target_data))

        for i in range(0, len(source_data)):
            temp = QTableWidgetItem(source_data[i])
            self.source_table.setItem(i, 0, temp)
            self.source_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            if source_data[i].__contains__(keyword):
                temp.setForeground(QBrush(QColor(255, 0, 0)))

        for i in range(0, len(target_data)):
            self.target_table.setItem(i, 0, QTableWidgetItem(target_data[i]))

    def createGridLayout(self):
        layout_grid = QGridLayout()

        layout_grid.setSpacing(10)

        label = QLabel("Source Content")
        label.setAlignment(Qt.AlignCenter)
        label2 = QLabel("Target Content")
        label2.setAlignment(Qt.AlignCenter)

        layout_grid.addWidget(self.settings_button, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 8)

        layout_grid.addWidget(self.scroll, 1, 0, 1, 9)

        layout_grid.addWidget(label, 2, 0, 1, 4)
        layout_grid.addWidget(label2, 2, 5, 1, 4)

        layout_grid.addWidget(self.source_table, 3, 0, 1, 4)
        layout_grid.addWidget(self.run_script_button, 3, 4, 1, 1)
        layout_grid.addWidget(self.target_table, 3, 5, 1, 4)
        self.setLayout(layout_grid)

    def openEntry(self):
        self.entry_window = EntryWindow(self.pos().x() + (self.width() / 4), self.pos().y() + 50)
        self.entry_window.show()
        self.entry_window.send_signal.connect(self.parse)

    def doAnimation(self):
        self.settings_page = Settings(self.pos().x() - 400, self.pos().y() + 60)
        self.anim = QPropertyAnimation(self.settings_page, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(-1000, 100, 500, 400))
        self.anim.setEndValue(QRect(0, 100, 500, 400))
        self.anim.start()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(mouse_hover)
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover + mouse_click)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover)
            if obj == self.create_entry_button:
                self.openEntry()
            elif obj == self.settings_button:
                self.doAnimation()
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(light)
        return super(TheWindow, self).eventFilter(obj, event)

    def resizeUI(self):
        self.my_width = self.width()
        self.my_height = self.height()

        self.scroll.setFixedHeight(int(self.height() / 3))

        for entry in self.entries:
            entry.setFixedHeight((((self.height() - 110) / 2) - 30) / 5)

        # set background image
        scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeUI()
