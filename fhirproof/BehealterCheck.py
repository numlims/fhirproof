import re

from fhirproof.FhirCheck import *
from dip import dig, dis
from fhirproof.fhirhelp import fhirhelp as fh
class BehealterCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        
        container = dig(resource, "container/0/identifier/0/value")
        if fh.type(resource) == "MASTER" and container != "ORG":
            self.err(f"container for sample {sampleid} should be ORG (Originalcontainer) but is {container} in json.")
        aqt_allowed = ["NUM_AliContainer", "NUMCryoAliquot500", "NUMAliquot1000", "NUMAliquot2000"]
        if fh.type(resource) == "DERIVED" and container not in aqt_allowed:
           self.err(f"container for sample {sampleid} should be NUM_AliContainer but is {container} in json.")

