# DatesCheck checks the time order of samples

from datetime import datetime

from FhirCheck import *

class DatesCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    # isodate parses date from iso formatted string
    def isodate(self, s):
        # example date: 2023-07-17T05:16:36.000+02:00
        # return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
        return datetime.fromisoformat(s)

    def check(self, entry):
        """
        Proben sollten in dieser zeitlichen Reihenfolge verarbeitet werden: 

        Abnahme (Collection) [bei Primär]<br/>
        Laboreingang (Received)  <br/>
        Zentrifugation [wenn da] <br/>
        Aliquotierung (Derival) [bei Aliquoten]   <br/>

        Wir legen die Zeiten für die Verarbeitungsschritte in das Array
        `timechain` in der Reihenfolge, in der wir sie erwarten. Dann können
        wir checken, ob die Zeiten in `timechain` tatsächlich in aufsteigender
        Reihenfolge sind.
        """
        resource = entry.get("resource")
        sampleid = fh.sampleid(resource)
        timechain = [] # ascending order
        if fh.type(resource) == "MASTER" or fh.type(resource) == "DERIVED":
            if "collection" not in resource or "collectedDateTime" not in resource.get("collection"):
                self.err(f"no collection date in {sampleid}")
            else:
                timechain.append(["collection date", self.isodate(resource.get("collection/collectedDateTime"))])
        if fh.type(resource) == "MASTER":
            if "receivedTime" not in resource:
                self.err(f"no receivedTime in sample {sampleid}")
            else:
                timechain.append(["received date", self.isodate(resource.get("receivedTime"))])
        if fh.type(resource) == "MASTER" or fh.type(resource) == "DERIVED":
            centri_date = None
            for e in resource.get("extension"):
                if e.get("url") == "https://fhir.centraxx.de/extension/sprec":
                    for ee in e.get("extension"):
                        if ee.get("url") == "https://fhir.centraxx.de/extension/sprec/preCentrifugationDelayDate":
                            centri_date = self.isodate(ee.get("valueDateTime"))
                            timechain.append(["centrifugation date", centri_date])

        """
        Bei Aliquoten sollte die Aliquotierung (Derival) nach der
        Zentrifugation sein, wir legen sie auf `timechain`.
        """

        if fh.type(resource) == "DERIVED":
            deriv_date = False
            for e in resource.get("extension"):
                if e.get("url") == "https://fhir.centraxx.de/extension/sample/derivalDate":
                    deriv_date = True
                    timechain.append(["derival date", self.isodate(e.get("valueDateTime"))])
            if deriv_date == False:
                self.err(f"no derival date for sample {sampleid}")


        """
        Aliquote sollten eingefroren worden sein (Reposition-Date) nachdem sie
        derived wurden.
        """

        if fh.type(resource) == "DERIVED":
            repo_date = False
            for e in resource.get("extension"):
                if e.get("url") == "https://fhir.centraxx.de/extension/sample/repositionDate":
                    repo_date = True
                    timechain.append(["reposition date", self.isodate(e.get("valueDateTime"))])
            if repo_date == False:
                self.err("no reposition date for sample {sampleid}")



        """
        Jetzt checken wir, ob die Einträge in `timechain` in aufsteigender
        Reihenfolge liegen.
        """

        # print("timechain: " + str(timechain))
        for i in range(1, len(timechain)):
            if timechain[i][1] < timechain[i-1][1]: # [1] accesses the dates
                self.err(f"in sample {sampleid} is {timechain[i][0]} before {timechain[i-1][0]}") # [0] accesses the names






        
