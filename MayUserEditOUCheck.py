# MayUserEditOECheck checks whether the user who does the fhir import is allowed to edit organisations-einheiten (OEs)

from FhirCheck import *

"""
Es sollte geprüft werden, ob der später zu verwendende FHIR-Import-User berechtigt ist, OEs der Proben und Probanden, die im JSON-enthalten sind, zu bearbeiten.

Dafür ist der spätere Import-User als Parameter an das Skript zu übergeben
Die Zuordnung eines Users zu OEs ist in CENTRAXX_PARTICIPANTORGUNITANO gespeichert.
User in CENTRAXX_PARTICIPANT

"""

class MayUserEditOUCheck(FhirCheck):

    # check checks whether user may edit the entry
    def check(self, entry, user):
        resource = entry['resource']
        # get org unit
        orgunit = fh.org(resource)
        query = """
        select * from centraxx_participantorgunitano as poa
        join centraxx_participant as p on p.oid = poa.creator
        join centraxx_organisationunit as ou where poa.organisation = ou.oid
        where p.username = ? and ou.code = ?
        """
        result = qfad(query, user, orgunit)
        if len(result) == 0:
            self.err("user " + user + " may not edit the sample")
            return
