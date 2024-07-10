all: fhirproof.py AqtMatCheck.py DatesCheck.py DerivmatCheck.py FhirCheck.py LocationCheck.py MayUserEditOUCheck.py OUCheck.py ParentingCheck.py PsnCheck.py

fhirproof.py: fhirproof.ct
	ct fhirproof.ct
AqtMatCheck.py: AqtMatCheck.ct
	ct AqtMatCheck.ct
BehealterCheck.py: BehealterCheck.ct
	ct BehealterCheck.ct
DatesCheck.py: DatesCheck.ct
	ct DatesCheck.ct
DerivmatCheck.py: DerivmatCheck.ct
	ct DerivmatCheck.ct
FhirCheck.py: FhirCheck.ct
	ct FhirCheck.ct
LocationCheck.py: LocationCheck.ct
	ct LocationCheck.ct
MayUserEditOUCheck.py: MayUserEditOUCheck.ct
	ct MayUserEditOUCheck.ct
OUCheck.py: OUCheck.ct
	ct OUCheck.ct
ParentingCheck.py: ParentingCheck.ct
	ct ParentingCheck.ct
PsnCheck.py: PsnCheck.ct
	ct PsnCheck.ct
