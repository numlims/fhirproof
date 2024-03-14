# smallerbundles.py splits one file of json bundles in several files
# and puts them in a folder
# usage: python smallerbundles.py <fhir json file> <out folder>

import json
from pathlib import Path
import sys

import fhirhelp as fh

# main reads the json, edits and prints
def main():
    # read
    namein = sys.argv[1]
    outfolder = sys.argv[2]
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
            # remove the _Px from name before adding it, two _Px_Px crashes the upload
            a = Path(namein).stem.split("_")
            name = "_".join(a[0:len(a)-1])
            json.dump(out, open(outfolder + "/" + name + "_p" + str(nout) + ".json", "w"))
            
            nout = nout + 1
            outbundle = []

main()
