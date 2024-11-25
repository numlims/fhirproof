import re

from dig import *
from FhirCheck import *
from fhirhelp import fhirhelp as fh



class LocationCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    def check(self, entry):
        ok = True
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        # restmenge zero
        if fh.restmenge(resource) == 0 and fh.lagerort(resource) != None:
            self.err(f"restmenge of sample {sampleid} is zero, it shouldn't have a lagerort but it's lagerort is {fh.lagerort(resource)}.")
        if fh.restmenge(resource) > 0:
            locpath = fh.lagerort(resource)
            # print(f"lagerort of sample {sampleid}: {locpath}")
            if locpath == None:
                self.err(f"no location path for sample {sampleid} in json, there should be one though.")

            query = "select * from centraxx_samplelocation where locationpath = ?"
            result = self.db.qfa(query, locpath)
            if len(result) == 0:
                self.err(f"location {locpath} for sample {sampleid} is not in db.") 



