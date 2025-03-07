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





