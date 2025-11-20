# automatically generated, DON'T EDIT. please edit BehealterCheck.ct from where this file stems.
import tr
import re
from dip import dig, dis
from fhirproof.fhirhelp import fhirhelp as fh
from fhirproof.FhirCheck import *
class BehealterCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
        """
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        
        container = dig(resource, "container/0/identifier/0/value")
        dbsample = None
        res = self.tr.sample(sampleids=[sampleid], verbose=[tr.receptacle])
        if len(res) > 0:
           dbsample = res[0]
        if fh.type(resource) == "MASTER" and (dbsample != None and container != dbsample.receptacle):
            self.err(f"container for primary sample {sampleid} should be {dbsample.receptacle} but is {container} in json.")
        aqt_allowed = ["NUM_AliContainer", "NUMCryoAliquot500", "NUMAliquot1000", "NUMAliquot2000"]
        if fh.type(resource) == "DERIVED" and container not in aqt_allowed:
           self.err(f"container for derived sample {sampleid} should be in {aqt_allowed} but is {container} in json.")

