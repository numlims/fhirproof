# smallerbundles.py splits one file of json bundles in several files

import json
from pathlib import Path
import sys

import fhirhelp as fh

# main reads the json, edits and prints
def main():
    # read
    namein = sys.argv[1]
    filein = open(namein)
    textin = filein.read()

    jsonin = json.loads(textin)

    outbundle = []

    size = 20
    nout = 0
    for i, val in enumerate(jsonin['entry']):
        outbundle.append(jsonin['entry'][i])
        if i % size == 0 or i == len(jsonin['entry'])-1:
            out = {
                "resourceType": "Bundle",
                "type": "transaction",
                "entry": outbundle
            }
            print(len(outbundle))
            json.dump(out, open("out/" + Path(namein).stem + "_p" + str(nout) + ".json", "w"))
            
            nout = nout + 1
            outbundle = []

main()
