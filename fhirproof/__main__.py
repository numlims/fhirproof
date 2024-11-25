
import sys
from fhirproof import fhirproof
import argparse


# parseargs parses command line arguments
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="a database target for db.ini file")
    parser.add_argument("user", help="a fhir-user")
    parser.add_argument("--config", help="a fhirproof config") # action="store_true" if true/false value
    parser.add_argument("--print-config", help="print template config yml", action="store_true")
    parser.add_argument("--log-dir", help="a directory of the fhirproof log")
    args = parser.parse_args()
    return args


# main runs fhirproof
def main():

    # get command line arguments
    args = parseargs()

    # get config
    # config = getconfig(args.config) # oder so

    # init fhirproof
    fp = fhirproof(args.target, sys.stdin, args.user, args.log_dir, args.config)

    # run fhirproof
    ok = fp.run()
    
    if ok:
        print("ok")
    else:
        print("error")



sys.exit(main())

