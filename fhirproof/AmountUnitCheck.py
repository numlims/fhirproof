# automatically generated, DON'T EDIT. please edit AmountUnitCheck.ct from where this file stems.
from dip import dig
from fhirproof.FhirCheck import FhirCheck
from figs import specimen as figs
class AmountUnitCheck(FhirCheck):
    def check(self, entry):
        """
         check checks the amount unit for initial and rest amount.
        """
        super().check(entry)
        resource = dig(entry, "resource")
        initialau = figs.initialamountunit(resource)
        restau = figs.restamountunit(resource)
        aulist = dig(self.fp.config, "amountunits")
        if aulist is None:
            aulist = []
        if initialau is not None and initialau not in aulist:
            self.err(f"sample {figs.sampleid(resource)} comes with initial amount unit {initialau}, it needs to be in {dig(self.fp.config, 'amountunits')}.")
        if restau is not None and restau not in aulist:
            self.err(f"sample {figs.sampleid(resource)} comes with rest amount unit {restau}, it needs to be in {dig(self.fp.config, 'amountunits')}")
    def __init__(self, fp):
        """
         __init__ inits the check.
        """
        FhirCheck.__init__(self, fp)
