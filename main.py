from stylesheets import *
from app import *

"""
TODO:
  5 - Multithreading einbauen
  ? - entrywindow offen lassen bei NO
    - Ausnahme-keywords einbauen
  6 - savefile
      - einstellungen 
  4 - settings
        - display on hover-button/label in entrywindow -> explain ausnahmekeyword oder FAQ in settings
        - custom hintergrund
        - light/dark mode
        - sprachen
        - slider zum einstellen der transparenz
        - Duplikat im Target ersetzen/nicht ersetzen/selbst entscheiden? /-Y == enable confirmation prompt
    - linux support(?)
    - If schleifen in eventFilter verbessern
    - regular expressions einbauen
    - wenn möglich eventFilter mit connect ersetzen
    
    - if 2 entries have the same source directory, the program crashes eventually
    
    - after clicking run_script_button with multiple entries(>1) that all have no keyword, the program crashes
    
    - zu verschiebene Datei existiert schon im target folder -> wird ersetzt
    
    - mögliche Konflikte:   
        - File im Source existiert schon im target
        - k > 2 keywords stehen im Konflikt (z.B. *2//8 -> 82.txt)
        - mehr als 2 Entries haben gleichen Source und versch. Targets und überschneidende Keywords -> datei kopieren
        
        - allg. Lösung: neues Fenster mit entsprechenden Fehlermeldungen und evtl. Fixes
    - Optimierung;
        - os.scandir() statt os.listdir() in folder.py
"""


def makeScrollable(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    return scroll


def shorten_path(path_name, length):
    shortened_path_name = ""

    folders = path_name.split('/')
    # folder_num limits the number of folders that are displayed
    folder_num = int(length / 10)
    start = len(folders) - folder_num
    if folder_num > start:
        start = 0

    folders = folders[start:len(folders)]

    for f in folders:
        slash = '/'
        # this condition is only met when f equals the path-letter (such as C:). This way the
        # shortened_path_name does not have a slash as its first character
        if f[1] == ':':
            slash = ''
        shortened_path_name = shortened_path_name + slash + f

    if len(shortened_path_name) >= 1 and shortened_path_name[1] == ':':
        return shortened_path_name

    return "..." + shortened_path_name


def read_file():
    file = open("./data/save.txt", "r")
    values = []
    for i in file:
        temp = i.split(',')
        temp.pop()
        values.append(temp)
    return values


def main():
    app = QApplication(sys.argv)
    win = TheWindow(read_file())

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
