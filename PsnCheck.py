import re

from FhirCheck import *
import fhirhelp as fh

class PsnCheck(FhirCheck):

    def __init__(self, fp):
        self.fp = fp
        
    def check(self, entry):

        """
        Ist das LIMS-Pseudonym (Limspsn) für den Patienten der in der DB zum
        Sample gehört das gleiche wie im Json? In der DB steht das
        Patienten-PSN in `idcontainer.psn` (das PSN in `sampleidcontainer` ist
        die Sampleid). Zu `idcontainer.psn` (Patient) kommen wir so: sowohl
        `sample` als auch `idcontainer` zeigen beide auf
        `patientcontainer.oid`, in `sample` über `sample.patientcontainer`, in
        `idcontainer` über `idcontainer.patientcontainer`. Wir joinen und
        sagen:
        """

        resource = entry["resource"]
        sampleid = fh.sampleid(resource)

        result = qfad("""
        select idc.psn from centraxx_sample s 
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid
        inner join centraxx_patientcontainer pc on s.patientcontainer = pc.oid 
        inner join centraxx_idcontainer idc on idc.patientcontainer = pc.oid
        where sidc.psn = ? and sidc.idcontainertype = 6""", sampleid)

        """
        Wenn das Sample Primary ist erwarten wir für die Limspsn ein Ergebnis,
        weil das Sample in der DB liegen sollte. Ansonsten, falls es ein
        Ergebnis gibt, checken wir es, sonst ist es nicht so schlimm.
        """

        if len(result) == 0:
            if fh.type(resource) == "MASTER":
                self.err("no patient psn in db for sample " + sampleid)
        elif fh.limspsn(resource) != result[0]["psn"]:
            self.err("limspsn for sample " + sampleid + " is " + fh.limspsn(resource) + " in json and " + result[0]["psn"] + " in db")

        """
        Wenn das Sample ein Derived/Aliquot ist, ist die Limspsn im
        Json-Parent die gleiche?
        """
        parentresource = self.fp.parent(entry)
        if parentresource != None:
            if fh.limspsn(parentresource) != fh.limspsn(resource):
                self.err("the limpspsn of sample " + sampleid + " is " + fh.limspsn(resource) + " in json, but " + fh.limspsn(parentresource) + " of its parent in json")
