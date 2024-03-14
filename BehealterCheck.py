import re

from FhirCheck import *

class BehealterCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    def check(self, entry):
        """
        Primärproben sollen Originalcontainer sein, Aliquot-Deriveds NUM
        Aliquotcontainer.

        """
        resource = entry["resource"]
        sampleid = fh.sampleid(resource)
        
        container = resource["container"][0]["identifier"][0]["value"]
        if fh.type(resource) == "MASTER" and container != "ORG":
            self.err(f"container for sample {sampleid} should be ORG (Originalcontainer) but is {container} in json.")
        if fh.type(resource) == "DERIVED" and container != "NUM_AliContainer":
            self.err(f"container for sample {sampleid} should be NUM_AliContainer but is {container} in json.")


