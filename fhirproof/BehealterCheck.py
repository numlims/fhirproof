import re

from FhirCheck import *
from dig import *
from fhirhelp import fhirhelp as fh

class BehealterCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    def check(self, entry):
        """
        Primärproben sollen Originalcontainer sein, Aliquot-Deriveds NUM
        Aliquotcontainer.

        """
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        
        container = dig(resource, "container/0/identifier/0/value")
        if fh.type(resource) == "MASTER" and container != "ORG":
            self.err(f"container for sample {sampleid} should be ORG (Originalcontainer) but is {container} in json.")
        if fh.type(resource) == "DERIVED" and container != "NUM_AliContainer":
            self.err(f"container for sample {sampleid} should be NUM_AliContainer but is {container} in json.")


