# automatically generated, DON'T EDIT. please edit IdContainerCheck.ct from where this file stems.
from fhirproof.FhirCheck import *
from dip import dig, dis
from fhirproof.fhirhelp import fhirhelp as fh
import tr
class IdContainerCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
         check runs the check.
        """
        super().check(entry)
        #print("traction: " + str(self.fp.tr))
        if self.fp.tr == None:
           return
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)

        #patientid = fh.limspsn(resource)
        res = self.fp.tr.sample(sampleids=[sampleid], verbose=[tr.trial])
        trialcode = None
        if len(res) > 0:
            trialcode = res[0].trial
        idcs = fh.identifiers(resource).keys()
        should = [ "SAMPLEID" ]
        
        confidcs = dig(self.fp.config, f"idcontainers/{trialcode}/{fh.type(resource)}")
        if confidcs is None:
            confidcs = []
        if fh.updatewithoverwrite(resource) == True:
            should.extend(confidcs)
        for idc in should:
          if idc not in idcs:
            self.err(f"sample {sampleid} should come with idcontainer {idc} for trial {trialcode}.")
        for idc in idcs:
          if idc not in confidcs + [ "SAMPLEID" ]:
            self.info(f"sample {sampleid} comes with idcontainer {idc} which is not specified for trial {trialcode} in the config.")
