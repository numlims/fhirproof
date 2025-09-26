from dip import dig, dis
class fhirhelp:
    @staticmethod
    def lagerort(resource):
        for e in dig(resource, "extension"):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocation":
                # return e["valueReference"]["identifier"]["value"]
                for ee in dig(e, "extension"):
                    if dig(ee, "url") == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                        return dig(ee, "valueString")
        return None
    @staticmethod
    def limspsn(resource):
        for coding in dig(resource, "subject/identifier/type/coding"):
            if dig(coding, "code") == "LIMSPSN":
                return dig(resource, "subject/identifier/value")
    @staticmethod
    def material(resource):
        return dig(resource, "type/coding/0/code")
    @staticmethod
    def parent_fhirid(resource):
        if not "parent" in resource:
            return None
        return dig(resource, "parent/0/reference") # there should only be one parent, so one element in the array
    @staticmethod
    def parent_sampleid(resource):
        if "parent" in resource:
            for parent in dig(resource, "parent"):
                if not "identifier" in parent:
                    continue
                for coding in dig(parent, "identifier/type/coding"):
                    if dig(coding, "code") == "SAMPLEID":
                        return dig(parent, "identifier/value") # pid: parent id
        return None
    @staticmethod
    def org(resource):
        for e in dig(resource, "extension"):
            # if re.match("organizationUnit", e["url"]):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sample/organizationUnit":
                return dig(e, "valueReference/identifier/value")
        return None
    @staticmethod
    def restmenge(resource):
        # pres = DictPath(resource)
        #if not "value" in resource["container"][0]["specimenQuantity"]:
        #    return None
        #return resource["container"][0]["specimenQuantity"]["value"]
        return dig(resource, "container/0/specimenQuantity/value")
    @staticmethod
    def type(resource):
        if dig(resource, "extension") == None:
            return None
        for e in dig(resource, "extension"):
            if dig(e, "url") == "https://fhir.centraxx.de/extension/sampleCategory":
                return dig(e, "valueCoding/code")
        return None
    @staticmethod
    def sampleid(resource):
        return dig(fhirhelp.identifiers(resource), "SAMPLEID")
    @staticmethod
    def identifiers(resource):
        out = {}
        if "identifier" not in resource:
            return None
        for identifier in dig(resource, "identifier"):
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
        return dig(resource, "resourceType")

