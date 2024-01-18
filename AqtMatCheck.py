# DerivmatCheck checks the organisation of a fhir entry

import re

from dbcon import *
import json
from FhirCheck import *
import fhirhelp as fh

class AqtMatCheck(FhirCheck):

    def check(self, entry):
        """
        Sind wir bei einer Aliquotgroup, kann ihr Material eine Reihe von
        Werten sein, abhängig von ihrem Primary Parent. Das Mapping von
        Parent-Material zu den möglichen Materialien der Aliquotgroup-Children
        steht in `pamm`.  Material CIT und SER bleiben gleich zwischen Aliquotgroup und
        Primary Parent. Sie sind nicht im Mapping gelistet, wir checken sie so.
        """

        resource = entry["resource"]        
        self.info("checking aliquotgroup " + entry["fullUrl"])

        # read pamm
        ALIQUOT_MATERIAL_MAP = "2023-03_03_MaterialAliquotingMapping.json"
        raw = json.loads(open(ALIQUOT_MATERIAL_MAP).read()) # maps from primary sample material to aliquote material
        pamm = {} # pamm: primary-aliquot-material-map
        for ptoa in raw:
            pm = ptoa["primarySampleMaterial"]
            pamm[pm] = []
            for am in ptoa["aliquotMaterialList"]:
                pamm[pm].append(am["material"])

        
        # child
        child_material = resource["type"]["coding"][0]["code"]

        # parent
        pid = fh.parent_sampleid(resource)
        if pid == None:
            self.err("aliquotgroup " + entry["fullUrl"] + " has no parent.")
            return

        if not pid in self.fp.entrybysampleid:
            self.err("at aliquotgroup " + entry["fullUrl"] + ": the parent (id " + pid + ") hasn't been encountered yet.")
            return
        parent = self.fp.entrybysampleid[pid]
        
        parent_material = fh.material(parent["resource"])

        # check
        if parent_material in ["CIT", "SER"]:
            if parent_material != child_material:
                self.err("material of aliquotegroup " + entry["fullUrl"] + " is " + child_material + ", but the material of its primary-parent " + fh.sample_id(parent["resource"]) + " is " + parent_material)
        elif not child_material in pamm[parent_material]: # mappings in pamm
            self.err("material of aliquotegroup " + entry["fullUrl"] + " is " + child_material + ", but the material of its primary-parent " + fh.sampleid(parent["resource"]) + " is " + parent_material)
