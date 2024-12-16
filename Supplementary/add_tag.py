# replace (set-logic QF_NRA) to (set-logic OMT_QF_NRA) to the top of the SMT file

import sys
import re
import os

def add_tag(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    with open(file_name, 'w') as f:
        for line in lines:
            if re.match(r'\(set-logic QF_NRA\)', line):
                f.write('(set-logic OMT_QF_NRA)\n')
            else:
                f.write(line)

if __name__ == '__main__':
    # traverse the directory
    for root, dirs, files in os.walk(sys.argv[1]):
        for file in files:
            if file.endswith('.smt2'):
                add_tag(os.path.join(root, file))