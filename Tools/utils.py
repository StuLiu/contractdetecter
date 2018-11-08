import os

# get all the name of files in the directory-"directoryPath" iteratively
# directoryPath : path of directory
# return list of strings:["name1", "name2", ... ]
def getFilesNameIteratively(directoryPath):
    root, dirs, files = os.walk(directoryPath)
    return files

def getDirOrFileName(directoryPath):
    return os.listdir(directoryPath)


# print(getDirOrFileName("./contracttest/abi"))

