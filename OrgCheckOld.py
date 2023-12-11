# OrgCheck checks the organisation of a fhir entry

## something fixed

import re

from dbcon import *
from FhirCheck import *
import fhirhelp as fh

class OrgCheck(FhirCheck):

    def check(self, entry):

        resource = entry["resource"]

        sampleid = fh.sampleid(resource)
        
        """
        Ist die Organisationunit vom Patienten und die der Probe die selbe?

        Die Organisationunit der Probe liegt im Json. Die Organisationunit vom
        Patienten holen wir aus der Datenbank.

        Die DB Query funktioniert so: Die codes der Organisation Units sind in
        `organisationsunit.code`. Der `idcontainer`, an den wir über die
        `sampleid` kommen, weist auf den `patientconainer`. Sie sind verbunden
        durch die Tabelle `patientorgunit`. Von `patientcontainer` kommen wir
        zu `sample`. Um an unser spezifisches Sample zu kommen müssen wir
        wieder über `sampleidcontainer` gehen.
        
        """
        """
        Der Patient keonnte zu mehreren Organisationseinheiten gehoeren, wegen Patientenzusammenfuehrungen. Dann waere die eine OE 'NUM'. Die filtern wir raus.
        """
        
        # get db org
        query = """
        select ou.code from centraxx_organisationunit ou 
        inner join centraxx_patientorgunit pou on ou.oid = pou.orgunit_oid
        inner join centraxx_patientcontainer pc on pou.patientcontainer_oid = pc.oid
        inner join centraxx_sample s on pc.oid = s.patientcontainer
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid where sidc.psn = ? and ou.code != 'NUM'"""

        dborgres = qfad(query, sampleid)

        """Wenn es die Probe in der Datenbank gibt checken wir die DB-Org der
        Probe gegen die Json-Org der Probe. Wenn es die Probe nicht in
        der Datenbank gibt, oder es keine DB-Org der Probe gibt,
        checken wir die DB-Org des Patienten gegen die Json-Org der
        Probe.

        """

        sample = sample(sampleid)
        
        # get json org
        json_org = fh.org(resource)

        typ = fh.type(resource)
        if typ == "MASTER":
            if json_org != None:
                # check
        else if typ == "DERIVED":
            if sample != None:
                if json_org != None:
                    # check
            else:
                if json_org == None:
                    # error
                else:
                    # check if oe of patient in db is oe in json
        
        db_org = ""
        # is there a result
        if len(dborgres) == 0:
            self.err("no organisation in db for sample " + sampleid)
        else:
            db_org = result[0]["code"]

        if json_org == None:
            self.err("no organisation in json for sample " + sampleid)

        # do the orgs match?
        if db_org != json_org:
            self.err("organisation units don't match for sample " + sampleid + ", json org is " + json_org + ", db org is " + db_org)
