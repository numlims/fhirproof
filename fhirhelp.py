# fhirhelp.py offers help functions for fhir json bundles.

# it offers these functions:
# lagerort
# limspsn
# material
# parent_fhirid
# parent_sampleid
# org
# restmenge
# sampleid
# type

# Die Doku für das Specimen-Json ist auf Simplifier,
# https://simplifier.net/CentraXX-Structures/Specimen/~details.

# from dict_path import DictPath # todo whole input as DictPath?

# lagerort gets the sampleLocation
def lagerort(resource):
    for e in resource.get("extension"):
        if e.get("url") == "https://fhir.centraxx.de/extension/sample/sampleLocation":
            # return e["valueReference"]["identifier"]["value"]
            for ee in e.get("extension"):
                if ee.get("url") == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                    return ee.get("valueString")
    return None

# limspsn gets the lims psn of the patient
def limspsn(resource):
    for coding in resource.get("subject/identifier/type/coding"):
        if coding.get("code") == "LIMSPSN":
            return resource.get("subject/identifier/value")

# material returns the material type of the resource
def material(resource):
    return resource.get("type/coding/0/code")

# parent_fhirid gets the fhirid of the parent from resource
def parent_fhirid(resource):
    if not "parent" in resource:
        return None
    return resource.get("parent/0/reference") # there should only be one parent, hence one element in the array
  
# parent_sampleid gets the sample id of the parent 
def parent_sampleid(resource):
    # try to fetch parent from json
    if "parent" in resource:
        for parent in resource.get("parent"):
            if not "identifier" in parent:
                continue
            for coding in parent.get("identifier/type/coding"):
                if coding.get("code") == "SAMPLEID":
                    return parent.get("identifier/value") # pid: parent id
    return None

# org returns the organisation or None if no organisation.
def org(resource):
    for e in resource.get("extension"):
        # if re.match("organizationUnit", e["url"]):
        if e.get("url") == "https://fhir.centraxx.de/extension/sample/organizationUnit":
            return e.get("valueReference/identifier/value")
    return None

# restmenge returns the restmenge of the sample
def restmenge(resource):
    # pres = DictPath(resource)
    #if not "value" in resource["container"][0]["specimenQuantity"]:
    #    return None
    #return resource["container"][0]["specimenQuantity"]["value"]
    return resource.get("container/0/specimenQuantity/value")

# sampleid tries to find the sample id in resource
# Die Datenbankabfrage braucht die Sample-ID. `sample_id` sucht die
# `SAMPLEID` im Json. Dafür gehen wir über das `identifier` Feld. Die
# `SAMPLEID` ist derjenige `identifier`, in dessen `type.coding` Array
# ein `code` `SAMPLEID` ist.
def sampleid(resource):
    if "identifier" not in resource:
        if type(resource) != "ALIQUOTGROUP":
            # print("maybe error: entry " + entry.get("fullUrl") + " is not aliquotgroup and has no identifier field (needed for sampleid).")
            print("maybe error: resource is not aliquotgroup and has no identifier field (needed for sampleid).") # todo put in entry/fullUrl here or some other identifier?
            return None
        #  sampleid = pyjq('.identifier | .[] | select(.type.coding[0].code == "SAMPLEID") | .value | tonumber', resource)
    if "identifier" not in resource:
        return None
    for identifier in resource.get("identifier"):
        for coding in identifier.get("type/coding"):
            if coding.get("code") == "SAMPLEID":
                return identifier.get("value")
    return None

# type returns the type from resource, 'MASTER', or 'ALIQUOTGROUP', or 'DERIVED'
# `type` findet den Probentyp. Es läuft die Extensions der `resource`
# durch und geben den `valueCoding.code` zurück wenn wir einem `valueCoding`
# Feld begegnen. In der DB steht der Type in DType. (Verwirrenderweise
# heißt das Material in der Datenbank auch Type, das ist hier nicht
# gemeint).
def type(resource):
    #    return len([e for e in resource["extension"] if "valueCoding" in e and e["valueCoding"]["code"] == typ]) > 0
    for e in resource.get("extension"):
        if "valueCoding" in e:
            return e.get("valueCoding/code")
    return None

  


