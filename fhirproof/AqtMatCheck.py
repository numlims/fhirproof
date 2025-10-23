# automatically generated, DON'T EDIT. please edit AqtMatCheck.ct from where this file stems.
import re
import json
import os
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
from dip import dig, dis
class AqtMatCheck(FhirCheck):
    def __init__(self, fp):
        """
         __init__ inits AqtMatCheck.
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
        """
        super().check(entry)

        resource = dig(entry, "resource")
        self.info(f"checking aliquotgroup {dig(entry, 'fullUrl')}")

        pamm = self.fp.config["pamm"]
        child_material = dig(resource, "type/coding/0/code")
        parentid = fh.parent_sampleid(resource)
        parentfhirid = fh.parent_fhirid(resource)        
        if parentid == None and parentfhirid == None:
            self.err(f"no parent reference given for aliquotgroup {dig(entry, 'fullUrl')}.")
            return 
        
        parent_material = None
        parent = None
        if parentid and parentid in self.fp.entrybysampleid:
           parent = self.fp.entrybysampleid[parentid]
        elif parentfhirid and parentfhirid in self.fp.entrybyfhirid:
           parent = self.fp.entrybyfhirid[parentfhirid]

        parent_material = fh.material(dig(parent, "resource"))
        if (not parent) and parentid:
            if self.tr != None:
                res = self.tr.sample(sampleids = [parentid], verbose_all = True) # todo specify which verbose fields?
                if len(res) == 0:
                    self.err(f"at aliquotgroup {dig(entry, 'fullUrl')}: the parent (id {pid}) is not in the db and hasn't been encountered in the json yet.")
                    return 
                parent_material = dig(res, "0/" + tr.sampletype_code)
        if not parent_material in pamm:
            self.info(f"material {parent_material} is not in pamm.")
        elif "*" in pamm[parent_material]:
            pass
        elif not child_material in pamm[parent_material]: # mappings in pamm
            self.err(f"material of aliquotgroup {dig(entry, 'fullUrl')} is {child_material}, needs to be in {pamm[parent_material]} to match the material {parent_material} of its primary parent {fh.sampleid(dig(parent, 'resource'))}")
