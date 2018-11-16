"""
        ****  detect solidity source code roughly  ****
    run this script to analyze source file rougthly
    see the output in logs/detectroughly.log
    and the fault source file will store in 'tempFaultSol' directory
    @ author : liuwang
    @ school : Wuhan University
    @ date   : 2018.11.8
"""

import re
import os
import shutil
from Tools.utils import getDirOrFileName
import logging
# config log file

logging.basicConfig(level=logging.INFO, filename='./logs/detectroughly.log',
                    format = '%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')
# print msg in console and log file
def doLogging(msg):
    print(msg)
    logging.info(msg)
    pass

SOURCECODE_DIR = './contractdata/sourcecode'
# SOURCECODE_DIR = './contracttest/sourcecode'

OUTPUT_DIR_DoSAttack = './tempFaultSol/DoSAttack'
OUTPUT_DIR_UexpectedEther = './tempFaultSol/UexpectedEther'
OUTPUT_DIR_ImproperAccessControl = './tempFaultSol/ImproperAccessControl'
def __checkDirAndCreate(path):
    if not os.path.exists(path):
        os.makedirs(path)
        doLogging('create directory {}'.format(path))
OUTPUT_DIRS = [OUTPUT_DIR_DoSAttack, OUTPUT_DIR_UexpectedEther, OUTPUT_DIR_ImproperAccessControl]
for dir in OUTPUT_DIRS:
    __checkDirAndCreate(dir)

# detect call in for-loop, return 'true' if code has for loop with checked call
def __detectForLoapWithCall(sourceCode):
    pattern = re.compile(r'(for[ ]*?\([^\{]*?\{[^\}]*?(?:transfer|(?:require|assert)\([^\)]*?(?:send|call\..*?))\(.*?\})', re.S)
    faults = re.findall(pattern, sourceCode)
    for fault in faults:
        doLogging('Code here may be Error:\n\t' + fault)
    return len(faults) > 0

# detect call in for-loop, return 'true' if code has for loop with checked call
def __detectUexpectedEther(sourceCode):
    pattern = re.compile(r'((?:(?:require|assert|if)\([^\)]*?(?:this\.|address\(this\)\.)balance[^\)]*?[><=]{1,}[^\)]*?\)|'
                         r'(?:require|assert|if)\([^\)]*?[><=]{1,}[^\)]*?(?:this\.|address\(this\)\.)balance.*?\)))', re.S)
    faults = re.findall(pattern, sourceCode)
    for fault in faults:
        doLogging('Code here may be Error:\n\t' + fault)
    return len(faults) > 0

def detectAllForLoapWithCall():
    doLogging('detectAllForLoapWithCall begin ......======================================')
    sols = getDirOrFileName(SOURCECODE_DIR)
    faultFiles = []
    print(len(sols))
    for filename in sols:
        try:
            with open(os.path.join(SOURCECODE_DIR, filename), encoding='utf-8' ) as file:
                sourcecode = file.read()
                if __detectForLoapWithCall(sourcecode):
                    faultFiles.append(filename)
                    doLogging(filename)
        except Exception:
            pass
    doLogging('detectAllForLoapWithCall finish !!!!!======================================')
    for filename in faultFiles:
        shutil.copyfile(os.path.join(SOURCECODE_DIR, filename),
                        os.path.join(OUTPUT_DIR_DoSAttack, filename))
    return faultFiles

def detectAllUexpectedEther():
    doLogging('detectAllUexpectedEther begin ......======================================')
    sols = getDirOrFileName(SOURCECODE_DIR)
    faultFiles = []
    print(len(sols))
    for filename in sols:
        try:
            with open(os.path.join(SOURCECODE_DIR, filename), encoding='utf-8' ) as file:
                sourcecode = file.read()
                if __detectUexpectedEther(sourcecode):
                    faultFiles.append(filename)
                    doLogging(filename)
        except Exception:
            pass
    doLogging('detectAllUexpectedEther finish !!!!!======================================')
    for filename in faultFiles:
        shutil.copyfile(os.path.join(SOURCECODE_DIR, filename),
                        os.path.join(OUTPUT_DIR_UexpectedEther, filename))
    return faultFiles


if __name__ == '__main__':
    # doLogging(detectAllForLoapWithCall())
    doLogging(detectAllUexpectedEther())