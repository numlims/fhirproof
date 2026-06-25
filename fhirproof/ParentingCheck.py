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
        if figs.category(resource) == "DERIVED":
            pfhirid = figs.parent_fhirid(resource)
            if pfhirid == None:
                self.err(f"sample {sampleid} is a derived, but there isn't a reference to a parent.")
                # we assume that we already visited the parent, if not, message
            elif pfhirid not in self.fp.entrybyfhirid:
                self.err(f"the parent of derived sample {sampleid} hasn't been encountered in the json file yet.")
            self.fp.aqtgchildless[pfhirid] = False
        if figs.category(resource) == "ALIQUOTGROUP":
            parentid = figs.parent_sampleid(resource)
            res = []
            if self.tr is not None:
                res = self.tr.sample(sampleids = [parentid])
            
            if not parentid in self.fp.entrybysampleid and len(res) == 0:
                self.err(f"the parent primary ({parentid}) of aliquot {figs.fhirid(resource)} isn't in the db and hasn't been encountered in the json yet.")
    def end(self):
        """
         end filters childless aliquot groups. it is called after all samples are checked.
        """
        for fhirid in self.fp.aqtgchildless.keys():
            if self.fp.aqtgchildless[fhirid] == True:
                super().check(dig(self.fp.entrybyfhirid, fhirid)) # for err to reference the correct file
                self.err(f"aliquotgroup {fhirid} is childless.")
