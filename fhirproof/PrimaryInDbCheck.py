from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
class PrimaryInDbCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    def check(self, entry):

        # skip if no id given
        if self.db == None:
            return
        
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)

        # samplerow = sample(sampleid)
        samplerow = self.tr.sample(sampleids=[sampleid], verbose_all=True) # todo specify which verbose fields?

        if samplerow == None and fh.type(resource) == "MASTER":
            self.err(f"sample {sampleid} is type master but it is not in the db.")

