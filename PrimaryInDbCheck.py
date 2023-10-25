# PrimaryInDb checks whether a primary sample is in the database

from dbcon import *
from FhirCheck import *

class PrimaryInDbCheck(FhirCheck):

    # check checks whether the sample is in db if it is a master
    def check(self, entry):
        resource = entry["resource"]

        sampleid = fh.sample_id(resource)

        samplerow = sample(sampleid)

        if samplerow == None and fh.type(resource) == "MASTER":
            error("sample " + sampleid + " is type master but it is not in the db.")

