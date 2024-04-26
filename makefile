all: fhirproof.py DatesCheck.py

fhirproof.py: fhirproof.ct
	ct fhirproof.ct

DatesCheck.py: DatesCheck.ct
	ct DatesCheck.ct
