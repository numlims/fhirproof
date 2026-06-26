# automatically generated, DON'T EDIT. please edit BehealterCheck.ct from where this file stems.
import tr
import re
from dip import dig, dis
from figs import specimen as figs
from fhirproof.FhirCheck import *
class BehealterCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample):
        """
        """
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        
        container = dig(resource, "container/0/identifier/0/value")
        if figs.category(resource) == "MASTER" and (dbsample != None and container != dbsample.receptacle):
            self.err(f"container for primary sample {sampleid} is {dbsample.receptacle} in db but is {container} in json.")
        aqt_allowed = self.fp.config["alicontainers"] # ["NUM_AliContainer", "NUMCryoAliquot500", "NUMAliquot1000", "NUMAliquot2000"]
        if figs.category(resource) == "DERIVED" and container not in aqt_allowed:
           self.err(f"container for derived sample {sampleid} is {container} in json but should be in {aqt_allowed}.")

