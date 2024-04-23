all: fhirproof.py

fhirproof.py: fhirproof.ct
	ct fhirproof.ct
