import os


class Folder:
    source = ""
    target = ""
    source_content = []
    keyword = ""

    def __init__(self, s, t):
        is_source = False
        try:
            self.source = s
            is_source = True
            os.chdir(self.source)

            # listdir sorts its content by ascii-value
            self.source_content = os.listdir(os.getcwd())
            self.my_print()

            self.target = t
            is_source = False
            os.chdir(self.target)

        except OSError:
            if is_source:
                print("Source-Directory not found.")
                return
            else:
                self.create_directory()

    def my_print(self):
        for i in self.source_content:
            print(i)

    def set_keyword(self, k):
        self.keyword = k

    def create_directory(self):
        while 1:
            inp = input("Target-Directory not found. Create missing Directory? [y/n]")
            if inp == 'y':
                os.system("mkdir " + "\"" + self.target + "\"")
                print("Successfully created Target-Directory.")
                break
            elif inp == 'n':
                print("Error: Target-Directory does not exist.")
                return
            else:
                continue
