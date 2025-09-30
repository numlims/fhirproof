from fhirproof.FhirCheck import *
from dip import dig, dis
from fhirproof.fhirhelp import fhirhelp as fh
import tr
class IdContainerCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        super().check(entry)
        confidcs = dig(self.fp.config, "idcontainers")
        # print("confidcs: " + str(confidcs))
        if confidcs == None:
           return
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)

        #patientid = fh.limspsn(resource)
        trialcode = self.fp.tr.sample(sampleids=[sampleid], verbose=[tr.trial_code])
        #trialcode = trials[0]["code"]
        idcs = fh.identifiers(resource).keys()
        if trialcode in list(confidcs.keys()):
          # missing
          for idc in confidcs[trialcode]:
            if idc not in idcs:
              self.err(f"sample {sampleid} should come with idcontainer {idc} for trial {trialcode}.")
          # not needed
          for idc in idcs:
            if idc not in confidcs[trialcode]:
              self.info(f"sample {sampleid} comes with idcontainer {idc} which is not specified for trial {trial} in the config.")
