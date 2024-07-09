import re
import json
from FhirCheck import *
from fhirhelp import fhirhelp as fh
from dig import *


class AqtMatCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    def check(self, entry):

        resource = dig(entry, "resource")
        self.info(f"checking aliquotgroup {dig(entry, 'fullUrl')}")

        ALIQUOT_MATERIAL_MAP = "2023-03_03_MaterialAliquotingMapping.json"
        raw = json.loads(open(ALIQUOT_MATERIAL_MAP).read()) # maps from primary sample material to aliquote material
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
            res = self.tr.smpl(psn = pid)
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





