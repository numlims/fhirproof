# RestmengeCheck checks the rest amount of a fhir entry

import re

from FhirCheck import *
import fhirhelp as fh

class RestmengeCheck(FhirCheck):

    entries = []

    def check(self, entry):
        # remember restmenge
        """
        Bei Masters mit Aliquoten soll die Restmenge größer null
        sein, bei Masters ohne Aliquote soll die Restmenge null sein.

Wie finden wir die Restmenge im Json? In der Simplifier Doku gibt es
        specimen.container.specimenQuantity:restAmount. Das zeigt auf
        Specimen.container.specimenQuantity im Json. 

Wir führen Buch. Begegnen wir einem Aliquot, merken wir uns in
        `shouldzerorest`, dass die Restmenge von seinem Parent null sein
        sollte. Am Ende gehen wir alle Entries durch und schauen, dass wenn
        für sie `shouldzerorest` gilt, ihre Restmenge wirklich null ist.
        """
        self.entries.append(entry) # remember for later
        resource = entry["resource"]
        self.fp.shouldzerorest[entry["fullUrl"]] = False
        # parents of derived-aliquotes should be with zero rest
        if fh.type(resource) == "DERIVED":
            self.fp.shouldzerorest[fh.parent_fhirid(resource)] = True


    def end(self):
        for entry in self.entries:
            #    restamount = entry["resource"]["container"][0]["specimenQuantity"]["value"]
            restamount = fh.restmenge(entry["resource"])
            sampleid = fh.sampleid(entry["resource"])
            # should restamount be zero, but isn't?
            if entry["fullUrl"] in self.fp.shouldzerorest and self.fp.shouldzerorest[entry["fullUrl"]] == True and restamount > 0:
                self.err("restamount (container.specimenQuantity) for sample " + sampleid + " should be zero, but is " + restamount)
