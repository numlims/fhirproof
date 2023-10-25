import re

from FhirCheck import *
import fhirhelp as fh

class ParentingCheck(FhirCheck):
    entrybyfhirid = {} # entries referenced by fullUrl / fhirids, e.g. "Specimen/1037700"
    aqtgchildless = {} # is a aliquotgroup without children?
    
    def check(self, entry):
        self.entrybyfhirid[entry["fullUrl"]] = entry
        
        """
        Die Folgenden Checks brauchen den Parent einer Probe. Wenn wir den
        Parent im Json schon getroffen haben, speichern wir seine `resource`
        in `parentresource`. Die können die folgenden Checks als Unterpfand
        nehmen, dass der Check ob ein Parent da ist schon erledigt wurde.
        """
        resource = entry["resource"]
        parentresource = None
        if fh.type(resource) == "DERIVED":
            # print("derived sample: " + str(samplerow))
            # get fhirid of aliquotgroup-parent
            pfhirid = fh.parent_fhirid(resource)
            if pfhirid == None:
                error("sample " + sampleid + " is a derived, but there isn't a reference to a parent.")
            # we assume that we already visited the parent, if not, message
        elif pfhirid not in self.entrybyfhirid:
            error("the parent of derived sample " + sampleid + " hasn't been encountered in the json file yet.")
        else:
            parentresource = self.entrybyfhirid[pfhirid]["resource"]

        if fh.type(resource) == "DERIVED":
            if fh.parent_fhirid(resource) not in self.aqtgchildless:
                error("the aliquotgroup of sample " + sampleid + " hasn't been encountered yet.") 
            self.aqtgchildless[fh.parent_fhirid(resource)] = False


    def end():
        for fhirid in keys(self.aqtgchildless):
            if self.aqtgchildless[fhirid] == True:
                error("aliquotgroup " + fhirid + " is childless.")

