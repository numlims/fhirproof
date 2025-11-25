# automatically generated, DON'T EDIT. please edit test_db.ct from where this file stems.
from fhirproof import fhirproof
def test_db():
    """
     test_db tests fhirproof against db.
    """
    fp = fhirproof("num_prod", "numddfhir", "test/fp.log", configpath="config.yaml")
    ok = fp.check("test/in", "latin-1")
    assert ok == True
