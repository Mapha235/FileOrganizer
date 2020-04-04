import os


class Folder:
    source_dir = ""
    target_dir = ""
    source_content = []
    target_content = []
    keyword = ""

    def __init__(self, s, t, k):
        is_source_dir = False
        self.keyword = k
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

        except OSError:
            if is_source_dir:
                print("source_dir-Directory not found.")
                return
            else:
                self.create_directory()

    def get_source_content(self):
        return self.source_content

    def get_target_content(self):
        return self.target_content

    def set_keyword(self, k):
        self.keyword = k

    def get_keyword(self):
        print(self.keyword)

    def create_directory(self):
        while 1:
            inp = input("target_dir-Directory not found. Create missing Directory? [y/n]")
            if inp == 'y':
                os.system("mkdir " + "\"" + self.target_dir + "\"")
                print("Successfully created target_dir-Directory.")
                break
            elif inp == 'n':
                print("Error: target_dir-Directory does not exist.")
                return
            else:
                continue

    # replaces the forwardslashes in source_dir and target_dir to backslashes
    def backslashes(self):
        source_dir_copy = self.source_dir.replace("/", "\\")
        target_dir_copy = self.target_dir.replace("/", "\\")
        return [source_dir_copy, target_dir_copy]

    def has_keyword(self):
        content_copy = []
        for iterator in self.source_content:
            if iterator.__contains__(self.keyword):
                content_copy.append(iterator)
                self.source_content.remove(iterator)

        return content_copy

    def move(self):
        s = self.backslashes()
        content_copy = self.has_keyword()

        for iterator in content_copy:
            print("move " + "\"" + s[0] + "\\" + iterator + "\"" + " " + s[1])
            os.system("move " + "\"" + s[0] + "\\" + iterator + "\"" + " \"" + s[1] + "\"")
            self.target_content.append(iterator)
        
        self.target_content.sort(reverse=False)
    
    

"""
- dictionary -> (word, flag) -> zip
"""
        
