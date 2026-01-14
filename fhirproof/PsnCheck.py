# automatically generated, DON'T EDIT. please edit PsnCheck.ct from where this file stems.
import re

from fhirproof.FhirCheck import *
from figs import specimen as figs
from dip import dig
class PsnCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
         check leasst den check laufen.
        """
        super().check(entry)
        
        if self.db == None:
            return
    
    
            
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
    
        
        result = self.db.qfad("""
        select idc.psn from centraxx_sample s 
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid
        inner join centraxx_patientcontainer pc on s.patientcontainer = pc.oid 
        inner join centraxx_idcontainer idc on idc.patientcontainer = pc.oid
        where sidc.psn = ? and sidc.idcontainertype = 6""", sampleid)
        
        patid = figs.patientid(resource, "LIMSPSN")
        
        if len(result) == 0:
            if figs.type(resource) == "MASTER":
                self.err(f"no patient psn in db for sample {sampleid}")
        elif patid != result[0]["psn"]:
            self.err(f"limspsn for sample {sampleid} is {patid} in json and {result[0]['psn']} in db.")
        parentresource = self.fp.parent(entry)
        if parentresource != None:
            parent_patid = figs.patientid(parentresource, "LIMSPSN")
            if parent_patid != patid:
                self.err(f"the limpspsn of sample {sampleid} is {patid} in json, but {parent_patid} of its parent in json")
