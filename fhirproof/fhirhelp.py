# fhirhelp.py offers help functions for fhir json bundles.

# it offers these functions:
# lagerort
# limspsn
# material
# parent_fhirid
# parent_sampleid
# org
# restmenge
# resourceType
# sampleid
# type

# Die Doku für das Specimen-Json ist auf Simplifier,
# https://simplifier.net/CentraXX-Structures/Specimen/~details.

# to import, say: from fhirhelp import fhirhelp as fh

from dip import dig, dis

class fhirhelp:
    
    # lagerort gets the sampleLocation
    @staticmethod
    def lagerort(resource):
        for e in dig(resource, "extension"):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocation":
                # return e["valueReference"]["identifier"]["value"]
                for ee in dig(e, "extension"):
                    if dig(ee, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                        return dig(ee, "valueString")
        return None

    # limspsn gets the lims psn of the patient
    @staticmethod
    def limspsn(resource):
        for coding in dig(resource, "subject/identifier/type/coding"):
            if dig(coding, "code") == "LIMSPSN":
                return dig(resource, "subject/identifier/value")

    # material returns the material type of the resource
    @staticmethod
    def material(resource):
        return dig(resource, "type/coding/0/code")

    # parent_fhirid gets the fhirid of the parent from resource
    @staticmethod
    def parent_fhirid(resource):
        if not "parent" in resource:
            return None
        return dig(resource, "parent/0/reference") # there should only be one parent, hence one element in the array

    # parent_sampleid gets the sample id of the parent
    @staticmethod
    def parent_sampleid(resource):
        # try to fetch parent from json
        if "parent" in resource:
            for parent in dig(resource, "parent"):
                if not "identifier" in parent:
                    continue
                for coding in dig(parent, "identifier/type/coding"):
                    if dig(coding, "code") == "SAMPLEID":
                        return dig(parent, "identifier/value") # pid: parent id
        return None

    # org returns the organisation or None if no organisation.
    @staticmethod
    def org(resource):
        for e in dig(resource, "extension"):
            # if re.match("organizationUnit", e["url"]):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/organizationUnit":
                return dig(e, "valueReference/identifier/value")
        return None

    # restmenge returns the restmenge of the sample
    @staticmethod
    def restmenge(resource):
        # pres = DictPath(resource)
        #if not "value" in resource["container"][0]["specimenQuantity"]:
        #    return None
        #return resource["container"][0]["specimenQuantity"]["value"]
        return dig(resource, "container/0/specimenQuantity/value")

    # type returns the type from resource, 'MASTER', or 'ALIQUOTGROUP', or 'DERIVED'
    # `type` findet den Probentyp. Es läuft die Extensions der `resource`
    # durch und geben den `valueCoding.code` zurück wenn wir einem `valueCoding`
    # Feld begegnen. In der DB steht der Type in DType. (Verwirrenderweise
    # heißt das Material in der Datenbank auch Type, das ist hier nicht
    # gemeint).
    @staticmethod
    def type(resource):
        #    return len([e for e in resource["extension"] if "valueCoding" in e and e["valueCoding"]["code"] == typ]) > 0
        # if no extension return none
        if dig(resource, "extension") == None:
            return None
        for e in dig(resource, "extension"):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sampleCategory":
                return dig(e, "valueCoding/code")
        return None

    @staticmethod
    def sampleid(resource):
        """sampleid returns the sample id of a resource."""
        return dig(fhirhelp.identifiers(resource), "SAMPLEID")

    @staticmethod
    def identifiers(resource):
        """identifiers returns the identifiers of a resource as dict keyed by the identifier codes, eg:
        { "SAMPLEID": "abc", "EXTSAMPLEID": "cde" }
        """
        out = {}
        if "identifier" not in resource:
            return None
        for identifier in dig(resource, "identifier"):
            # ziehe den code (SAMPLEID, EXTSAMPLEID, etc) aus dem type/coding array
            codings = dig(identifier, "type/coding")
            if codings == None:
                continue
            for coding in codings:
                if dig(coding, "system") == "urn:centraxx":
                    # take the code as key. the value is a field of identifier.
                    key = dig(coding, "code")
                    out[key] = dig(identifier, "value")
        return out

    @staticmethod
    def resourceType(resource):
        """resourceType returns the resource type, Specimen or Observation."""
        return dig(resource, "resourceType")
    
