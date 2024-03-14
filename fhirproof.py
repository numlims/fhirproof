# fhirproof: fhir import checker

# usage: fhirproof.py <file name> <user name> <log dir>

# fhirproof checkt, ob FHIR Json Dateien ins Centraxx importiert werden
# können und loggt in `logs/fhirproof.log`.

import json
import logging
from pathlib import Path
import sys
import fhirhelp as fh

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

from traction import *

# Fhirproof reads fhir json from stdin and checks the entries
class Fhirproof:

    # these variables are accessible to the fhirchecks
    entrybyfhirid = {} # entries referenced by fullUrl / fhirids, e.g. "Specimen/1037700"
    entrybysampleid = {} # entries referenced by sampleid
    shouldzerorest = {} # should restmenge be zero
    aqtgchildless = {} # is a aliquotgroup without children?

    # these functions are accessible by the fhirchecks
    
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
    
    def __init__(self, target, file, user, logdir):

        self.target = target
        self.db = dbcq(target)
        self.tr = traction(self.db)

        # sys.stdin works on powershell
        textin = ""
        for line in file:
            textin += line

        self.textin = textin
        self.user = user
        self.logdir = logdir
        self.ok = True

    # init may not return anything, so run function
    def run(self):
        user = self.user
        logdir = self.logdir
        textin = self.textin

        # print("textin: " + textin)
        
        #print("hello fhirproof")
        #self.fruit = "apple"
        #print("self.fruit: " + self.fruit)


        # print("textin: " + textin)
        # print("after textin print")

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
        for entry in jsonin["entry"]:
            # keep arrays up to date
            self.entrybyfhirid[entry["fullUrl"]] = entry

            ## aliquote checks
            
            """
            Für Aliquotgruppen gibt es keine Sampleid. Weil wir für relativ viele
            Checks die `sampleid` benutzen, gehen wir zum nächsten Check, wenn es
            im Json keine Sampleid gibt. Aliquotgruppen haben keine Sampleid, ihre
            Checks machen wir bevor wir weiter gehen.
            """
            if fh.type(entry['resource']) == "ALIQUOTGROUP":
                aqtg_count += 1
                if not entry["fullUrl"] in self.aqtgchildless: # tmp way to prohibit overwrites
                    self.aqtgchildless[entry["fullUrl"]] = True
                aqtmat.check(entry)

            sampleid = fh.sampleid(entry['resource'])
            if sampleid == None:
                continue

            self.entrybysampleid[sampleid] = entry

            if fh.type(entry['resource']) == "DERIVED":
                derived_count += 1
            if fh.type(entry['resource']) == "MASTER":
                master_count += 1
            
            ## non-aliquote checks
            
            #<primary in db>>
            primary_in_db.check(entry)
            #<dates>>
            dates.check(entry)
            #<location>>
            location.check(entry)
            #<behealter>>
            behealter.check(entry)
            #<org>>
            ou.check(entry) # todo uncomment again
            #<parenting>>
            parenting.check(entry)
            #<psn>>
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
            str(aqtg_count) + " aliquot groups\n" +
            str(master_count) + " master samples\n" +
            str(derived_count) + " derived samples\n" +
            str(len(jsonin['entry'])) + " total\n" )
        
        return self.ok # written by FhirCheck.err()


# main runs fhirproof
def main():
    if len(sys.argv) < 4:
        print("usage: fhirproof.py <db target> <file name> <user name> [<log dir>]")
        return

    target = sys.argv[1] # db target

    # read
    # on powershell, there seem to be file-conversion issues with this
    # namein = sys.argv[1]
    # filein = open(namein)
    # textin = filein.read()
    
    # name of fhir user
    user = sys.argv[3]

    logdir = None
    # optional log dir, todo maybe do --log-dir mydir
    if len(sys.argv) == 5:
        logdir = sys.argv[4]

    fp = Fhirproof(target, sys.stdin, user, logdir)
    ok = fp.run()
    if ok:
        print("ok")
    else:
        print("error")

if __name__ == "__main__":
    main()


