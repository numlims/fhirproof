# automatically generated, DON'T EDIT. please edit IdContainerCheck.ct from where this file stems.
from fhirproof.FhirCheck import *
from dip import dig, dis
from figs import specimen as figs
import tr
class IdContainerCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample):
        """
         check runs the check.
        """
        super().check(entry)
        #print("traction: " + str(self.fp.tr))
        if dbsample is None:
           return
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)

        #patientid = figs.limspsn(resource)
        trialcode = dbsample.trial
        idcs = figs.identifiers(resource).keys()
        should = [ "SAMPLEID" ]
        
        confidcs = dig(self.fp.config, f"idcontainers/{trialcode}/{figs.category(resource)}")
        if confidcs is None:
            confidcs = []
        if figs.update_with_overwrite(resource) == True:
            should.extend(confidcs)
        for idc in should:
          if idc not in idcs:
            self.err(f"sample {sampleid} should come with idcontainer {idc} for trial {trialcode}.")
        for idc in idcs:
          if idc not in confidcs + [ "SAMPLEID" ]:
            self.info(f"sample {sampleid} comes with idcontainer {idc} which is not strictly needed for trial {trialcode}.")
