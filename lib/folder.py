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
        source_content = self.get_source_content()
        target_content = self.get_target_content()
        s = self.backslashes(self.source_dir)
        t = self.backslashes(self.target_dir)

        i = 0
        keyword_list = self.split_keywords()

        #while not (len(source_content) == 0 or i == len(source_content)):
            #if any(key in source_content[i] for key in keyword_list) or self.keywords == "":
                #print(f"move \"{s[0]}\\{source_content[i]}\" \"{s[1]}\"")
                #os.system(f"move \"{s[0]}\\{source_content[i]}\" \"{s[1]}\"")
                #target_content.append(source_content.pop(i))
            #else:
                #i += 1

        #for it in keyword_list:
        #    os.system(f"move \"{s}\\*{it}*\" \"{t}\"")
        for it in keyword_list:
            for data in glob.glob(os.path.join(self.source_dir, f"*{it}*")):
                try:
                    shutil.move(data, self.target_dir)
                except shutil.Error:
                    print(f"Error {data} already exists.")

