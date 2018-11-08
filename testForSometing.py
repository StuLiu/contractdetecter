
import re

targetString = '中华人名共和国人均GDP在1.4-1.6万元之间，而美国是6.5-7万元之间'
msgs = re.findall(r'(\d+\.\d+?-\d+\.\d万元|\d+\.\d+?-\d万元)', targetString)
print(msgs)


from pathlib import Path
import os
SOURCECODE_DIR = "./contractdata/sourcecode/"
print(Path(SOURCECODE_DIR),Path(SOURCECODE_DIR).exists())
print(os.path.normpath(SOURCECODE_DIR), os.path.exists(os.path.normpath(SOURCECODE_DIR)))
print(os.path.abspath(SOURCECODE_DIR), os.path.exists(os.path.abspath(SOURCECODE_DIR)))