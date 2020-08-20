from main import makeScrollable
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
        self.my_width = 1000
        self.my_height = 600
        self.src_path = ""
        self.dst_path = ""

        self.setMinimumSize(1000, 500)

        self.language = "ENG"

        self.entry_window = None
        self.settings_page = None

        self.entries = []

        self.setWindowIcon(QtGui.QIcon("./data/icon.png"))

        self.settings_btn = QtWidgets.QPushButton(self)
        self.create_entry_btn = QtWidgets.QPushButton("Create New Entry", self)
        self.run_script_btn = QtWidgets.QPushButton(self)
        self.dst_btn = QtWidgets.QPushButton("Destination Content")
        self.src_btn = QtWidgets.QPushButton("Source Content")

        # list of all btns
        self.btns = []

        self.btns.append(self.settings_btn)
        self.btns.append(self.create_entry_btn)
        self.btns.append(self.run_script_btn)
        self.btns.append(self.src_btn)
        self.btns.append(self.dst_btn)

        self.src_table = QTableWidget()
        self.src_table.setColumnCount(1)

        self.shortcut = QShortcut(QKeySequence("Ctrl+M"), self)

        header = self.src_table.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.hide()

        self.dst_table = QTableWidget(self)
        self.dst_table.setColumnCount(1)

        header2 = self.dst_table.horizontalHeader()
        header2.hide()
        header2.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.entry_box = QGroupBox(self)

        self.files_moved_label = QtWidgets.QLabel()
        self.files_moved_label.setAlignment(Qt.AlignCenter)
        self.files_moved_label.hide()

        try:
            self.root = values[0][0]
            self.bg_path = values[0][2]

            self.theme = dark
            self.set_theme(int(values[0][1]), self.bg_path)
        except IndexError:
            self.theme = default
            self.bg_path = ""
        values.pop(0)

        self.analyze_values(values)

        self.initFuncs()
        self.initUI()
        self.button_handler()

    def initUI(self):
        self.setWindowTitle("File Organizer")
        self.setGeometry(self.x, self.y, self.my_width, self.my_height)
        self.bg = QImage(self.bg_path)
        # self.setFixedSize(self.my_width, self.my_height)

        # Design of the settings btn
        # self.settings_btn.setFixedSize(70, 70)

        # self.create_entry_btn.setFixedHeight(70)

        # self.src_btn.setFixedWidth(self.src_table.frameGeometry().width())
        # print(self.src_table.frameGeometry().width())
        # self.dst_btn.setFixedWidth(self.src_table.frameGeometry().width())
        # print(self.src_table.frameGeometry().width())

        for btn in self.btns:
            # used for mouse hover event
            btn.installEventFilter(self)

        # self.btns.clear()

        # assign design layout to all widgets
        self.scroll = makeScrollable(self.entry_box)
        self.createGridLayout()
        self.createBoxLayout()

        for it in self.entries:
            # entry_width = (self.frameGeometry().width() - 20)
            # entry_height = self.entry_box.frameGeometry().height() / 5
            # it.setFixedSize(entry_width, entry_height)
            self.entry_box_layout.addWidget(it)

        self.update_theme()

        self.show()

    def save_state(self):
        file = open(f"{self.root}/data/save.txt", "w")
        file.write(f"{self.root}|")
        file.write(f"{self.get_theme()}|")
        file.write(f"{self.bg_path}|\n")
        file.close()
        file = open(f"{self.root}/data/save.txt", "a")

        for it in self.entries:
            file.write(f"{it.my_id}|"
                       f"{it.script.get_src_dir()}|"
                       f"{it.script.get_dst_dir()}|"
                       f"{it.script.get_keywords()}|"
                       f"{it.get_check_box()}|\n")
        file.close()

    def update_theme(self):
        self.settings_icon = QtGui.QIcon("./data/einstellungen.png")
        self.arrow_icon = QtGui.QIcon("./data/arrow2.png")

        if self.theme is not default:

            if self.theme is dark:
                pix = QtGui.QPixmap("./data/einstellungen.png")
                pix2 = QtGui.QPixmap("./data/arrow2.png")
                painter = QtGui.QPainter(pix)
                painter.setCompositionMode(
                    QtGui.QPainter.CompositionMode_SourceIn)
                painter.fillRect(pix.rect(), QtGui.QColor(255, 255, 255))
                painter.end()
                painter2 = QtGui.QPainter(pix2)
                painter2.setCompositionMode(
                    QtGui.QPainter.CompositionMode_SourceIn)
                painter2.fillRect(pix.rect(), QtGui.QColor(255, 255, 255))
                painter2.end()
                self.settings_icon.addPixmap(pix)
                self.arrow_icon.addPixmap(pix2)

            # set background image
            self.bg = QImage(self.bg_path)
            scaled_bg = self.bg.scaled(QSize(self.my_width, self.my_height))
            palette = QPalette()
            palette.setBrush(QPalette.Background, QBrush(scaled_bg))
            self.setPalette(palette)

        else:
            self.setPalette(self.style().standardPalette())
            self.bg_path = ""

        self.settings_btn.setIcon(QtGui.QIcon(self.settings_icon))
        icon_size = self.settings_btn.size().height() * 2 / 3
        self.settings_btn.setIconSize(QtCore.QSize(icon_size, icon_size))

        self.run_script_btn.setFixedWidth(self.my_width / 10)
        self.run_script_btn.setFixedSize(
            (self.my_width - (self.my_width % 100) - 100) / 10, (self.my_width - (self.my_width % 100) - 100) / 10)

        self.run_script_btn.setIcon(QtGui.QIcon(self.arrow_icon))
        self.run_script_btn.setIconSize(QtCore.QSize(60, 60))

        self.settings_btn.setStyleSheet(self.theme)
        self.create_entry_btn.setStyleSheet(self.theme + "font-size: 14pt")
        self.run_script_btn.setStyleSheet(self.theme)

        self.src_btn.setStyleSheet(self.theme + "font-size: 10pt")
        self.dst_btn.setStyleSheet(self.theme + "font-size: 10pt")

        self.files_moved_label.setStyleSheet(self.theme)

        self.src_table.setStyleSheet(
            self.theme + "font-size: 10pt; color: black;")
        self.dst_table.setStyleSheet(
            self.theme + "font-size: 10pt; color: black;")
        self.entry_box.setStyleSheet(self.theme)

    def analyze_values(self, values: list):
        for it in values:
            self.entries.append(
                Entry(self.root, it[1], it[2], it[3], it[4] == "True"))

    def initFuncs(self):
        for it in self.entries:
            it.clicked_signal.connect(self.show_content)
            it.send_id.connect(self.organize_entries)
            it.send_id2.connect(self.adjust_buttons)
            it.files_moved_signal.connect(self.message)

    def button_handler(self):
        self.run_script_btn.clicked.connect(self.run_task)
        self.shortcut.activated.connect(self.run_task)
        self.create_entry_btn.clicked.connect(self.openEntry)
        self.settings_btn.clicked.connect(self.open_settings)
        self.src_btn.clicked.connect(
            lambda: os.system(f"explorer {self.src_path}"))
        self.dst_btn.clicked.connect(
            lambda: os.system(f"explorer {self.dst_path}"))

    def createBoxLayout(self):
        self.entry_box_layout.setAlignment(Qt.AlignTop)
        self.entry_box_layout.setContentsMargins(0, 0, 0, 0)

        self.entry_box.setLayout(self.entry_box_layout)

    def has_duplicate(self, s: str, t: str, k: str):
        msg = QMessageBox()
        for it in self.entries:
            if it.script.get_src_dir() == s and it.script.get_dst_dir() == t:
                msg.setWindowTitle("Error")
                msg.setText(
                    "Error: An identical entry already exists.\nMerge with existing entry?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                msg.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
                ret = msg.exec()
                if ret == QMessageBox.Yes:
                    if not it.keywords.text():
                        temp = k
                    else:
                        temp = f"//{k}"
                    it.script.set_keywords(it.script.get_keywords() + temp)
                    it.keywords.insert(temp)
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
            entry = Entry(self.root, data[0], data[1], data[2])
            self.entries.append(entry)
            self.entry_box_layout.addWidget(entry)

            entry.clicked_signal.connect(self.show_content)
            entry.send_id.connect(self.organize_entries)
            entry.send_id2.connect(self.adjust_buttons)
            # IDEA: on click: send id of the entry and use it to access self.entries and entry.func()

    def message(self, files):
        self.files_moved_label.show()
        if files == 1:
            msg = "1 file moved."
        else:
            msg = f"{files} files moved."

        self.files_moved_label.setText(msg)

    def run_task(self):
        files_moved = 0
        for it in self.entries:
            if it.get_check_box():
                temp = it.script.move()
                files_moved += temp

        for it in self.entries:
            if it.get_check_box():
                it.script.remove()
                it.mousePressEvent(it.clicked)

        self.message(files_moved)

    def organize_entries(self, index):
        for i in range(index + 1, len(self.entries)):
            self.entries[i].adjustID()
        self.entries.pop(index)

    def show_content(self, src_folders: list, src_files: list, dst_folders: list, dst_files: list, keywords: str):
        self.src_table.setRowCount(len(src_folders) + len(src_files))

        self.dst_table.setRowCount(len(dst_folders) + len(dst_files))

        keyword_list = keywords.split("//")

        src_file_count = len(src_files)
        dst_file_count = len(dst_files)



        for i in range(0, src_file_count + len(src_folders)):

            if i >= src_file_count:
                if src_file_count == 0:
                    temp = QTableWidgetItem(src_folders[i])
                else:
                    temp = QTableWidgetItem(src_folders[i % src_file_count])

                self.src_table.setItem(i, 0, temp)
                self.src_table.item(i, 0).setForeground(QtGui.QColor(128, 128, 128))
            else:
                temp = QTableWidgetItem(src_files[i])
                self.src_table.setItem(i, 0, temp)

                self.src_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                if self.theme == dark:
                    temp.setForeground(QBrush(QColor(255, 255, 255)))

                if any(key in src_files[i] for key in keyword_list):

                    if self.theme is dark:
                        temp.setForeground(QBrush(QColor(225, 127, 80)))
                    else:
                        temp.setForeground(QBrush(QColor(225, 100, 80)))
                    font = QtGui.QFont()
                    font.setBold(True)
                    temp.setFont(font)


        for i in range(0, dst_file_count + len(dst_folders)):
            if i >= dst_file_count:
                if dst_file_count == 0:
                    temp = QTableWidgetItem(dst_folders[i])
                else:
                    temp = QTableWidgetItem(dst_folders[i % dst_file_count])
                    

                self.dst_table.setItem(i, 0, temp)
                self.dst_table.item(i, 0).setForeground(QtGui.QColor(128, 128, 128))

            else:
                temp = QTableWidgetItem(dst_files[i])
                self.dst_table.setItem(i, 0, temp)

                if self.theme == dark:
                    temp.setForeground(QBrush(QColor(255, 255, 255)))


    def adjust_buttons(self, index):
        entry = self.entries[index]
        s = entry.script.get_src_dir()
        t = entry.script.get_dst_dir()
        self.src_btn.setText(entry.src.text())
        self.dst_btn.setText(entry.dst.text())
        self.src_path = entry.script.backslashes(s)
        self.dst_path = entry.script.backslashes(t)

    def openEntry(self):
        self.entry_window = EntryWindow(self.pos().x() + (self.width() / 4), self.pos().y() + 50, self.get_theme(),
                                        self.bg_path)
        #self.entry_window.setFixedSize(self.my_width / 2, self.my_height / 5)
        self.entry_window.show()
        self.entry_window.send_signal.connect(self.parse)

    def createGridLayout(self):
        layout_grid = QGridLayout()

        layout_grid.setSpacing(10)

        layout_grid.addWidget(self.settings_btn, 0, 0, 1, 1)
        layout_grid.addWidget(self.create_entry_btn, 0, 1, 1, 8)

        layout_grid.addWidget(self.scroll, 1, 0, 1, 9)

        layout_grid.addWidget(self.src_btn, 2, 0, 1, 4)
        layout_grid.addWidget(self.files_moved_label, 2, 4, 1, 1)
        layout_grid.addWidget(self.dst_btn, 2, 5, 1, 4)

        layout_grid.addWidget(self.src_table, 3, 0, 1, 4)
        layout_grid.addWidget(self.run_script_btn, 3, 4, 1, 1)
        layout_grid.addWidget(self.dst_table, 3, 5, 1, 4)
        self.setLayout(layout_grid)

    def eventFilter(self, obj, event):
        if obj == self.src_btn or obj == self.dst_btn:
            font_size = "font-size:10pt;"
        else:
            font_size = "font-size:14pt;"

        if obj is self.settings_btn:
            icon_path = "./data/einstellungen.png"
        elif obj is self.run_script_btn:
            icon_path = "./data/arrow2.png"

        if self.theme is not default:
            if event.type() == QtCore.QEvent.HoverEnter:
                if self.theme is light:
                    obj.setStyleSheet(
                        mouse_hover + "background-color: rgba(255, 255, 255, 0.5);" + font_size)
                else:
                    obj.setStyleSheet(mouse_hover + font_size)

                if (obj is self.settings_btn or obj is self.run_script_btn) and self.theme is light:
                    icon = QtGui.QIcon(icon_path)
                    pix = QtGui.QPixmap(icon_path)
                    painter = QtGui.QPainter(pix)
                    painter.setCompositionMode(
                        QtGui.QPainter.CompositionMode_SourceIn)
                    painter.fillRect(pix.rect(), QtGui.QColor(255, 255, 255))
                    painter.end()
                    icon.addPixmap(pix)
                    obj.setIcon(icon)
                obj.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            elif event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.LeftButton:
                obj.setStyleSheet(mouse_hover + mouse_click + font_size)
            elif event.type() == QtCore.QEvent.MouseButtonRelease and event.button() == QtCore.Qt.LeftButton:
                obj.setStyleSheet(mouse_hover + font_size)
            elif event.type() == QtCore.QEvent.HoverLeave:
                obj.setStyleSheet(self.theme + font_size)
                if self.theme is light:
                    if obj is self.settings_btn:
                        obj.setIcon(self.settings_icon)
                    elif obj is self.run_script_btn:
                        obj.setIcon(self.arrow_icon)

        return super(TheWindow, self).eventFilter(obj, event)

    def open_settings(self):
        self.settings_page = Settings(self.pos().x() + 10, self.pos().y() + 120, self.language is "ENG",
                                      self.get_theme(), self.bg_path == f"{self.root}/data/bg4.jpg", self.root)

        settings_win_width = self.my_width / 3
        settings_win_height = self.my_height - 150
        if settings_win_height < 540:
            settings_win_height = 540
        if settings_win_width < 400:
            settings_win_width = 400
        self.settings_page.setFixedSize(
            settings_win_width, settings_win_height)

        self.settings_page.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)

        if self.settings_page.toggle:
            self.settings_page.show()
        else:
            self.settings_page.closeEvent(self.settings_page.close)
        self.settings_page.design_signal.connect(self.set_theme)

    def get_theme(self) -> int:
        if self.theme is dark:
            return 1
        elif self.theme is light:
            return 2
        return 0

    def set_theme(self, color_mode: int, bg_path: str):
        if color_mode == 0:
            self.theme = default
        elif color_mode == 1:
            self.theme = dark
        elif color_mode == 2:
            self.theme = light

        self.src_table.setRowCount(0)
        self.dst_table.setRowCount(0)
        self.bg_path = bg_path
        self.update_theme()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.save_state()
        if self.settings_page is not None:
            self.settings_page.close()
        if self.entry_window is not None:
            self.entry_window.close()

    def moveEvent(self, a0: QtGui.QMoveEvent):
        if self.settings_page is not None:
            self.settings_page.updatePos(
                self.pos().x() + 20, self.pos().y() + 125)

    def resizeEvent(self, event):
        self.my_height = self.frameGeometry().height()
        self.my_width = self.frameGeometry().width()

        self.update_theme()

        button_size = (self.my_width - (self.my_width % 100) - 100) / 10

        for btn in self.btns:
            if btn == self.settings_btn or btn == self.run_script_btn:
                btn.setFixedSize(button_size, button_size)
            elif btn == self.create_entry_btn:
                btn.setFixedHeight(button_size)
        icon_size = self.settings_btn.size().height() * 2 / 3
        # self.settings_btn.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.settings_btn.setIconSize(QtCore.QSize(icon_size, icon_size))

        # for entry in self.entries:
        #    entry_width = (self.frameGeometry().width() - 20)
        #    entry_height = self.entry_box.frameGeometry().height() / 5
        #    entry.setFixedSize(entry_width, entry_height)
