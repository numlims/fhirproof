# automatically generated, DON'T EDIT. please edit DatesCheck.ct from where this file stems.
from datetime import datetime
from dip import dig, dis
from fhirproof.FhirCheck import *
from figs import specimen as figs
from tram import Sample
class DatesCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def isodate(self, s):
        """
         isodate parses date from iso formatted string. for now return date
         only, to allow day-precision dates to pass check.
        """
        # example date: 2023-07-17T05:16:36.000+02:00
        # return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
        #return datetime.fromisoformat(s)
        return datetime.fromisoformat(s).date()
    def check(self, entry, dbsample:Sample):
        """
        """
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        timechain = [] # ascending order
        if figs.category(resource) == "MASTER" or figs.category(resource) == "DERIVED":
            collectiondate = figs.collected_date(resource)
            if collectiondate is None:
                self.err(f"no collection date for sample {sampleid}")
            else:
                timechain.append(["collection date", self.isodate(collectiondate)])
        if figs.category(resource) == "MASTER":
            receiveddate = figs.received_date(resource)
            if receiveddate is None:
                self.err(f"no receivedTime for sample {sampleid}")
            else:
                timechain.append(["received date", self.isodate(receiveddate)])
        if figs.category(resource) == "MASTER" or figs.category(resource) == "DERIVED":
            centridate = figs.centrifugation_date(resource)
            if centridate is not None:
                timechain.append(["centrifugation date", self.isodate(centridate)])
            else:
                if dbsample is not None and dbsample.stockprocessing not in [None, "", "Sprec-N", "NO"]:
                    self.err(f"sample {sampleid} should come with a centrifugation date (stock processing: {dbsample.stockprocessing}).")
        if figs.category(resource) == "DERIVED":
            deriv_date = figs.derival_date(resource)
            if deriv_date is not None:    
                timechain.append(["derival date", self.isodate(deriv_date)])
            else:
                self.err(f"no derival date for sample {sampleid}")

        if figs.category(resource) == "DERIVED":
            repo_date = figs.reposition_date(resource)
            if repo_date is not None:
                timechain.append(["reposition date", self.isodate(repo_date)])
            else:
                self.err(f"no reposition date for sample {sampleid}")
        # print("timechain: " + str(timechain))
        for i in range(1, len(timechain)):
            if timechain[i][1] < timechain[i-1][1]: # [1] accesses the dates
                self.err(f"in sample {sampleid} is {timechain[i][0]} before {timechain[i-1][0]}") # [0] accesses the names
