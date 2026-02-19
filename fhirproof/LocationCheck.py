# automatically generated, DON'T EDIT. please edit LocationCheck.ct from where this file stems.
import re

from dip import dig
from fhirproof.FhirCheck import *
from figs import specimen as figs

class LocationCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
        """
        super().check(entry)
        ok = True
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        # restmenge zero
        if figs.restamount(resource) == 0 and figs.locationpath(resource) != None:
            self.err(f"restmenge of sample {sampleid} is zero, it shouldn't have a lagerort but it's lagerort is {figs.locationpath(resource)}.")
        if figs.restamount(resource) > 0 and self.db != None:
            locpath = figs.locationpath(resource)
            # print(f"lagerort of sample {sampleid}: {locpath}")
            if locpath == None:
                self.err(f"no location path for sample {sampleid} in json, there should be one though.")

            query = "select * from centraxx_samplelocation where locationpath = ?"
            result = self.db.qfa(query, locpath)
            if len(result) == 0:
                self.err(f"location {locpath} for sample {sampleid} is not in db.") 
