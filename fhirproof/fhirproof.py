# this file is generated automatically, please edit the .ct file from which it stems.


import json

from dig import *
from AqtMatCheck import *
from PrimaryInDbCheck import *
from DatesCheck import *
from LocationCheck import *
from BehealterCheck import *
from OUCheck import *
from ParentingCheck import *
from PsnCheck import *
from RestmengeCheck import *
from DerivmatCheck import *
from MayUserEditOUCheck import *
from fhirhelp import fhirhelp as fh
import logging
import sys
from traction import *
import argparse



# Fhirproof reads fhir json from stdin and checks the entries
class Fhirproof:

    # these variables are accessible to the fhirchecks
    entrybyfhirid = {} # entries referenced by fullUrl / fhirids, e.g. "Specimen/1037700"
    entrybysampleid = {} # entries referenced by sampleid
    shouldzerorest = {} # should restmenge be zero
    aqtgchildless = {} # is a aliquotgroup without children?


    # parent returns the entry's parent entry resource, if there is one, else none
    def parent(self, entry):
        parent = None
        resource = entry['resource']
        if fh.type(resource) != "DERIVED":              
            return None
        # get fhirid of aliquotgroup-parent
        pfhirid = fh.parent_fhirid(resource)
        if pfhirid == None:
            return None
        elif pfhirid not in self.entrybyfhirid:
            return None
        return self.entrybyfhirid[pfhirid]['resource']



    def _setuplog(self, logdir):
        # setup a logger to write to a file into logs folder
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        # log to file
        if logdir == "":
            # logdir = Path.joinpath(Path(__file__).parent.parent, 'logs/')
            logdir = "../logs"
        # file_handler = logging.FileHandler(Path.joinpath(logdir, 'fhirproof.log'))
        file_handler = logging.FileHandler(logdir + "/fhirproof.log")
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # log to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        log.addHandler(stdout_handler)
        self.log = log


    # init inits fhirproof with db target, input file, centraxx user, log dir and config
    def __init__(self, target, file, user, logdir, config=None):

        self.target = target
        # connect to db
        self.db = dbcq(target)
        # traction for queries
        self.tr = traction(self.db)

        # sys.stdin works on powershell
        textin = ""         # maybe use textin = open(0).read()
        for line in file:
            textin += line

        # the other args
        self.textin = textin
        self.user = user
        self.logdir = logdir
        
        # is the input ready for centraxx import?
        self.ok = True


    # init may not return anything, so run function
    def run(self):
        user = self.user
        logdir = self.logdir
        textin = self.textin

        #jsonin = DictPath(json.loads(textin))
        jsonin = json.loads(textin)

        if logdir == None:
            logdir = ""

        self._setuplog(logdir)
        self.log.info(f"starting against {self.target}")


        # initialize checks
        aqtmat = AqtMatCheck(self)
        primary_in_db = PrimaryInDbCheck(self)
        dates = DatesCheck(self)
        location = LocationCheck(self)
        behealter = BehealterCheck(self)
        ou = OUCheck(self)
        parenting = ParentingCheck(self)
        psn = PsnCheck(self)
        restmenge = RestmengeCheck(self)
        derivmat = DerivmatCheck(self)
        mayeditou = MayUserEditOUCheck(self)

        # count for some stats
        aqtg_count = 0
        master_count = 0
        derived_count = 0


        # run checks
        for entry in dig(jsonin, "entry"):
            #print(f"type(entry): {type(entry)}")
            # keep arrays up to date
            self.entrybyfhirid[dig(entry, "fullUrl")] = entry

            if fh.type(dig(entry, 'resource')) == "ALIQUOTGROUP":
                aqtg_count += 1
                if not dig(entry, "fullUrl") in self.aqtgchildless: # tmp way to prohibit overwrites
                    self.aqtgchildless[dig(entry, "fullUrl")] = True
                aqtmat.check(entry)

            # print(f"entry resource: {json.dumps(dig(entry, 'resource'))}")
            sampleid = fh.sampleid(dig(entry, 'resource'))
            if sampleid == None:
                continue

            self.entrybysampleid[sampleid] = entry
            if fh.type(dig(entry, 'resource')) == "DERIVED":
                derived_count += 1
            if fh.type(dig(entry, 'resource')) == "MASTER":
                master_count += 1
            # primary in db
            primary_in_db.check(entry)
            # dates
            dates.check(entry)
            # location
            location.check(entry)
            # behealter
            behealter.check(entry)
            # org
            ou.check(entry)
            # parenting
            parenting.check(entry)
            # psn
            psn.check(entry)
            # restmenge
            restmenge.check(entry)
            # derived material
            derivmat.check(entry)
            # edit oe?
            # mayeditou.check(entry, user)




        restmenge.end()
        parenting.end()
        self.log.info(f"ended against {self.target}: "+
            str(aqtg_count) + " aliquot groups, " +
            str(master_count) + " master samples, " +
            str(derived_count) + " derived samples, " +
            str(len(jsonin['entry'])) + " total\n" )
        
        return self.ok # written by FhirCheck.err()




  

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
    fp = Fhirproof(args.target, sys.stdin, args.user, args.log_dir, args.config)

    # run fhirproof
    ok = fp.run()
    
    if ok:
        print("ok")
    else:
        print("error")



if __name__ == "__main__":
    main()

