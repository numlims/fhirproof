# OrgCheck checks the organisation of a fhir entry

import re

from dbcon import *
from FhirCheck import *
import fhirhelp as fh

class OrgCheck(FhirCheck):

    def check(self, entry):
        # only do if sample in db?
        
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
        resource = entry["resource"]

        sampleid = fh.sampleid(resource)

        # get db org
        query = """
        select ou.code from centraxx_organisationunit ou 
        inner join centraxx_patientorgunit pou on ou.oid = pou.orgunit_oid
        inner join centraxx_patientcontainer pc on pou.patientcontainer_oid = pc.oid
        inner join centraxx_sample s on pc.oid = s.patientcontainer
        inner join centraxx_sampleidcontainer sidc on sidc.sample = s.oid where sidc.psn = ?"""

        result = qfad(query, sampleid)

        """
        Wir machen den Check nur, wenn es die Probe in der Datenbank gibt. Das
        sollte hier reichen: Dass Primärproben in der Datenbank sein sollen
        wird woanders gecheckt, und Deriveds müssen nicht unbedingt schon in
        der Datenbank sein.
        """
        db_org = ""
        # is there a result
        if len(result) == 0:
            self.err("no organisation in db for sample " + sampleid)
        else:
            db_org = result[0]["code"]

        # get json org
        json_org = fh.org(resource)
        if json_org == None:
            self.err("no organisation in json for sample " + sampleid)

        # do the orgs match?
        if db_org != json_org:
            self.err("organisation units don't match for sample " + sampleid + ", json org is " + json_org + ", db org is " + db_org)
