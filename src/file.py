import json
from collections import namedtuple


class File():
    def __init__(self, project_root: str, color_mode, bg_path, run_in_background, enable_shortcut, replace_existing, entries):
        super().__init__()
        self.project_root = project_root
        self.color_mode = color_mode
        self.bg_path = bg_path
        self.run_in_background = run_in_background
        self.enable_shortcut = enable_shortcut
        self.entries = entries

        self.settings_dict = {}
        self.entries_dict = {}

    def read(self):
        with open(self.project_root, 'r') as file:
            self.settings_dict = json.load(file)
            # self.data = json.loads()
        self.entries_dict = self.settings_dict['entries']
        del self.settings_dict['entries']
        print(self.settings_dict)
        # print(self.data['enable-shortcut'])

        # print(self.data['entries'][0]['keywords'])

    def entryDecoder(self, obj):
        None

    def write(self, mode: str, line: str):
        None

    def update(self):
        None


def makeEntry(dict):
    if '__entry__' in dict:
        return File(dict['project_root'], dict['color_mode'],
                    dict['bg_path'], dict['run_in_background'],
                    dict['enable_shortcut'], dict['replace_existing'], 
                    dict['entries'])
    return dict


def main():
    # file = File("C:/Dev/python/FileOrganizer/data/save.json")
    # file.read()
    data = json.loads(
        '{"__entry__" : true, "project_root": "C:/Dev/python/FileOrganizer", "color_mode": 2, "bg_path": "C:/Dev/python/FileOrganizer/data/bg.jpg", "run_in_background": true, "enable_shortcut": true, "replace_existing": true, "entries": [{"id": 0,        "src": "",        "dst": "",        "keywords": [],        "isChecked": true},    {"id": 1,        "src": "",        "dst": "",        "keywords": [],        "isChecked": true}]}', object_hook=makeEntry)
    print(type(data))
    # print(data.project_root)
    # entry = makeEntry(data)
    # print(type(entry))


if __name__ == "__main__":
    main()
