import re

from FhirCheck import *

class LocationCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    def check(self, entry):
        ok = True
        """
        Gibt es den Lagerort in der DB? Für alle Aliquot-Deriveds ist der
        Lagerort angegeben, außer ihre Restmenge ist null. Bei Primärproben
        ist nur bei Speichel und PaxGene ein Lagerort angegeben.
        """
        resource = entry.get("resource")
        sampleid = fh.sampleid(resource)
        if (fh.type(resource) == "DERIVED" and fh.restmenge(resource) > 0) or (fh.type(resource) == "MASTER" and (fh.material(resource) == "NUM_speichel" or fh.material(resource) == "PAXgene")):
            locpath = None
            for e in resource.get("extension"):
                if e.get("url") == "https://fhir.centraxx.de/extension/sample/sampleLocation":
                    for ee in e.get("extension"):
                        if ee.get("url") == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                            locpath = ee.get("valueString")
            if locpath == None:
                self.err(f"no location path for sample {sampleid}, there should be one though.")

            """
            Der Lagerort ist ein Pfad, der entweder mit einem Rack endet oder
            nicht. In der Datenbank stehen die Lagerorte ohne Rack. Im Json kann
            man nicht erkennen, ob der letzte Bestandteil vom Lagerort ein Rack
            ist oder nicht, deshalb machen wir zwei checks, einmal den kompletten
            Pfad und einmal mit abgeschnittenem Ende.
            """
            query = "select * from centraxx_samplelocation where locationpath = ?"
            result = self.db.qfa(query, locpath)
            if len(result) == 0:
                # check the shorter path, non-greedy matching
                shortpath = re.sub(" -->.*$", "", locpath)
                result = self.db.qfa(query, shortpath)
                if len(result) == 0:
                    self.err(f"location {locpath} for sample {sampleid} is not in db.") 


