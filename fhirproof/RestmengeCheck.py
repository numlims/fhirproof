import re

import numbers
from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
class RestmengeCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    entries = []    
    def check(self, entry):
        self.entries.append(entry) # remember for later
        self.fp.shouldzerorest[entry["fullUrl"]] = False
        resource = dig(entry, "resource")
        # parents of derived-aliquotes should be with zero rest
        if fh.type(resource) == "DERIVED":
            self.fp.shouldzerorest[fh.parent_fhirid(resource)] = True
        restamount = fh.restmenge(resource)
        sampleid = fh.sampleid(resource)
        if not isinstance(restamount, numbers.Number):
            self.err(f"restamount for sample {sampleid} needs to be a number ({type(restamount).__name__}).")
        collectionQuantity = dig(resource, "collection/quantity/value")
        if collectionQuantity is not None and not isinstance(collectionQuantity, numbers.Number):
            self.err(f"collection quantity for sample {sampleid} needs to be a number (not {type(collectionQuantity).__name__}).")
        if (restamount is None or restamount == 0) and fh.lagerort(resource) is not None:
            self.err(f"restmenge for sample {sampleid} is zero, and there is a sampleLocation given, please remove the sampleLocation")
    def end(self):
        for entry in self.entries:
            #    restamount = entry["resource"]["container"][0]["specimenQuantity"]["value"]
            restamount = fh.restmenge(dig(entry, "resource"))
            sampleid = fh.sampleid(dig(entry, "resource"))
            # should restamount be zero, but isn't?
            if dig(entry, "fullUrl") in self.fp.shouldzerorest and self.fp.shouldzerorest[dig(entry, "fullUrl")] == True and restamount > 0:
                self.err(f"restamount (container.specimenQuantity) for sample {sampleid} should be zero, but is {restamount}")
    
