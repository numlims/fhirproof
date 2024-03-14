# PrimaryInDb checks whether a primary sample is in the database

# from dbcon import *
from FhirCheck import *

class PrimaryInDbCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    # check checks whether the sample is in db if it is a master
    def check(self, entry):
        
        resource = entry["resource"]

        sampleid = fh.sampleid(resource)

        # samplerow = sample(sampleid)
        samplerow = self.tr.sample(sampleid)

        if samplerow == None and fh.type(resource) == "MASTER":
            self.err(f"sample {sampleid} is type master but it is not in the db.")
        

