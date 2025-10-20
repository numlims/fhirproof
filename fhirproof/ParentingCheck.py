import re

from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
class ParentingCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        # is there a reference to a parent?
        if fh.type(resource) == "DERIVED":
        
            # is there a fhirid referencing a parent?
            pfhirid = fh.parent_fhirid(resource)
            if pfhirid == None:
                self.err(f"sample {sampleid} is a derived, but there isn't a reference to a parent.")
                # we assume that we already visited the parent, if not, message
            elif pfhirid not in self.fp.entrybyfhirid:
                self.err(f"the parent of derived sample {sampleid} hasn't been encountered in the json file yet.")
        
            if fh.parent_fhirid(resource) not in self.fp.aqtgchildless:
                self.err(f"the aliquotgroup of sample {sampleid} hasn't been encountered yet.") 
            # print(fh.parent_fhirid(resource) + " is not childless")
            self.fp.aqtgchildless[fh.parent_fhirid(resource)] = False
    def end(self):
        for fhirid in self.fp.aqtgchildless.keys():
            if self.fp.aqtgchildless[fhirid] == True:
                self.err(f"aliquotgroup {fhirid} is childless.")
