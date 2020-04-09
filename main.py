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
    - linux support(?)
    - If schleifen in eventFilter verbessern
    - regular expressions einbauen
    - wenn möglich eventFilter mit connect ersetzen
    
    - if 2 entries have the same source directory, the program crashes eventually
    
    - after clicking run_script_button with multiple entries(>1) that all have no keyword, the program crashes
    
  3 - anzahl dateien verschoben anzeigen
    - zu verschiebene Datei existiert schon im target folder(?)
    
    - mögliche Konflikte:
        - File im Source existiert schon im target
        - k > 2 keywords stehen im Konflikt (z.B. *2//8 -> 82.txt)
        - mehr als 2 Entries haben gleichen Source und versch. Targets und überschneidende Keywords -> datei kopieren
        
        - allg. Lösung: neues Fenster mit entsprechenden Fehlermeldungen und evtl. Fixes
"""


def makeScrollable(widget):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    return scroll


def shorten_path(path_name, length):
    counter = 0
    shortened_path_name = ""

    for i in reversed(path_name):
        if counter >= 2:
            break
        elif i == '/':
            counter += 1
        shortened_path_name += i

    shortened_path_name = shortened_path_name[::-1]
    l = len(shortened_path_name)
    if l >= length:
        k = l - 1 - length
        shortened_path_name = shortened_path_name[k:l - 1]

    if l >= 1 and shortened_path_name[1] == ":":
        return shortened_path_name

    return "..." + shortened_path_name


def read_file():
    file = open("./data/save.txt", "r")
    values = []
    for i in file:
        temp = i.split(",")
        temp.pop()
        values.append(temp)
    return values


def main():
    app = QApplication(sys.argv)
    win = TheWindow(read_file())

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
