# automatically generated, DON'T EDIT. please edit DatesCheck.ct from where this file stems.
from datetime import datetime
from dip import dig, dis
from fhirproof.FhirCheck import *
from figs import specimen as figs
from tram import Sample
def isunknown(resource, path:str):
    """
     isunknown says when it's ok not to give an error when a date is missing, because it is unknown.
     
     it expects a object at path in the resource, holding an extension:
     
     path: `collection/_collectedDateTime`
     
     resource:
     
     `
     ...
     "collection" : {
         "collectedDateTime": "",
         "_collectedDateTime": {
         "extension": [
             {
                 "url": "http://hl7.org/fhir/StructureDefinition/data-absent-reason",
                 "valueCode": "unknown"
             }
         ]
     }
     ...
     `
    """
    atpath = dig(resource, path)
    if atpath is None:
        return False
    absent_reason = figs.extension(atpath, "http://hl7.org/fhir/StructureDefinition/data-absent-reason")
    return dig(absent_reason, "valueCode") == "unknown"
class DatesCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, dbsample:Sample):
        """
        """
        super().check(entry)
        resource = dig(entry, "resource")
        sampleid = figs.sampleid(resource)
        timechain = [] # ascending order
        if figs.category(resource) == "MASTER" or figs.category(resource) == "DERIVED":
            collectiondate = figs.collected_date(resource)
            if collectiondate is None and not isunknown(resource, "collection/_collectedDateTime"):
                self.err(f"no collection date for sample {sampleid}")
            else:
                timechain.append(["collection date", collectiondate])
        if figs.category(resource) == "MASTER":
            receiveddate = figs.received_date(resource)
            if receiveddate is None:
                self.err(f"no receivedTime for sample {sampleid}")
            else:
                timechain.append(["received date", receiveddate])
        if figs.category(resource) == "MASTER" or figs.category(resource) == "DERIVED":
            stockprodate = figs.stockprocessing_date(resource)
            if stockprodate is not None:
                timechain.append(["stockprocessing date", stockprodate])
            else:
                if figs.category(resource) == "MASTER" and dbsample is not None and dbsample.stockprocessing not in [None, "", "Sprec-N", "NO"]:
                    self.err(f"sample {sampleid} should come with a stockprocessing date (stock processing: {dbsample.stockprocessing}).")
        if figs.category(resource) == "DERIVED":
            deriv_date = figs.derival_date(resource)
            if deriv_date is not None:    
                timechain.append(["derival date", deriv_date])
            else:
                self.err(f"no derival date for sample {sampleid}")

        if figs.category(resource) == "DERIVED":
            repo_date = figs.reposition_date(resource)
            if repo_date is not None:
                timechain.append(["reposition date", repo_date])
            else:
                self.err(f"no reposition date for sample {sampleid}")
        # print("timechain: " + str(timechain))
        for i in range(1, len(timechain)):
            #if timechain[i][1] < timechain[i-1][1]: # [1] accesses the dates
            a = datetime.fromisoformat(timechain[i-1][1])
            b = datetime.fromisoformat(timechain[1][1])
            if DatesCheck.compare(a, b) == 1:
                self.err(f"in sample {sampleid} is {timechain[i][0]} before {timechain[i-1][0]}.") # [0] accesses the names
    @staticmethod
    def compare(a:datetime, b:datetime):
        """
         compare compares two datetimes. if one datetime is date-level (not
         time-level) compare both on date-level, otherwise compare on
         time-level.
         
         this handling is needed because there can be dates without a time,
         like 2025-12-05.  datetime sets their time to 00:00 when parsing.
         this would mean that a chain with middle time 00:00 would be correct
         if it's on the same day:
         
           2025-12-05 09:00
           2025-12-05 00:00
           2025-12-05 12:00
        """
        midnight = datetime.strptime("00:00:00", "%H:%M:%S")
        if a.time() == midnight.time() or b.time() == midnight.time():
            a = a.date()
            b = b.date()
        if a > b:
            return 1
        elif b > a:
            return -1
        else:
            return 0
