# automatically generated, DON'T EDIT. please edit PrimaryMatCheck.ct from where this file stems.
from fhirproof.FhirCheck import FhirCheck
from figs import specimen as figs
class PrimaryMatCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample):
        """
         check checks that the material doesn't change for primary samples.
        """
        super().check(entry)
        resource = figs.resource(entry)
        if figs.category(resource) != "MASTER":
            return
        sampleid = figs.sampleid(resource)
        if dbsample is None:
            return
        if figs.type(resource) != dbsample.type:
            self.err(f"material of primary sample {sampleid} can't be changed. (from {dbsample.type} to {figs.type(resource)})")
