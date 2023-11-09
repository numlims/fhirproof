# fhirproof: fhir import checker

fhirproof checkt, ob FHIR Json Dateien ins Centraxx importiert werden
können und loggt errors in `logs/fhirproof.log`.

# Checks

## Primärprobe in DB: PrimaryInDbCheck

Wenn die Probe eine Primärprobe (MASTER) im Json ist, sollte es sie
schon in der Datenbank geben. Derived Proben muss es nicht unbedingt
schon in der Datenbank geben, sie können neu dazu kommen.

## Zeitangaben: DatesCheck

Proben sollten in dieser zeitlichen Reihenfolge verarbeitet werden: 

Abnahme (Collection) [bei Primär]<br/>
Laboreingang (Received)  <br/>
Zentrifugation [wenn da] <br/>
Aliquotierung (Derival) [bei Aliquoten]   <br/>

## Proben-Container: BehealterCheck

Primärproben sollen Originalcontainer sein, Aliquot-Deriveds NUM
Aliquotcontainer.

## Lagerort: LocationCheck

Gibt es den Lagerort in der DB? Für alle Aliquot-Deriveds ist der
Lagerort angegeben, außer ihre Restmenge ist null. Bei Primärproben
ist nur bei Speichel und PaxGene ein Lagerort angegeben.

Der Lagerort muss existieren und etwas anderes als UserWorkspace sein.

## Zentrifugationsart

Todo: Es wird geprüft, ob die Zentrifugationsart die in den Json Daten
angegeben ist auch in der DB existiert.

## Organisationsunit von Patient und Probe: OrgCheck

Die Organisationunit vom Patienten der Probe muss die selbe sein.

## Childless Aliquot Group: ParentingCheck

Aliquotgruppen sollen nicht ohne Deriveds sein, die an ihnen hängen.

## LIMS-Pseudonym: PsnCheck

Das LIMS-Pseudonym (Limspsn) für den Patienten der in der DB zum
Sample gehört soll das gleiche wie im Json sein.

Wenn das Sample ein Derived/Aliquot ist, soll die Limspsn im
Json-Parent die gleiche sein.

## Restmenge: RestmengeCheck

Bei Masters mit Aliquoten soll die Restmenge null sein, bei Masters
ohne Aliquote soll die Restmenge groesser null sein.

## Material: DerivmatCheck

Das Material eines Entries soll seinem Parent Entry entsprechen,
sofern es einen Parent gibt. Ist der Entry ein Derived (Aliquot), muss
es das gleiche Material sein wie seine Parent-Aliquotgroup.

Das Code-Klarnamen Mapping kann man über die Datenbank abfragen,
indem man von `sampletype.code` zu `multilingualentry.value` über die
verbindende Tabelle `sampletype_ml_name` geht.

    select st.code, ml.value from centraxx_sampletype st
      inner join centraxx_sampletype_ml_name stml on stml.related_oid
      = st.oid
      inner join centraxx_multilingualentry ml on stml.oid = ml.oid
        order by st.code, ml.lang desc

Ohne order by ml.lang kommt manchmal Deutsch zuerst, manchmal English.

Die Namen zu den Codes sind im Anhang.

## Test

Eine kleine Testdatei ist angebrannt.json. Da drin nach den _comment
Feldern suchen, z.B. die Zeiten sind kaputt.

Dateien aus vorangegangenen Importen mit denen man testen kann liegen
in test-dresden und test-wuerz. In Dresden ist die Reihenfolge
kaputt, in Wuerzburg die Master Sample Ids.

Auf dem Test-Applikations-Server liegen Import Dateien in
C:\applications\centraxx-home\fhir-custom-export\num_wuerz\import\CASE*
 und in C:\applications\kairos\FHIR-Importer\Dresden\error

## Log

A little shell pipeline for extracting certain sampleids from the
logfile is in `scripts/sampleids-from-log.sh`.

## Down the line

Vielleicht eine groovy Version zum Einbinden in Centraxx.

## Anhang

Codes und Namen. 

| Code | Name English | Name German |
| ---- | ---- | ---- |
| BLD | Whole Blood | Vollblut |
| CIT | Citrate | Citrat |
| CITLEFTOVER | unnamed (CITLEFTOVER) | Citrat (Restmaterial) |
| DHZB_BLDRNASTABIL | unnamed (DHZB_BLDRNASTABIL) | Blut RNA stabilisiert |
| DHZB_ZB | unnamed (DHZB_ZB) | Zelluläre Blutbestandteile |
| EDTA | EDTA-Plasma | EDTA-Plasma |
| EDTABUF | Buffy Coat | Buffy Coat |
| EDTALEFTOVER | unnamed (EDTAREST) | EDTA-Plasma (Restmaterial) |
| EDTAWB | Whole Blood EDTA | EDTA Vollblut |
| GEW | unnamed (GEW) | Gewebe |
| LH | unnamed (LH) | Lithium-Heparin |
| MYOCARD | unnamed (MYOCARD) | Myocardbiopsie |
| NUM_bal | BAL | BAL |
| NUM_balc | BAL cells | BAL-Zellen |
| NUM_balf | BAL fluid | BAL-Überstand |
| NUM_CPT_PL | unnamed (NUM_CPT_PL) | CPT-Plasmaüberstand |
| NUM_DNA | unnamed (NUM_DNA) | DNA |
| NUM_enta | endotracheal suction | Trachealsekret |
| NUM_haare | Hair | Haare |
| NUM_heppl | Heparin plasma | Heparin-Plasma |
| NUM_liquor | Liquor | Liquor |
| NUM_liquorc | CSF cells | Liquor Zellen |
| NUM_liquorf | CSF supernatant | Liquor Überstand |
| NUM_nasen-rachenabstrich | Nasopharyngeal swab | Nasopharyngealabstrich |
| NUM_pax | PAX-Gene | PAX-Gene |
| NUM_pbmc | PBMC | PBMC |
| NUM_PBMC_C | PBMC cells | PBMC Zellen |
| NUM_pbmc_cpt | CPT for PBMC | CPT für PBMC |
| NUM_pbmc_edta | EDTA for PBMC | EDTA für PBMC |
| NUM_PBMC_EDTAPL | EDTA plasma PBMC | PBMC EDTA-Plasma |
| NUM_pbmc_hep | PBMC Heparin | Heparin für PBMC |
| NUM_PCR | unnamed (NUM_PCR) | PCR-Abstrich |
| NUM_rachenabstrich | Oropharyngeal swab | Oropharyngealabstrich |
| NUM_RAG | unnamed (NUM_RAG) | Schnelltest-Abstrich |
| NUM_RNA | unnamed (NUM_RNA) | RNA |
| NUM_speichel | Saliva | Speichel |
| NUM_sputum | Sputum | Sputum |
| NUM_stuhl | Stool | Stuhl |
| NUM_urinf | Urine fluid | Urin-Überstand |
| NUM_urins | urine sediment | Urin-Sediment |
| NUM_wange | Cheek swab | Wangenabstrich |
| NUM_ZB | unnamed (NUM_ZB) | Zellulaere Blutbestandteile |
| PAXgene | PAXgene (Vollblut) | PAXgene |
| SER | Serum | Serum |
| Tempus | unnamed (Tempus™ Blood RNA Tube) | Tempus™ Blood RNA (Vollblut) |
| URN | Urine | Urin |
