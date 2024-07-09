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
        if (fh.type(resource) == "DERIVED" and fh.restmenge(resource) > 0) or (fh.type(resource) == "MASTER" and (fh.material(resource) == "NUM_speichel" or fh.material(resource) == "PAXgene")):
            locpath = None
            for e in dig(resource, "extension"):
                if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocation":
                    for ee in dig(e, "extension"):
                        if dig(ee, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                            locpath = dig(ee, "valueString")
            if locpath == None:
                self.err(f"no location path for sample {sampleid}, there should be one though.")
            query = "select * from centraxx_samplelocation where locationpath = ?"
            result = self.db.qfa(query, locpath)
            if len(result) == 0:
                # check the shorter path, non-greedy matching
                shortpath = re.sub(" -->.*$", "", locpath)
                result = self.db.qfa(query, shortpath)
                if len(result) == 0:
                    self.err(f"location {locpath} for sample {sampleid} is not in db.") 





