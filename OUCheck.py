# OUCheck checks the organisation unit of a fhir entry

import re

from dbcon import *
from FhirCheck import *
import fhirhelp as fh

class OUCheck(FhirCheck):

    def check(self, entry):

        resource = entry["resource"]

        sampleid = fh.sampleid(resource)

        s = sample(sampleid)

        # get db org of patient
        query = """
        select ou.code from centraxx_organisationunit ou 
        inner join centraxx_patientorgunit pou on ou.oid = pou.orgunit_oid
        inner join centraxx_patientcontainer pc on pou.patientcontainer_oid = pc.oid
        inner join centraxx_sample s on pc.oid = s.patientcontainer
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid where sidc.psn = ? and ou.code != 'NUM'"""

        dborgres = qfad(query, sampleid)

        # get json org
        json_org = fh.org(resource)

        typ = fh.type(resource)
        
        if s != None and typ == "MASTER":
            # MasterSample im LIMS
            if json_org != None:
                # OE im JSON - check notwendig
                self._check(dborgres, json_org, sampleid)
           # OE nicht im JSON angegeben - kein check notwendig
            
        elif typ == "DERIVED":

            if s != None:
                # Aliquot im LIMS
                if json_org != None:
                    # OE im JSON angegeben - check gegen DB notwendig
                    self._check(dborgres, json_org, sampleid)

                # OE nicht im JSON angegeben - kein check notwendig
            else:
                
                # Aliquot nicht im LIMS
                if json_org == None:
                    # OE nicht im JSON angegeben - fehler
                    self.err("there is no json org for derived sample " + sampleid)
                else:
                    # OE im JSON angegeben, check ob OE des Probanden aus DB mit OE im JSON übereinstimmt
                    self._check(dborgres, json_org, sampleid)
        
        # Aliquotgruppe: OE nicht notwendig

    # _check checks dborg and jsonorg
    def _check(self, dborgres, jsonorg, sampleid):
        dborg = ""
        # is there a result
        if len(dborgres) == 0:
            self.err("no organisation in db for sample " + sampleid)
        else:
            dborg = dborgres[0]["code"]

        if jsonorg == None:
            self.err("no organisation in json for sample " + sampleid)

        # do the orgs match?
        if dborg != jsonorg:
            self.err("organisation units don't match for sample " + sampleid + ", json org is " + jsonorg + ", db org is " + dborg)

