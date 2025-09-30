import re

from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
class DerivmatCheck(FhirCheck):
      def __init__(self, fp):
          FhirCheck.__init__(self, fp)
      def check(self, entry):
          super().check(entry)
          resource = dig(entry, "resource")
          sampleid = fh.sampleid(resource)
  
          child_material = dig(resource, "type/coding/0/code")
  
          parentresource = self.fp.parent(entry)
          if fh.type(resource) == "DERIVED" and parentresource:
              parent_material = dig(parentresource, "type/coding/0/code")
              if parent_material != child_material:
                  parentfhirid = dig(parentresource, "fullUrl")
                  self.err(f"parent and child material don't match, parent {parentfhirid} is of material {parent_material}, child {sampleid} is of material {child_material} (that's not SOP-conform)")
  
