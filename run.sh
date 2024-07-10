cat ../concat.gen.json | python3 fhirproof.py num_prod numddfhir --log-dir logs

cat ../data/asavespecimen/2023-11-01_18-50-02-964-Specimen_P0.json | python3 fhirproof.py num_prod numddfhir --log-dir logs
