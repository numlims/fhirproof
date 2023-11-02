# fhirproof: fhir import checker

# fhirproof checkt, ob FHIR Json Dateien ins Centraxx importiert werden
# können und loggt in `logs/fhirproof.log`.

import json
import logging
from pathlib import Path
import sys

from AqtMatCheck import *
from PrimaryInDbCheck import *
from DatesCheck import *
from LocationCheck import *
from BehealterCheck import *
from OrgCheck import *
from ParentingCheck import *
from PsnCheck import *
from RestmengeCheck import *
from DerivmatCheck import *

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

    def _setuplog(self):
        # setup a logger to write to a file into logs folder
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        # log to file
        file_handler = logging.FileHandler( Path.joinpath(Path(__file__).parent.parent, 'logs/fhirproof.log'))
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # log to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        log.addHandler(stdout_handler)
        self.log = log
    
    def __init__(self):
        #print("hello fhirproof")
        #self.fruit = "apple"
        #print("self.fruit: " + self.fruit)

        self._setuplog()

        # read
        namein = sys.argv[1]
        filein = open(namein)
        textin = filein.read()

        jsonin = json.loads(textin)

        # initialize checks
        aqtmat = AqtMatCheck(self)
        primary_in_db = PrimaryInDbCheck(self)
        dates = DatesCheck(self)
        location = LocationCheck(self)
        behealter = BehealterCheck(self)
        org = OrgCheck(self)
        parenting = ParentingCheck(self)
        psn = PsnCheck(self)
        restmenge = RestmengeCheck(self)
        derivmat = DerivmatCheck(self)

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
                self.aqtgchildless[entry["fullUrl"]] = True
                aqtmat.check(entry)

            sampleid = fh.sampleid(entry['resource'])
            if sampleid == None:
                continue

            self.entrybysampleid[sampleid] = entry
            
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
            org.check(entry)
            #<parenting>>
            parenting.check(entry)
            #<psn>>
            psn.check(entry)
            # restmenge
            restmenge.check(entry)
            # derived material
            derivmat.check(entry)

        restmenge.end()
        parenting.end()

# main runs fhirproof
def main():
    Fhirproof()

main()
