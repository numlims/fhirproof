# automatically generated, DON'T EDIT. please edit MayUserEditOUCheck.ct from where this file stems.
from dip import dig
from fhirproof.FhirCheck import *
from figs import specimen as figs
class MayUserEditOUCheck(FhirCheck):
    def __init__(self, fp):
        """
         __init__ inits the check.
        """
        FhirCheck.__init__(self, fp)
    def check(self, entry, user):
        """
         check checks whether the fhir import user may edit the orga that is
         named in the entry.
        """
        super().check(entry)
        if self.db is None or user is None:
            return
        resource = dig(entry, 'resource')
        orgunit = figs.orga(resource)
        query = """
        select p.username from centraxx_participantorgunitano as poa
        join centraxx_participant as p on p.oid = poa.participant
        join centraxx_organisationunit as ou on poa.organisation = ou.oid
        where p.username = ? and ou.code = ?
        """

        """ dq query:
        select centraxx_participantorgunitano.* {
            .creator.username[ = ?],
            .organisation.code[ = ?]
        } 
        """
        result = self.db.qfad(query, user, orgunit)
        if len(result) == 0:
            self.err(f"user {user} may not edit the sample")
            return 
