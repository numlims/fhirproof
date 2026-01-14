# automatically generated, DON'T EDIT. please edit ParentingCheck.ct from where this file stems.
import re

from dip import dig
from fhirproof.FhirCheck import *
from figs import specimen as figs
class ParentingCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
        """
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        # is there a reference to a parent?
        if figs.type(resource) == "DERIVED":
        
            # is there a fhirid referencing a parent?
            pfhirid = figs.parent_fhirid(resource)
            if pfhirid == None:
                self.err(f"sample {sampleid} is a derived, but there isn't a reference to a parent.")
                # we assume that we already visited the parent, if not, message
            elif pfhirid not in self.fp.entrybyfhirid:
                self.err(f"the parent of derived sample {sampleid} hasn't been encountered in the json file yet.")
        
            if figs.parent_fhirid(resource) not in self.fp.aqtgchildless:
                self.err(f"the aliquotgroup of sample {sampleid} hasn't been encountered yet.") 
            # print(figs.parent_fhirid(resource) + " is not childless")
            self.fp.aqtgchildless[figs.parent_fhirid(resource)] = False
    def end(self):
        """
        """
        for fhirid in self.fp.aqtgchildless.keys():
            if self.fp.aqtgchildless[fhirid] == True:
                self.err(f"aliquotgroup {fhirid} is childless.")
