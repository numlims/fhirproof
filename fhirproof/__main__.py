# automatically generated, DON'T EDIT. please edit main.ct from where this file stems.

import sys
from fhirproof import fhirproof
import argparse
import os.path
# parseargs parses command line arguments
def parseargs():
    """
     parseargs parst die command line argumente.
     
     fhirproof nimmt target und user ohne name, und die config datei, eine
     option die konfig stub zu printen und das log file.
    """
    parser = argparse.ArgumentParser()
    # parser.add_argument("what", help="observation|specimen")
    parser.add_argument("dir", help="read fhir jsons from this dir")
    parser.add_argument("--db", help="a database target for db.ini file")
    parser.add_argument("--user", help="a fhir-user")
    parser.add_argument("--config", help="a fhirproof config") # action="store_true" if true/false value
    parser.add_argument("--print-config", help="print template config yml", action="store_true")
    parser.add_argument("--log", help="a logfile")
    parser.add_argument("--settings", help="path to the settings yaml")
    parser.add_argument("-e", help="file encoding")
    args = parser.parse_args()
    return args
# main runs fhirproof
def main():
    """
     main reads the commandline arguments and starts fhirproof.
    """
    args = parseargs()
    #try:
    fp = fhirproof(args.db, args.user, args.log, configpath=args.config)
    #except Exception:
    #    return
    ok = fp.check(args.dir, args.e)
    if ok is True:
        print("fhirproof: ok")
        return 0
    else:
        print("fhirproof: not ok")
        return 1

sys.exit(main())
