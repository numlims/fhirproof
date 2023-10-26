import re

from FhirCheck import *
import fhirhelp as fh

# ParentingCheck checks that parent references add up
class ParentingCheck(FhirCheck):

    def __init__(self, fp):
        self.fp = fp
        
    def check(self, entry):
        resource = entry["resource"]
        sampleid = fh.sampleid(resource)
        
        # is there a reference to a parent?
        if fh.type(resource) == "DERIVED":
            # print("derived sample: " + str(samplerow))
            # get fhirid of aliquotgroup-parent
            pfhirid = fh.parent_fhirid(resource)

            if pfhirid == None:
                self.err("sample " + sampleid + " is a derived, but there isn't a reference to a parent.")
                # we assume that we already visited the parent, if not, message
            elif pfhirid not in self.fp.entrybyfhirid:
                self.err("the parent of derived sample " + sampleid + " hasn't been encountered in the json file yet.")

        if fh.type(resource) == "DERIVED":
            if fh.parent_fhirid(resource) not in self.fp.aqtgchildless:
                self.err("the aliquotgroup of sample " + sampleid + " hasn't been encountered yet.") 
            self.fp.aqtgchildless[fh.parent_fhirid(resource)] = False


    def end(self):
        for fhirid in self.fp.aqtgchildless.keys():
            if self.fp.aqtgchildless[fhirid] == True:
                self.err("aliquotgroup " + fhirid + " is childless.")

