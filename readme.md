# fhirproof: fhir import checker

fhirproof checkt, ob FHIR Json Dateien ins Centraxx importiert werden
können.

```
fhirproof [specimen|observation] <json dir> --db <db target> --user <user> --log <logfile>
```

example:

```
fhirproof specimen specimen-dir --db num_prod --user numwuerzfhir --log fp.log
```

Sieh auch `fhirproof -h`.

## Install

Das .whl von [releases](https://github.com/numlims/fhirproof/releases)
downloaden und mit pip installieren:

```
pip install fhirproof-<version>.whl
```

Installieren aus source:

```
make install
```

## Dev

Der Code kann aus den .ct Dateien mit
[ct](https://github.com/tnustrings/codetext/releases) oder mit [ct
fuer
vscode](https://marketplace.visualstudio.com/items?itemName=tnustrings.codetext)
generiert werden.

Make die .ct Dateien mit `make`.

## Checks

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


## license

[cc0](https://creativecommons.org/publicdomain/zero/1.0/)