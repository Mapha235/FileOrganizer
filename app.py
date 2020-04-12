from main import makeScrollable
from main import shorten_path
from stylesheets import *
from entrywindow import EntryWindow
from entry import Entry
from settings import Settings


class TheWindow(QWidget):
    def __init__(self, values: list):
        super(TheWindow, self).__init__()
        self.entry_box_layout = QVBoxLayout()
        self.scroll = QScrollArea()
        self.x = 160
        self.y = 200
        self.my_width = 800
        self.my_height = 500
        self.source_path = ""
        self.target_path = ""

        self.entry_window = None
        self.settings_page = None

        self.entries = []
        self.analyze_values(values)

        # set Background Image
        self.bg = QImage("./data/bg4.jpg")

        self.settings_button = QtWidgets.QPushButton(self)
        self.create_entry_button = QtWidgets.QPushButton("Create New Entry", self)
        self.run_script_button = QtWidgets.QPushButton(self)
        self.target_button = QtWidgets.QPushButton("Target Content")
        self.source_button = QtWidgets.QPushButton("Source Content")

        # list of all buttons
        self.buttons = []

        self.buttons.append(self.settings_button)
        self.buttons.append(self.create_entry_button)
        self.buttons.append(self.run_script_button)
        self.buttons.append(self.source_button)
        self.buttons.append(self.target_button)

        self.source_table = QTableWidget()
        self.source_table.setStyleSheet(entry_layout + "color: black;")
        self.source_table.setColumnCount(1)

        self.shortcut = QShortcut(QKeySequence("Ctrl+M"), self)

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

        self.initFuncs()
        self.initUI()
        self.button_handler()

    def save_state(self):
        file = open("./data/save.txt", "w")
        for it in self.entries:
            file.write(f"{it[0]},"
                       f"{it[1].script.get_source_dir()},"
                       f"{it[1].script.get_target_dir()},"
                       f"{it[1].script.get_keywords()},"
                       f"{it[1].get_check_box()},\n")


    def analyze_values(self, values: list):
        for it in values:
            self.entries.append((int(it[0]), Entry(it[1], it[2], it[3], it[4] == "True")))

    def initFuncs(self):
        for it in self.entries:
            it[1].clicked_signal.connect(self.show_content)
            it[1].send_id.connect(self.organize_entries)
            it[1].send_id2.connect(self.adjust_buttons)

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

        self.source_button.setFixedWidth(345)
        self.target_button.setFixedWidth(345)
        self.source_button.setStyleSheet("font-size: 10pt")
        self.target_button.setStyleSheet("font-size: 10pt")
        self.source_button.clicked.connect(lambda: os.system(f"explorer {self.source_path}"))
        self.target_button.clicked.connect(lambda: os.system(f"explorer {self.target_path}"))

        for button in self.buttons:
            # used for mouse hover event
            button.installEventFilter(self)

        self.buttons.clear()

        # assign design layout to all widgets
        self.scroll = makeScrollable(self.entry_box)
        self.setStyleSheet(light)
        self.createGridLayout()
        self.createBoxLayout()

        for it in self.entries:
            self.entry_box_layout.addWidget(it[1])

        self.show()

    def button_handler(self):
        self.run_script_button.clicked.connect(self.run_task)
        self.shortcut.activated.connect(self.run_task)

    def createBoxLayout(self):
        self.entry_box_layout.setAlignment(Qt.AlignTop)
        self.entry_box_layout.setContentsMargins(0, 0, 0, 0)

        self.entry_box.setLayout(self.entry_box_layout)

    def has_duplicate(self, s: str, t: str, k: str):
        msg = QMessageBox()
        for it in self.entries:
            if it[1].script.get_source_dir() == s and it[1].script.get_target_dir() == t:
                msg.setWindowTitle("Error")
                msg.setText("Error: An identical entry already exists.\nMerge with existing entry?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                ret = msg.exec()
                if ret == QMessageBox.Yes:
                    if not it[1].keywords.text():
                        temp = k
                    else:
                        temp = f"//{k}"
                    it[1].script.set_keywords(it[1].script.get_keywords() + temp)
                    it[1].keywords.insert(temp)
                elif ret == QMessageBox.No:
                    pass
                return True
            else:
                continue
        return False


    def parse(self, data: list):
        if len(data) < 3:
            print("Error!")
        elif not self.has_duplicate(data[0], data[1], data[2]):
            entry = Entry(data[0], data[1], data[2])
            self.entries.append((entry.my_id, entry))
            self.entry_box_layout.addWidget(entry)

            entry.clicked_signal.connect(self.show_content)
            entry.send_id.connect(self.organize_entries)
            entry.send_id2.connect(self.adjust_buttons)

    def run_task(self):
        for i in self.entries:
            if i[1].get_check_box():
                i[1].script.move()
                i[1].mousePressEvent(i[1].clicked)

    def organize_entries(self, index):
        for i in range(index + 1, len(self.entries)):
            self.entries[i][1].adjustID()
            self.entries[i] = (self.entries[i][1].my_id,) + self.entries[i][1:]
        self.entries.pop(index)

    def show_content(self, source_data: list, target_data: list, keyword: str):
        self.source_table.setRowCount(len(source_data))
        self.target_table.setRowCount(len(target_data))
        keyword_list = keyword.split("//")

        for i in range(0, len(source_data)):
            temp = QTableWidgetItem(source_data[i])
            self.source_table.setItem(i, 0, temp)
            self.source_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

            if any(key in source_data[i] for key in keyword_list):
                temp.setForeground(QBrush(QColor(255, 0, 0)))

        for i in range(0, len(target_data)):
            self.target_table.setItem(i, 0, QTableWidgetItem(target_data[i]))


    def adjust_buttons(self, index):
        entry = self.entries[index][1]
        s = entry.script.get_source_dir()
        t = entry.script.get_target_dir()
        self.source_button.setText(entry.source.text())
        self.target_button.setText(entry.target.text())
        self.source_path = entry.script.backslashes(s)
        self.target_path = entry.script.backslashes(t)

    def openEntry(self):
        self.entry_window = EntryWindow(self.pos().x() + (self.width() / 4), self.pos().y() + 50)
        self.entry_window.show()
        self.entry_window.send_signal.connect(self.parse)

    def createGridLayout(self):
        layout_grid = QGridLayout()

        layout_grid.setSpacing(10)

        layout_grid.addWidget(self.settings_button, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_button, 0, 1, 1, 8)

        layout_grid.addWidget(self.scroll, 1, 0, 1, 9)

        layout_grid.addWidget(self.source_button, 2, 0, 1, 4)
        layout_grid.addWidget(self.target_button, 2, 5, 1, 4)

        layout_grid.addWidget(self.source_table, 3, 0, 1, 4)
        layout_grid.addWidget(self.run_script_button, 3, 4, 1, 1)
        layout_grid.addWidget(self.target_table, 3, 5, 1, 4)
        self.setLayout(layout_grid)

    def doAnimation(self):
        self.settings_page = Settings(self.pos().x() - 400, self.pos().y() + 60)
        self.anim = QPropertyAnimation(self.settings_page, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(-1000, 100, 500, 400))
        self.anim.setEndValue(QRect(0, 100, 500, 400))
        self.anim.start()

    def eventFilter(self, obj, event):
        if obj == self.source_button or obj == self.target_button:
            font_size = "font-size:10pt;"
        else:
            font_size = ""

        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setStyleSheet(mouse_hover + font_size)
            obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover + mouse_click + font_size)
        elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
            obj.setStyleSheet(mouse_hover + font_size)
            if obj == self.create_entry_button:
                self.openEntry()
            elif obj == self.settings_button:
                self.doAnimation()
        elif event.type() == QtCore.QEvent.HoverLeave:
            obj.setStyleSheet(light + font_size)
        return super(TheWindow, self).eventFilter(obj, event)

    def resizeUI(self):
        self.my_width = self.width()
        self.my_height = self.height()

        self.scroll.setFixedHeight(int(self.height() / 3))

        # set background image
        scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(scaled_bg))
        self.setPalette(palette)

    def resizeEvent(self, event):
        self.resizeUI()


    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.save_state()