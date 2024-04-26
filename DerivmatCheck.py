# DerivmatCheck checks the material of a derived (aliquot) entry

import re

from dig import *
from FhirCheck import *
from fhirhelp import fhirhelp as fh

class DerivmatCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    def check(self, entry):
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)

        """
        Wir checken, ob Material eines Entries seinem Parent Entry entspricht,
        sofern es einen Parent gibt. Ist der Entry ein Derived (Aliquot), muss
        es das gleiche Material sein wie seine Parent-Aliquotgroup. Von
        Derived zu seiner Parent-Aliquotgroup kommen wir über die Fhirid.
        """
        
        child_material = dig(resource, "type/coding/0/code")

        parentresource = self.fp.parent(entry)
        if fh.type(resource) == "DERIVED" and parentresource:
            parent_material = parentresource("type/coding/0/code")
            if parent_material != child_material:
                self.err(f"parent and child material don't match, parent {p_fhirid} is of material {parent_material}, child {sampleid} is of material {child_material} (that's not SOP-conform)")

