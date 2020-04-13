import os, glob, shutil


class Folder:
    source_dir = ""
    target_dir = ""

    keywords = ""

    def __init__(self, s, t, k):
        is_source_dir = False
        self.keywords = k
        try:
            self.source_dir = s
            is_source_dir = True
            os.chdir(self.source_dir)

            self.target_dir = t
            is_source_dir = False
            os.chdir(self.target_dir)

        except OSError:
            if is_source_dir:
                print("Source-Directory not found.")
                return
            else:
                self.create_directory()

    def get_source_dir(self):
        return self.source_dir

    def get_target_dir(self):
        return self.target_dir

    def get_source_content(self):
        return os.listdir(self.source_dir)

    def get_target_content(self):
        return os.listdir(self.target_dir)

    def set_keywords(self, k):
        self.keywords = k

    def get_keywords(self):
        return self.keywords

    def create_directory(self):
        while 1:
            inp = input("Target-Directory not found. Create missing Directory? [y/n]")
            if inp == 'y':
                os.system("mkdir " + "\"" + self.target_dir + "\"")
                print("Successfully created Target-Directory.")
                break
            elif inp == 'n':
                print("Error: Target-Directory does not exist.")
                return
            else:
                continue

    def split_keywords(self):
        keywords = self.keywords.split("//")
        return keywords

    # replaces the forwardslashes in source_dir and target_dir to backslashes

    def backslashes(self, path: str):
        return path.replace("/", "\\")

    def move(self):
        keyword_list = self.split_keywords()

        for it in keyword_list:
            for data in glob.glob(os.path.join(self.source_dir, f"*{it}*")):
                try:
                    shutil.move(data, self.target_dir)
                except shutil.Error:
                    print(f"Error {data} already exists.")
