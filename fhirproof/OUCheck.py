import re

from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
class OUCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)
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
    def check(self, entry):
    
        if self.db == None:
            return 
        
        resource = dig(entry, "resource")
    
        sampleid = fh.sampleid(resource)
    
        s = self.tr.sample(sampleid)
    
        # get db org of sample
        sampleorgq = """
        select ou.code as 'organisationunit.code' from centraxx_sample s 
        inner join centraxx_sampleidcontainer as sidc on sidc.sample = s.oid 
        inner join centraxx_organisationunit as ou on ou.oid = s.orgunit 
        where sidc.psn = ? and sidc.idcontainertype = 6 and ou.code != 'NUM'
        """
    
        """dq query:
        select centraxx_organisationunit {
          .code[!= 'NUM'],
          <centraxx_sample<centraxx_sampleidcontainer {
            .psn[=?], .idcontainertype[=6]
          }
        }
        """
        sampleorgres = self.db.qfad(sampleorgq, sampleid)
        # sample org from json
        sampleorgjson = fh.org(resource)
        typ = fh.type(resource)
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
                    self.err(f"there is no json org for derived sample {sampleid}")
                else:
                    # OE im JSON angegeben
    
                    # check ob OE des Probanden aus DB mit OE im JSON übereinstimmt
    
                    # old, does this work?
                    patorgq = """
                    SELECT OU.CODE as 'organisationunit.code' FROM CENTRAXX_IDCONTAINER IDC 
                    INNER JOIN CENTRAXX_PATIENTORGUNIT POU ON IDC.PATIENTCONTAINER=POU.PATIENTCONTAINER_OID 
                    INNER JOIN CENTRAXX_IDCONTAINERTYPE IDCT ON IDC.IDCONTAINERTYPE=IDCT.OID 
                    INNER JOIN CENTRAXX_ORGANISATIONUNIT OU ON POU.ORGUNIT_OID=OU.OID 
                    WHERE OU.CODE != 'NUM' AND IDCT.CODE=? AND IDC.PSN=?
    
                    """
    #                patorgq = """ # with patientcontainer
    #                select ou.code as 'organisationunit.code' from centraxx_idcontainer idc
    #                inner join centraxx_patientcontainer pc on idc.patientcontainer=pc.oid
    #                inner join centraxx_patientorgunit pou on pou.patientcontainer_oid=pc.oid
    #                inner join centraxx_organisationunit ou on pou.orgunit_oid=ou.oid
    #                inner join centraxx_idcontainertype idct on idc.idcontainertype=idct.oid
    #                where ou.code != 'NUM' and idct.code=? and idc.psn=?
    #                """
                    """
                    dq query:
                    centraxx_idcontainer {
                      .psn[=?],
                      .patientcontainer(i) {
                          <centraxx_patientorgunit(i).orgunit_oid(i).code[!='NUM']
                       },
                      .idcontainertype(i).code[=?]
                    }
                    """
                    psn = fh.limspsn(resource)
                    res = self.db.qfad(patorgq, "LIMSPSN", psn)
                    patorg = None
                    if len(res) > 0:
                       patorg = res[0]['organisationunit.code'] # todo ist es immer LIMSPSN?
    
                    # do the orgs of patient and sample match?
                    if sampleorgjson != patorg: # todo print patient psn
                        self.err(f"organisation units don't match for patient and sample {sampleid}, json org of sample is {sampleorgjson}, db org of its patient is {patorg}")
    
        # Aliquotgruppe: OE nicht notwendig
