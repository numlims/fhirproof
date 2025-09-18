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

    # sampleid tries to find the sample id in resource
    # Die Datenbankabfrage braucht die Sample-ID. `sample_id` sucht die
    # `SAMPLEID` im Json. Dafür gehen wir über das `identifier` Feld. Die
    # `SAMPLEID` ist derjenige `identifier`, in dessen `type.coding` Array
    # ein `code` `SAMPLEID` ist.
    @staticmethod
    def sampleid(resource):
        # print("resource has identifier: " + str(resource.has("identifier")))
        #print(f"typeof resource: {fhirhelp.type(resource)}")
        if "identifier" not in resource:
            #print(f"type(resource): {type(fhirhelp.resource)}")
            if fhirhelp.type(resource) != "ALIQUOTGROUP":
                # raise Exception("no identifier") # todo remove
                # print("maybe error: entry " + entry.get("fullUrl") + " is not aliquotgroup and has no identifier field (needed for sampleid).")
                print("maybe error: resource is not aliquotgroup and has no identifier field (needed for sampleid).") # todo put in entry/fullUrl here or some other identifier?
                return None
            #  sampleid = pyjq('.identifier | .[] | select(.type.coding[0].code == "SAMPLEID") | .value | tonumber', resource)
        if "identifier" not in resource:
            return None
        for identifier in dig(resource, "identifier"):
            if dig(identifier, "type/coding") == None:
                continue
            for coding in dig(identifier, "type/coding"):
                if dig(coding, "code") == "SAMPLEID":
                    return dig(identifier, "value")
        return None

    @staticmethod
    def resourceType(resource):
        """resourceType returns the resource type, Specimen or Observation."""
        return dig(resource, "resourceType")
    
