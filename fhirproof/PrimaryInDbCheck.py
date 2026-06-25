# automatically generated, DON'T EDIT. please edit PrimaryInDbCheck.ct from where this file stems.
from dip import dig
from fhirproof.FhirCheck import *
from figs import specimen as figs
class PrimaryInDbCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample):
        """
         check checks whether the sample is in db if it is a master.
        """
        super().check(entry)

        # skip if no id given
        if self.db == None:
            return
        
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)

        # samplerow = sample(sampleid)
        #res = self.tr.sample(sampleids=[sampleid], verbose_all=True) # todo specify which verbose fields?

        if dbsample is None and figs.category(resource) == "MASTER":
            self.err(f"sample {sampleid} is type master but it is not in the db.")

