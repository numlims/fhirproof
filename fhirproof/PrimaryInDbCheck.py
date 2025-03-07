from dig import *
from FhirCheck import *
from fhirhelp import fhirhelp as fh


class PrimaryInDbCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    def check(self, entry):
        
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)

        # samplerow = sample(sampleid)
        samplerow = self.tr.sample(sampleid)

        if samplerow == None and fh.type(resource) == "MASTER":
            self.err(f"sample {sampleid} is type master but it is not in the db.")




