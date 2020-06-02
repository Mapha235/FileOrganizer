import os, glob, shutil


class Folder:
    src_dir = ""
    dst_dir = ""

    keywords = ""

    def __init__(self, s, t, k):
        is_src_dir = False
        self.keywords = k
        try:
            self.src_dir = s
            is_src_dir = True
            os.chdir(self.src_dir)

            self.dst_dir = t
            is_src_dir = False
            os.chdir(self.dst_dir)

        except OSError:
            if is_src_dir:
                print("Source-Directory not found.")
                return
            else:
                self.create_directory()

    def get_src_dir(self):
        return self.src_dir

    def get_dst_dir(self):
        return self.dst_dir

    def get_src_content(self):
        return os.listdir(self.src_dir)

    def get_dst_content(self):
        return os.listdir(self.dst_dir)

    def set_keywords(self, k):
        self.keywords = k

    def get_keywords(self):
        return self.keywords

    def create_directory(self):
        while 1:
            inp = input("Destination-Directory not found. Create missing Directory? [y/n]")
            if inp == 'y':
                os.system("mkdir " + "\"" + self.dst_dir + "\"")
                print("Successfully created Destination-Directory.")
                break
            elif inp == 'n':
                print("Error: Destination-Directory does not exist.")
                return
            else:
                continue

    def split_keywords(self):
        keywords = self.keywords.split("//")
        return keywords

    # replaces the forwardslashes in src_dir and dst_dir to backslashes
    def backslashes(self, path:str):
        return path.replace("/", "\\")

    def move(self):
        keyword_list = self.split_keywords()

        for it in keyword_list:
            for data in glob.glob(os.path.join(self.src_dir, f"*{it}*")):
                try:
                    shutil.copy(data, self.dst_dir)
                except shutil.Error:
                    print(f"Error {data} already exists.")

    def remove(self):
        keyword_list = self.split_keywords()

        for it in keyword_list:
            for data in glob.glob(os.path.join(self.src_dir, f"*{it}*")):
                try:
                    os.unlink(data)
                except shutil.Error as e:
                    print(f"Fail: {e}")
