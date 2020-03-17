import os



class Folder:
    source = ""                 #Quellpfad
    target = ""                 #Zielpfad
    source_content = []         #Inhalt von Quellpfad
    keyword = ""


    def __init__(self, s, t):
        is_source = False
        try:
            self.source = s
            is_source = True
            os.chdir(self.source)

            # listdir sorts its content by ascii-value
            self.source_content = os.listdir(os.getcwd())

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

    #replaces the forwardslashes in source and target to backslashes
    def backslashes(self):
        source_copy = self.source.replace("/" , "\\")
        target_copy = self.target.replace("/" , "\\")
        return [source_copy, target_copy]



    def move(self):
        s = self.backslashes()
        for iterator in self.source_content:
            if iterator.__contains__(self.keyword):
                print("move " + "\"" + s[0] + "\\" + iterator + "\"" + " " + s[1])
                os.system("move " + "\"" + s[0] + "\\" + iterator + "\"" + " \"" + s[1] + "\"")


