# automatically generated, DON'T EDIT. please edit OUCheck.ct from where this file stems.
import re

from dip import dig
from fhirproof.FhirCheck import *
from fhirproof.fhirhelp import fhirhelp as fh
import tr
class OUCheck(FhirCheck):
    def __init__(self, fp):
        """
        """
        FhirCheck.__init__(self, fp)
    def _check(self, dborga, jsonorga, sampleid):
        """
         _check checks whether db orga and json orga of sample match.
        """
        if dborga == None:
            self.err(f"no organisation in db for sample {sampleid}")
        if jsonorga == None:
            self.err(f"no organisation in json for sample {sampleid}")
        if dborga != jsonorga:
            self.err(f"organisation units don't match for sample {sampleid}, json orga is {jsonorga}, db orga is {dborga}")
    def check(self, entry):
        """
         check starts the check.
        """
        super().check(entry)
        if self.db == None:
            return 
        resource = dig(entry, "resource")
    
        sampleid = fh.sampleid(resource)
    
        res = self.fp.tr.sample(sampleids=[sampleid], verbose=[tr.orga])
        trsample = None
        if len(res) > 0:
          trsample = res[0]
        sampleorgjson = fh.org(resource)
        typ = fh.type(resource)
        if trsample != None and typ == "MASTER":
            if sampleorgjson != None:
                self._check(trsample.orga, sampleorgjson, sampleid)
        elif typ == "DERIVED": 
            if trsample != None:
                if sampleorgjson != None:
                    self._check(trsample.orga, sampleorgjson, sampleid)
            else:
                if sampleorgjson == None:
                    self.err(f"there is no json org for derived sample {sampleid}")
                else:
                    patorgq = """
                    SELECT OU.CODE as 'organisationunit.code' FROM CENTRAXX_IDCONTAINER IDC 
                    INNER JOIN CENTRAXX_PATIENTORGUNIT POU ON IDC.PATIENTCONTAINER=POU.PATIENTCONTAINER_OID 
                    INNER JOIN CENTRAXX_IDCONTAINERTYPE IDCT ON IDC.IDCONTAINERTYPE=IDCT.OID 
                    INNER JOIN CENTRAXX_ORGANISATIONUNIT OU ON POU.ORGUNIT_OID=OU.OID 
                    WHERE OU.CODE != 'NUM' AND IDCT.CODE=? AND IDC.PSN=?
                    """
                    psn = fh.limspsn(resource)
                    res = self.db.qfad(patorgq, "LIMSPSN", psn)
                    patorg = None
                    if len(res) > 0:
                       patorg = res[0]['organisationunit.code'] # todo ist es immer LIMSPSN?
                    if sampleorgjson != patorg: # todo print patient psn
                        self.err(f"organisation units don't match for patient and sample {sampleid}, json org of sample is {sampleorgjson}, db org of its patient is {patorg}")
