"""
        ****  detect solidity source code roughly  ****
    run this script to analyze source file rougthly
    see the output in logs/detectroughly.log
    and the fault source file will store in 'tempFaultSol' directory
    @ author : liuwang
    @ school : Wuhan University
    @ date   : 2018.10.22
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

OUTPUT_DIR_DoSAttack = './tempFaultSol/DoSAttack'
if not os.path.exists(OUTPUT_DIR_DoSAttack):
    os.makedirs(OUTPUT_DIR_DoSAttack)
    doLogging('create directory {}'.format(OUTPUT_DIR_DoSAttack))

# detect call in for-loop, return 'true' if code has for loop with call
def __detectForLoapWithCall(sourceCode):
    pattern = re.compile(r'(for[ ]*?\([^\{]*?\{[^\}]*?(?:transfer|send|call)\(.*?\})', re.S)
    faults = re.findall(pattern, sourceCode)
    for fault in faults:
        doLogging(fault)
    return re.search(pattern, sourceCode) != None


def detectAllForLoapWithCall():
    doLogging('detectAllForLoapWithCall begin ......======================================')
    sols = getDirOrFileName('./contractdata/sourcecode')
    faultFiles = []
    for filename in sols:
        try:
            with open('./contracttest/sourcecode/'+filename, encoding='utf-8' ) as file:
                sourcecode = file.read()
                if __detectForLoapWithCall(sourcecode):
                    faultFiles.append(filename)
                    doLogging(filename)
        except Exception:
            pass
    doLogging('detectAllForLoapWithCall finish !!!!!======================================')
    for filename in faultFiles:
        shutil.copyfile('./contracttest/sourcecode/' + filename,
                        os.path.join(OUTPUT_DIR_DoSAttack, filename))
    return faultFiles

if __name__ == '__main__':
    print(detectAllForLoapWithCall())