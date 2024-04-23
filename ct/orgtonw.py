# orgtonw converts an org file (or ft file) to a nw file.
# reimplementation of org2nw and rm-org-indent.awk for non-posix environment.
# usage: cat program.org | python orgtonw.py | python tangle.py

# supports #+begin_src/#+end_src and #+b/#+e tags.

# supports ft

import sys
import re

insrc = False # are we in a source block

# read the file
for line in sys.stdin:
    if re.match(r"#\+begin_src \S+\s+", line) or re.match(r"#\+b \S+\s+", line) or re.match(r"^#>", line):
        # we're in source
        insrc = True 
        # remove the begin_src stuff, keep the <<chunkname>>= stuff
        line = re.sub(r"#\+begin_src \S+\s+", "", line)
        # remove the begin_src shorthand #+b
        line = re.sub(r"#\+b \S+\s+", "", line)
        # remove ft tag
        if re.match(r"^#>", line):
            line = re.sub(r"^#>\s+", "", line)
            # if language suffix given, remove it
            if re.match(r"^\.\w+", line):
                line = re.sub(r"^\.\w+", "", line)
            # if no name is given, add .
            if re.match(r"^\s*$", line):
                line = ".\n"
        # add << >>= if missing (for ft and org)
        if not re.match(r"<<.*>>=", line):
            line = "<<" + line[0:len(line)-1] + ">>=\n" # the substring cuts off the \n at the end of the line
    elif re.match(r"#\+end_src", line) or re.match(r"#\+e$", line) or re.match(r"#\+e\s+", line) or re.match(r"^<#\n$", line): # todo the two #\+e regexes as one
        # we're not in source anymore
        insrc = False
        # @ marks the beginning of doku
        line = "@\n" # linebreak necessary so that only @ is on line

    # if in source, we remove the two leading blanks org-mode adds
    if insrc:
        line = re.sub(r"^  ", "", line)

    # we print the line
    print(line, end="")
    
