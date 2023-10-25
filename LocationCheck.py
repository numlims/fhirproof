import re

from FhirCheck import *

class LocationCheck(FhirCheck):

    def check(self, entry):
        """
        Gibt es den Lagerort in der DB? Für alle Aliquot-Deriveds ist der
        Lagerort angegeben, außer ihre Restmenge ist null. Bei Primärproben
        ist nur bei Speichel und PaxGene ein Lagerort angegeben.
        """
        resource = entry["resource"]
        if (fh.type(resource) == "DERIVED" and fh.restmenge(resource) > 0) or (fh.type(resource) == "MASTER" and (fh.material(resource) == "NUM_speichel" or fh.material(resource) == "PAXgene")):
            locpath = None
            for e in resource["extension"]:
                if e["url"] == "https://fhir.centraxx.de/extension/sample/sampleLocation":
                    for ee in e["extension"]:
                        if ee["url"] == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                            locpath = ee["valueString"]
            if locpath == None:
                error("no location path for sample " + sampleid + ", there should be one though.")

            """
            Der Lagerort ist ein Pfad, der entweder mit einem Rack endet oder
            nicht. In der Datenbank stehen die Lagerorte ohne Rack. Im Json kann
            man nicht erkennen, ob der letzte Bestandteil vom Lagerort ein Rack
            ist oder nicht, deshalb machen wir zwei checks, einmal den kompletten
            Pfad und einmal mit abgeschnittenem Ende.
            """
            query = "select * from centraxx_samplelocation where locationpath = ?"
            result = query_fetch_all(query, locpath)
            if len(result) == 0:
                # check the shorter path, non-greedy matching
                shortpath = re.sub(" -->.*$", "", locpath)
                result = query_fetch_all(query, shortpath)
                if len(result) == 0:
                    error("location " + locpath + " for sample " + sampleid + " is not in db.") 

