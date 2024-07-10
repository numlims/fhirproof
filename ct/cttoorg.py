# cttoorg: convert codetext-format to org-format
# usage: cat myprogram.tag | python cttoorg.py <lang of prog>

import sys
import re

# temp: pass the programming language as argument
lang = sys.argv[1]

# we are not in source
insrc = False

for line in sys.stdin:
    # we encounter a source block
    if not insrc and re.match(r"^<<", line):
        # replace the << with the #+begin_src 
        line = re.sub(r"^<<", f"#+begin_src {lang} ", line)
        insrc = True
        # avoid adding leading blanks to this line
        print(line, end="")
        continue
    # we leave a src block
    if insrc and re.match("^>>$", line):
        insrc = False
        # replace the >> with the #+end_src
        line = "#+end_src\n"
        
    # put in leading blanks in src
    if insrc:
        print("  " + line, end="")
    else:
        print(line, end="")
    
