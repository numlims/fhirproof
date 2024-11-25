# proofnmove.py 
# for dd
# this was thought of as a shell script, but for now it seems to be a quick way to get output from fhirproof.

from fhirproof import Fhirproof
import os
import sys

target = sys.argv[1] # db target
# name of fhir user
user = sys.argv[3]
logdir = sys.argv[4]

fp = Fhirproof(target, sys.stdin, user, logdir)
ok = fp.run()
if ok:
    print("fhirproof says ok")
    os.system("echo 'i would move files now'")

    #os.system(""" cmd.exe \c 'C:\applications\centraxx-home\fhir-custom-export\move_files.bat 
    #          "C:\applications\centraxx-home\fhir-custom-export\num_dd\import" "C:\kairos\FHIR-Importer\Dresden" 
    #          "C:\kairos\FHIR-Importer\start_dresden_import.bat" ' """)
    os.system(""" C:\applications\centraxx-home\fhir-custom-export\move_files.bat 
              "C:\applications\centraxx-home\fhir-custom-export\num_dd\import" "C:\kairos\FHIR-Importer\Dresden" 
              "C:\kairos\FHIR-Importer\start_dresden_import.bat" """)
else:
    print("fhirproof says not ok, see in logs")
# os.system("echo 'hello proofnmove'")

# cmd.exe /c 'C:\applications\centraxx-home\fhir-custom-export\move_files.bat "C:\applications\centraxx-home\fhir-custom-export\num_dd\import" "C:\kairos\FHIR-Importer\Dresden" "C:\kairos\FHIR-Importer\start_dresden_import.bat"'
