
import re

targetString = '中华人名共和国人均GDP在1.4-1.6万元之间，而美国是6.5-7万元之间'
msgs = re.findall(r'(\d+\.\d+?-\d+\.\d万元|\d+\.\d+?-\d万元)', targetString)
print(msgs)