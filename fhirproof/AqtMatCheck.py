import re
import json
import os
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
from dip import dig, dis
class AqtMatCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    def check(self, entry):

        resource = dig(entry, "resource")
        self.info(f"checking aliquotgroup {dig(entry, 'fullUrl')}")

        # go to the pamm relative from current path
        pamm_path = os.path.join(os.getcwd(), self.fp.pamm_path)
        raw = json.loads(open(pamm_path).read()) # maps from primary sample material to aliquote material
        pamm = {} # pamm: primary-aliquot-material-map
        for ptoa in raw:
            pm = ptoa["primarySampleMaterial"]
            pamm[pm] = []
            for am in ptoa["aliquotMaterialList"]:
                pamm[pm].append(am["material"])
        child_material = dig(resource, "type/coding/0/code")
        pid = fh.parent_sampleid(resource)
        if pid == None:
            self.err(f"aliquotgroup {dig(entry, 'fullUrl')} has no parent.")
            return 
        
        parent_material = None
        if not pid in self.fp.entrybysampleid:
            if self.tr != None:
                res = self.tr.sample(sampleids = [pid], verbose_all = True) # todo specify which verbose fields?
                if len(res) == 0:
                    self.err(f"at aliquotgroup {dig(entry, 'fullUrl')}: the parent (id {pid}) is not in the db and hasn't been encountered in the json yet.")
                    return 
                parent_material = dig(res, "0/sampletype.code")
        else:
            parent = self.fp.entrybysampleid[pid]
            parent_material = fh.material(dig(parent, "resource"))
        # check
        if parent_material in ["CIT", "SER"]:
            if parent_material != child_material:
                self.err(f"material of aliquotegroup {dig(entry, 'fullUrl')} is {child_material}, but the material of its primary-parent {fh.sample_id(parent('resource'))} is {parent_material}")
        elif not child_material in pamm[parent_material]: # mappings in pamm
            self.err(f"material of aliquotegroup {dig(entry, 'fullUrl')} is {child_material}, but the material of its primary-parent {fh.sampleid(dig(parent, 'resource'))} is {parent_material}")
