import re

from FhirCheck import *
from fhirhelp import fhirhelp as fh
from dig import *


class PsnCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    

    def check(self, entry):
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
    
        
        result = self.db.qfad("""
        select idc.psn from centraxx_sample s 
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid
        inner join centraxx_patientcontainer pc on s.patientcontainer = pc.oid 
        inner join centraxx_idcontainer idc on idc.patientcontainer = pc.oid
        where sidc.psn = ? and sidc.idcontainertype = 6""", sampleid)
        
        if len(result) == 0:
            if fh.type(resource) == "MASTER":
                self.err(f"no patient psn in db for sample {sampleid}")
        elif fh.limspsn(resource) != result[0]["psn"]:
            self.err(f"limspsn for sample {sampleid} is {fh.limspsn(resource)} in json and {result[0]['psn']} in db")
        parentresource = self.fp.parent(entry)
        if parentresource != None:
            if fh.limspsn(parentresource) != fh.limspsn(resource):
                self.err(f"the limpspsn of sample {sampleid} is {fh.limspsn(resource)} in json, but {fh.limspsn(parentresource)} of its parent in json")
        

    


