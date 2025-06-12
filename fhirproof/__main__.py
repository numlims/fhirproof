
import sys
from fhirproof import fhirproof
import argparse
# parseargs parses command line arguments
def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("what", help="observation|specimen")
    parser.add_argument("dir", help="read fhir jsons from this dir")
    parser.add_argument("--db", help="a database target for db.ini file")
    parser.add_argument("--user", help="a fhir-user")
    parser.add_argument("--config", help="a fhirproof config") # action="store_true" if true/false value
    parser.add_argument("--print-config", help="print template config yml", action="store_true")
    parser.add_argument("--log", help="a logfile")
    parser.add_argument("--pamm", help="the path to the pamm")
    args = parser.parse_args()
    return args
# main runs fhirproof
def main():

    # get command line arguments
    args = parseargs()

    # get config
    # config = getconfig(args.config) # oder so

    # init fhirproof
    fp = fhirproof(args.db, args.user, args.log, args.config, pamm=args.pamm)

    # run for specimen
    if args.what == "specimen":
      # run fhirproof
      # ok = fp.run()
      ok = fp.check_specimens(args.dir)
    elif args.what == "observation":
      ok = fp.check_observations(args.dir)
    
    if ok:
        print("ok")
    else:
        print("error")

sys.exit(main())
