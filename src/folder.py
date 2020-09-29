import os
import glob
import shutil
from exception import FilenameAlreadyExistsError


class Folder:

    def __init__(self, src, dst, keyw):
        is_src_dir = False
        self.keywords = keyw
        self.replaceEnabled = False

        try:
            self.src_dir = src
            is_src_dir = True
            os.chdir(self.src_dir)

            self.dst_dir = dst
            is_src_dir = False
            os.chdir(self.dst_dir)

        except OSError:
            if is_src_dir:
                print("Source-Directory not found.")
            else:
                self.createDirectory()

    def getSrcDir(self):
        return self.src_dir

    def getDstDir(self):
        return self.dst_dir

    def getSrcContent(self):
        lst = list(os.walk(self.src_dir))[0][:]
        lst = list(lst[1:3])
        return lst

    def getDstContent(self):
        lst = list(os.walk(self.dst_dir))[0][:]
        lst = list(lst[1:3])
        return lst

    def setKeywords(self, k):
        self.keywords = k

    def getKeywords(self):
        return self.keywords

    def setOption(self, val: bool):
        self.replaceEnabled = val

    def createDirectory(self):
        while 1:
            inp = input(
                "Destination-Directory not found. Create missing Directory? [y/n]")
            if inp == 'y':
                os.system("mkdir " + "\"" + self.dst_dir + "\"")
                print("Successfully created Destination-Directory.")
                break
            elif inp == 'n':
                print("Error: Destination-Directory does not exist.")
                return
            else:
                continue

    def splitKeywords(self):
        keywords = self.keywords.split("//")
        return keywords

    # replaces the forwardslashes in src_dir and dst_dir to backslashes
    def backslashes(self, path: str):
        return path.replace("/", "\\")

    def move(self, isReverse=False):
        if isReverse:
            src_dir = self.dst_dir
            dst_dir = self.src_dir
        else:
            src_dir = self.src_dir
            dst_dir = self.dst_dir

        keyword_list = self.splitKeywords()
        self.files = [file for file in os.listdir(
            src_dir) if os.path.isfile(os.path.join(src_dir, file))]
        files_moved = 0
        for it in keyword_list:
            matching_files = [file for file in self.files if it in file]
            # matching_files = [os.path.join(src_dir, file) for file in matching_files]
            files_moved += len(matching_files)

            for data in matching_files:
                try:
                    dst = f"{dst_dir}/{data}"
                    if not self.replaceEnabled and os.path.isfile(dst):
                        raise FilenameAlreadyExistsError
                    elif not os.path.isfile(dst):
                        shutil.copyfile(f"{src_dir}/{data}", f"{dst_dir}/{data}")
                except FilenameAlreadyExistsError:
                    file = data.split('.')
                    os.replace(os.path.join(src_dir, data),
                               os.path.join(src_dir, f"{file[0]} - moved.{file[1]}"))
                    file_index = self.files.index(data)
                    data = f"{file[0]} - moved.{file[1]}"
                    self.files[file_index] = data
                    matching_files.append(data)
                
        return files_moved

    def remove(self, isReverse=False):
        queue = []
        keyword_list = self.splitKeywords()

        if isReverse:
            src_dir = self.dst_dir
        else:
            src_dir = self.src_dir

        for it in keyword_list:
            matching_files = [file for file in self.files if it in file]
            matching_files = [os.path.join(src_dir, file)
                              for file in matching_files]
            for data in matching_files:
                try:
                    os.unlink(data)
                except PermissionError:
                    queue.append(data)
                except FileNotFoundError:
                    None
        self.files.clear()
        while len(queue) != 0:
            for entry in queue:
                try:
                    os.unlink(entry)
                except shutil.Error as e:
                    print(f"Fail: {e}")
                except PermissionError as e:
                    None
                except FileNotFoundError:
                    queue.pop()
