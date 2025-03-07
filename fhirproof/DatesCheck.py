from datetime import datetime
from dig import *
from FhirCheck import *
from fhirhelp import fhirhelp as fh


class DatesCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    # isodate parses date from iso formatted string
    def isodate(self, s):
        # example date: 2023-07-17T05:16:36.000+02:00
        # return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
        return datetime.fromisoformat(s)


    def check(self, entry):
        resource = dig(entry, "resource")
        sampleid = fh.sampleid(resource)
        timechain = [] # ascending order
        if fh.type(resource) == "MASTER" or fh.type(resource) == "DERIVED":
            if "collection" not in resource or "collectedDateTime" not in dig(resource, "collection"):
                self.err(f"no collection date in {sampleid}")
            else:
                timechain.append(["collection date", self.isodate(dig(resource, "collection/collectedDateTime"))])
        if fh.type(resource) == "MASTER":
            if "receivedTime" not in resource:
                self.err(f"no receivedTime in sample {sampleid}")
            else:
                timechain.append(["received date", self.isodate(dig(resource, "receivedTime"))])
        if fh.type(resource) == "MASTER" or fh.type(resource) == "DERIVED":
            centri_date = None
            for e in dig(resource, "extension"):
                if dig(e, "url") == "https://fhir.centraxx.de/extension/sprec":
                    for ee in dig(e, "extension"):
                        if dig(ee, "url") == "https://fhir.centraxx.de/extension/sprec/preCentrifugationDelayDate":
                            centri_date = self.isodate(dig(ee, "valueDateTime"))
                            timechain.append(["centrifugation date", centri_date])
        if fh.type(resource) == "DERIVED":
            deriv_date = False
            for e in dig(resource, "extension"):
                if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/derivalDate":
                    deriv_date = True
                    timechain.append(["derival date", self.isodate(dig(e, "valueDateTime"))])
            if deriv_date == False:
                self.err(f"no derival date for sample {sampleid}")

        if fh.type(resource) == "DERIVED":
            repo_date = False
            for e in dig(resource, "extension"):
                if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/repositionDate":
                    repo_date = True
                    timechain.append(["reposition date", self.isodate(dig(e, "valueDateTime"))])
            if repo_date == False:
                self.err("no reposition date for sample {sampleid}")

        # print("timechain: " + str(timechain))
        for i in range(1, len(timechain)):
            if timechain[i][1] < timechain[i-1][1]: # [1] accesses the dates
                self.err(f"in sample {sampleid} is {timechain[i][0]} before {timechain[i-1][0]}") # [0] accesses the names





