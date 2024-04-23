# orgtoct: convert org to codetext
# usage: cat myprogram.org | python orgtoct.py 

import sys
import re

# we are not in source
insrc = False

for line in sys.stdin:
    # we encounter a source block
    # replace #+begin_src lang with <<
    if re.match(r"^#\+begin_src", line):
        insrc = True
        # remove << and >>= surrounding name
        line = re.sub(r"<<", "", line)
        line = re.sub(r">>=", "", line)
        # replace the begin source with <<
        line = re.sub(r"^#\+begin_src \w+ ", "<<", line) # \w+: programming lang
    # replace the end source with >>
    if re.match(r"^#\+end_src", line):
        insrc = False
        line = re.sub(r"^#\+end_src", ">>", line)
    
    # if in source, we remove the two leading blanks org-mode adds
    if insrc:
        line = re.sub(r"^  ", "", line)
    
    print(line, end="")
    
