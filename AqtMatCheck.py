# DerivmatCheck checks the organisation of a fhir entry

import re

# from dbcon import *
import json
from FhirCheck import *
import fhirhelp as fh

class AqtMatCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    def check(self, entry):
        """
        Sind wir bei einer Aliquotgroup, kann ihr Material eine Reihe von
        Werten sein, abhängig von ihrem Primary Parent. Das Mapping von
        Parent-Material zu den möglichen Materialien der Aliquotgroup-Children
        steht in `pamm`.  Material CIT und SER bleiben gleich zwischen Aliquotgroup und
        Primary Parent. Sie sind nicht im Mapping gelistet, wir checken sie so.
        """

        resource = entry.get("resource")
        self.info(f"checking aliquotgroup {entry.get('fullUrl')}")

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
        child_material = resource.get("type/coding/0/code")

        # parent
        pid = fh.parent_sampleid(resource)
        if pid == None:
            self.err(f"aliquotgroup {entry.get('fullUrl')} has no parent.")
            return 
        
        parent_material = None
        """ wenn der parent nicht schon im json aufgetaucht ist schauen wir nach ihm und seinem material in der db. """
        if not pid in self.fp.entrybysampleid:
            res = self.tr.smpl(psn = pid)
            if len(res) == 0:
                self.err(f"at aliquotgroup {entry.get('fullUrl')}: the parent (id {pid}) is not in the db and hasn't been encountered in the json yet.")
                return 
            parent_material = res.get("0/sampletype.code")
        else:
            parent = self.fp.entrybysampleid[pid]
            parent_material = fh.material(parent.get("resource"))

        # check
        if parent_material in ["CIT", "SER"]:
            if parent_material != child_material:
                self.err(f"material of aliquotegroup {entry.get('fullUrl')} is {child_material}, but the material of its primary-parent {fh.sample_id(parent('resource')} is {parent_material}")
        elif not child_material in pamm[parent_material]: # mappings in pamm
            self.err(f"material of aliquotegroup {entry.get('fullUrl')} is {child_material}, but the material of its primary-parent {fh.sampleid(parent.get('resource'))} is {parent_material}")
        
