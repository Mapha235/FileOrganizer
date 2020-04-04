import os


class Folder:
    source_dir = ""
    target_dir = ""
    source_content = []
    target_content = []
    keywords = ""

    def __init__(self, s, t, k):
        is_source_dir = False
        self.keywords = k
        try:
            self.source_dir = s
            is_source_dir = True
            os.chdir(self.source_dir)

            # listdir sorts its content by ascii-value
            self.source_content = os.listdir(s)

            self.target_dir = t
            is_source_dir = False
            os.chdir(self.target_dir)

            self.target_content = os.listdir(t)
            keywords = self.split_keywords()

        except OSError:
            if is_source_dir:
                print("Source-Directory not found.")
                return
            else:
                self.create_directory()

    def get_source_content(self):
        return self.source_content

    def get_target_content(self):
        return self.target_content

    def set_keywords(self, k):
        self.keywords = k
        keywords = self.split_keywords()

    def get_keywords(self):
        print(self.keywords)

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
        print(keywords)
        return keywords


    # replaces the forwardslashes in source_dir and target_dir to backslashes
    def backslashes(self):
        source_dir_copy = self.source_dir.replace("/", "\\")
        target_dir_copy = self.target_dir.replace("/", "\\")
        return [source_dir_copy, target_dir_copy]


    def move(self):
        s = self.backslashes()
        i = 0
        while 1:
            if self.source_content[i].__contains__(self.keywords) or self.keywords == "":
                print(f"move \"{s[0]}\\{self.source_content[i]}\" \"{s[1]}\"")
                os.system(f"move \"{s[0]}\\{self.source_content[i]}\" \"{s[1]}\"")
                self.target_content.append(self.source_content.pop(i))
            else:
                i += 1

            if len(self.source_content) == 0 or i == len(self.source_content):
                break


    

"""
- dictionary -> (word, flag) -> zip
"""
        
