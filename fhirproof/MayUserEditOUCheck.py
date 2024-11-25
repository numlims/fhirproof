from dig import *
from FhirCheck import *
from fhirhelp import fhirhelp as fh


class MayUserEditOUCheck(FhirCheck):
    def __init__(self, fp):
        FhirCheck.__init__(self, fp)


    # check checks whether user may edit the entry
    def check(self, entry, user):
        resource = dig(entry, 'resource')
        # get org unit
        orgunit = fh.org(resource)
        query = """
        select * from centraxx_participantorgunitano as poa
        join centraxx_participant as p on p.oid = poa.creator
        join centraxx_organisationunit as ou where poa.organisation = ou.oid
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




