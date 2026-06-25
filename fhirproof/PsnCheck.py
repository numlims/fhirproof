# automatically generated, DON'T EDIT. please edit PsnCheck.ct from where this file stems.
import re

from fhirproof.FhirCheck import *
from figs import specimen as figs
from dip import dig
import tr
class PsnCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample):
        """
         check runs the check.
        """
        super().check(entry)
        
        if self.db == None:
            return
    
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        dbpatid = None
        if dbsample is not None:
            dbpatid = dbsample.patient.id()
        jpatid = figs.patientid(resource, "LIMSPSN")
        if dbpatid is None:
            if figs.category(resource) == "MASTER":
                self.err(f"no patient psn in db for sample {sampleid}")
        elif dbpatid.strip().casefold() != jpatid.strip().casefold():
            self.err(f"limspsn for sample {sampleid} is {jpatid} in json and {dbpatid} in db.")
        parentresource = self.fp.parent(entry)
        if parentresource != None:
            parent_patid = figs.patientid(parentresource, "LIMSPSN")
            if parent_patid != jpatid:
                self.err(f"the limpspsn of sample {sampleid} is {jpatid} in json, but {parent_patid} of its parent in json.")
