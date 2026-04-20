# automatically generated, DON'T EDIT. please edit LamaObs.ct from where this file stems.
from fhirproof.FhirCheck import *
from figs import observation as figs
class LamaObs(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry):
        """
         check checks that only the codes belonging to the observation's method
         (messprofil) are given.
        """
        super().check(entry)
        resource = figs.resource(entry)
        method = figs.method(resource)
        res = self.tr.method(methods=[method])
        if method not in res:
            self.err(f"{method} not in db masterdata.")
        mema = res[method]
        cats = self.tr.catalog()
        comps = figs.component(resource)
        #print("comps:")
        #print(comps)
        for labval, comp in comps:
            if labval not in mema["labvals"]:
                self.err(f"labval {labval} not in db masterdata for method {method}.")
            lama = mema["labvals"][labval]                
            if lama["type"] == "CATALOG":
                catcode = lama["catalog"]
                if catcode not in cats:
                    self.err(f"no catalog {catcode} in db masterdata.")
                if comp['value'] not in cats[catcode]:
                    self.err(f"code {comp['value']} is not in catalog {catcode}.")
            if lama["type"] == "ENUMERATION":
                usageentries = lama["usageentry"]
                if comp["value"] not in usageentries:
                    self.err(f"code {comp['value']} is not part of usageentries for labval {lama['code']}. should be in {usageentries.keys()}")
