# OUCheck checks whether the organisation units in the db and json match, if a derived sample is not (yet) in the db it check's the organisation unit of the patient to whom the sample belongs

import re

# from dbcon import *
from FhirCheck import *
import fhirhelp as fh

class OUCheck(FhirCheck):

    def __init__(self, fp):
        FhirCheck.__init__(self, fp)

    def check(self, entry):
        """
        Ist die Organisationunit vom Patienten und die der Probe die selbe?

        Die Organisationunit der Probe liegt im Json. Die Organisationunit vom
        Patienten holen wir aus der Datenbank.
        """

        resource = entry.get("resource")

        sampleid = fh.sampleid(resource)

        s = self.tr.sample(sampleid)

        """
        Der Patient keonnte zu Organisationseinheiten gehoeren, wegen Patientenzusammenfuehrungen. Dann waere die eine OE 'NUM'. Die filtern wir raus.
        """

        # get db org of sample
        sampleorgq = """
        select ou.code as 'organisationunit.code' from centraxx_sample s 
        inner join centraxx_sampleidcontainer as sidc on sidc.sample = s.oid 
        inner join centraxx_organisationunit as ou on ou.oid = s.orgunit 
        where sidc.psn = ? and sidc.idcontainertype = 6 and ou.code != 'NUM'
        """
        
        # get patient org from db
        sampleorgres = self.db.qfad(sampleorgq, sampleid)

        # get sample org from json
        sampleorgjson = fh.org(resource)

        typ = fh.type(resource)

        # MasterSample im LIMS? 
        if s != None and typ == "MASTER":

            # OE im JSON - check notwendig
            if sampleorgjson != None:
                self._check(sampleorgres, sampleorgjson, sampleid)
           # OE nicht im JSON angegeben - kein check notwendig
            
        elif typ == "DERIVED": # derived sample
            
            # Aliquot im LIMS?
            if s != None:

                # OE im JSON angegeben?
                if sampleorgjson != None:
                    #  check gegen DB notwendig
                    self._check(sampleorgres, sampleorgjson, sampleid)

                # OE nicht im JSON angegeben - kein check notwendig
            else:
                # Aliquot nicht im LIMS
                
                # OE nicht im JSON angegeben
                if sampleorgjson == None:
                    # fehler
                    self.err("there is no json org for derived sample {sampleid}")
                else:
                    # OE im JSON angegeben

                    # check ob OE des Probanden aus DB mit OE im JSON übereinstimmt

                    patorgq = """
                    SELECT OU.CODE as 'organisationunit.code' FROM CENTRAXX_IDCONTAINER IDC 
                    INNER JOIN CENTRAXX_PATIENTORGUNIT POU ON IDC.PATIENTCONTAINER=POU.PATIENTCONTAINER_OID 
                    INNER JOIN CENTRAXX_IDCONTAINERTYPE IDCT ON IDC.IDCONTAINERTYPE=IDCT.OID 
                    INNER JOIN CENTRAXX_ORGANISATIONUNIT OU ON POU.ORGUNIT_OID=OU.OID 
                    WHERE OU.CODE != 'NUM' AND IDCT.CODE=? AND IDC.PSN=?
                    """
                    psn = fh.limspsn(resource)
                    patorg = self.db.qfad(patorgq, "LIMSPSN", psn)[0]['organisationunit.code'] # todo ist es immer LIMSPSN?
                    
                    # do the orgs of patient and sample match?
                    if sampleorgjson != patorg: # todo print patient psn
                        self.err(f"organisation units don't match for patient and sample {sampleid}, json org of sample is {sampleorgjson}, db org of its patient is {dborg}")

        # Aliquotgruppe: OE nicht notwendig

    
    # _check checks whether db org and json org of sample match
    def _check(self, dbresult, jsonorg, sampleid):
        dborg = ""
        # is there a result
        if len(dbresult) == 0:
            self.err(f"no organisation in db for sample {sampleid}")
        else:
            dborg = dbresult[0]["organisationunit.code"]

        if jsonorg == None:
            self.err(f"no organisation in json for sample {sampleid}")

        # do the orgs of patient and sample match?
        if dborg != jsonorg:
            self.err(f"organisation units don't match for sample {sampleid}, json org of sample is {jsonorg}, db org of is {dborg}")

