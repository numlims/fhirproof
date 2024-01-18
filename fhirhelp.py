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

# lagerort gets the sampleLocation
def lagerort(resource):
    for e in resource["extension"]:
        if e["url"] == "https://fhir.centraxx.de/extension/sample/sampleLocation":
            # return e["valueReference"]["identifier"]["value"]
            for ee in e["extension"]:
                if ee["url"] == "https://fhir.centraxx.de/extension/sample/sampleLocationPath":
                    return ee["valueString"]
    return None

# limspsn gets the lims psn of the patient
def limspsn(resource):
    for coding in resource["subject"]["identifier"]["type"]["coding"]:
        if coding["code"] == "LIMSPSN":
            return resource["subject"]["identifier"]["value"]

# material returns the material type of the resource
def material(resource):
    return resource["type"]["coding"][0]["code"]

# parent_fhirid gets the fhirid of the parent from resource
def parent_fhirid(resource):
    if not "parent" in resource:
        return None
    return resource["parent"][0]["reference"] # there should only be one parent, hence one element in the array
  
# parent_sampleid gets the sample id of the parent 
def parent_sampleid(resource):
    # try to fetch parent from json
    if "parent" in resource:
        for parent in resource["parent"]:
            if not "identifier" in parent:
                continue
            for coding in parent["identifier"]["type"]["coding"]:
                if coding["code"] == "SAMPLEID":
                    return parent["identifier"]["value"] # pid: parent id
    return None

# org returns the organisation or None if no organisation.
def org(resource):
    for e in resource["extension"]:
        # if re.match("organizationUnit", e["url"]):
        if e["url"] == "https://fhir.centraxx.de/extension/sample/organizationUnit":
            return e["valueReference"]["identifier"]["value"]
    return None

# restmenge returns the restmenge of the sample
def restmenge(resource):
    if not "value" in resource["container"][0]["specimenQuantity"]:
        return None
    return resource["container"][0]["specimenQuantity"]["value"]

# sampleid tries to find the sample id in resource
# Die Datenbankabfrage braucht die Sample-ID. `sample_id` sucht die
# `SAMPLEID` im Json. Dafür gehen wir über das `identifier` Feld. Die
# `SAMPLEID` ist derjenige `identifier`, in dessen `type.coding` Array
# ein `code` `SAMPLEID` ist.
def sampleid(resource):
    if "identifier" not in resource:
        if type(resource) != "ALIQUOTGROUP":
            print("maybe error: entry " + entry["fullUrl"] + " is not aliquotgroup and has no identifier field (needed for sampleid).")
            return None
        #  sampleid = pyjq('.identifier | .[] | select(.type.coding[0].code == "SAMPLEID") | .value | tonumber', resource)
    if "identifier" not in resource:
        return None
    for identifier in resource["identifier"]:
        for coding in identifier["type"]["coding"]:
            if coding["code"] == "SAMPLEID":
                return identifier["value"]
    return None

# type returns the type from resource, 'MASTER', or 'ALIQUOTGROUP', or 'DERIVED'
# `type` findet den Probentyp. Es läuft die Extensions der `resource`
# durch und geben den `valueCoding.code` zurück wenn wir einem `valueCoding`
# Feld begegnen. In der DB steht der Type in DType. (Verwirrenderweise
# heißt das Material in der Datenbank auch Type, das ist hier nicht
# gemeint).
def type(resource):
    #    return len([e for e in resource["extension"] if "valueCoding" in e and e["valueCoding"]["code"] == typ]) > 0
    for e in resource["extension"]:
        if "valueCoding" in e:
            return e["valueCoding"]["code"]
    return None

  


