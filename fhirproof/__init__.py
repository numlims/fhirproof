
import tr
from dbcq import dbcq
import yaml
from dip import dig
from figs import specimen as fgs
from tram import Sample
import fhirio

from fhirproof.AmountUnitCheck import *
from fhirproof.AqtMatCheck import *
from fhirproof.PrimaryInDbCheck import *
from fhirproof.DatesCheck import *
from fhirproof.LocationCheck import *
from fhirproof.BehealterCheck import *
from fhirproof.OUCheck import *
from fhirproof.ParentingCheck import *
from fhirproof.PsnCheck import *
from fhirproof.RestmengeCheck import *
from fhirproof.DerivmatCheck import *
from fhirproof.MayUserEditOUCheck import *
from fhirproof.IdContainerCheck import *
from fhirproof.PrimaryMatCheck import *
from fhirproof.ObsMasterdataCheck import *
import os
import json
import logging
import sys

# fhirproof reads fhir json from stdin and checks the entries
class fhirproof:

    # these variables are accessible to the fhirchecks
    entrybyfhirid = {} # entries referenced by fhirid (fullUrl), e.g. "Specimen/1037700"
    entrybysampleid = {} # entries referenced by sampleid
    shouldzerorest = {} # should restmenge be zero
    aqtgchildless = {} # is a aliquotgroup without children?
    _accept = {} # was this file without errors? keyed by filename.
    def __init__(self, dbtarget, user, logfile, configpath:str=None, loglevel:str="INFO", quiet:bool=False):
        self.dbtarget = dbtarget

        self.db = None
        self.tr = None
        if dbtarget != None:
            self.db = dbcq(dbtarget)
            self.tr = tr.traction(self.db)
        self.user = user
        self.logfile = logfile
        self._setuplog(logfile, loglevel, quiet)
        with open(configpath, "r") as file:
             self.config = yaml.safe_load(file)
        self.ok = True

    def check(self, dir, encoding="utf-8"):
        entries = fhirio.read_entries(dir, encoding, keep_filenames=True)
        self.check_entries(entries)
        accepted = []
        for k, v in self._accept.items():
            if v == True:
                accepted.append(k)
        return self.ok, accepted

    def check_entries(self, entries):
        self.ok = True

        self.log.info(f"START CHECK")
        self.log.info(f"starting check against {self.dbtarget}")
        amountunit = AmountUnitCheck(self)
        aqtmat = AqtMatCheck(self)
        primary_in_db = PrimaryInDbCheck(self)
        dates = DatesCheck(self)
        location = LocationCheck(self)
        behealter = BehealterCheck(self)
        ou = OUCheck(self)
        parenting = ParentingCheck(self)
        psn = PsnCheck(self)
        restmenge = RestmengeCheck(self)
        derivmat = DerivmatCheck(self)
        mayeditou = MayUserEditOUCheck(self)
        idcontainer = IdContainerCheck(self)
        primmat = PrimaryMatCheck(self)
        labvalmasterobs = ObsMasterdataCheck(self)
        master_count = 0        
        aqtg_count = 0
        derived_count = 0
        pat_count = 0
        for entry in entries:
            self._accept[entry["_filename"]] = True
        currentfile = ""
        # run checks
        for entry in entries:
            if currentfile != dig(entry, "_filename"):
                currentfile = dig(entry, "_filename")
                self.log.info(str(currentfile) + ": checking file")
            # keep arrays up to date
            self.entrybyfhirid[fgs.full_url(entry)] = entry

            resource = fgs.resource(entry)
            if fgs.resource_type(resource) == "Specimen":
              if fgs.category(resource) == "ALIQUOTGROUP":
                  aqtg_count += 1
                  if not fgs.full_url(entry) in self.aqtgchildless: # tmp way to prohibit overwrites
                      self.aqtgchildless[fgs.full_url(entry)] = True
                  aqtmat.check(entry)
  
              # print(f"entry resource: {json.dumps(fgs.resource(entry))}")
              sampleid = fgs.sampleid(resource)
              if sampleid == None:
                  continue
              res = self.tr.sample(sampleids=[sampleid], verbose_all=True)
              dbsample:Sample = None
              if len(res) > 0:
                  dbsample = res[0]
              self.entrybysampleid[sampleid] = entry
  
              if fgs.category(resource) == "MASTER":
                  master_count += 1
              if fgs.category(resource) == "DERIVED":
                  derived_count += 1
              if fgs.category(resource) == "PATIENT":
                  pat_count += 1
              sampletype = fgs.type(resource)
              trial = self._trial_from_orga(fgs.orga(resource))
              # amount units
              if not self._skip(type(amountunit).__name__, trial, sampletype):
                  amountunit.check(entry, dbsample)
              # primary in db
              if not self._skip(type(primary_in_db).__name__, trial, sampletype):
                  primary_in_db.check(entry, dbsample)
              # dates
              if not self._skip(type(dates).__name__, trial, sampletype):
                  dates.check(entry, dbsample)
              # location
              if not self._skip(type(location).__name__, trial, sampletype):  
                  location.check(entry, dbsample)
              # behealter
              if not self._skip(type(behealter).__name__, trial, sampletype):
                  behealter.check(entry, dbsample)
              # org
              if not self._skip(type(ou).__name__, trial, sampletype):
                  ou.check(entry, dbsample)
              # parenting
              if not self._skip(type(parenting).__name__, trial, sampletype):
                  parenting.check(entry, dbsample)
              # psn
              if not self._skip(type(psn).__name__, trial, sampletype):
                  psn.check(entry, dbsample)
              # restmenge
              if not self._skip(type(restmenge).__name__, trial, sampletype):
                  restmenge.check(entry, dbsample)
              # derived material
              if not self._skip(type(derivmat).__name__, trial, sampletype):
                  derivmat.check(entry, dbsample)
              # edit oe
              if not self._skip(type(mayeditou).__name__, trial, sampletype):            
                  mayeditou.check(entry, self.user)
              # id container
              if not self._skip(type(idcontainer).__name__, trial, sampletype):
                  idcontainer.check(entry, dbsample)
              # primary material
              if not self._skip(type(primmat).__name__, trial, sampletype):
                  primmat.check(entry, dbsample)
            elif fgs.resource_type(resource) == "Observation":
              trial = None
              sampletype = None
              if not self._skip(type(labvalmasterobs).__name__, trial, sampletype):
                  labvalmasterobs.check(entry)

        restmenge.end()
        parenting.end()
        self.log.info(f"ended check against {self.dbtarget}: " +
            str(pat_count) + " patients, " +
            str(master_count) + " master samples, " +        
            str(aqtg_count) + " aliquot groups, " +
            str(derived_count) + " derived samples, " + 
            str(len(entries)) + " total" )
        
        return self.ok # written by FhirCheck.err()

    def _setuplog(self, logfile, loglevel, quiet:bool=False):
        log = logging.getLogger(__name__)            
        log.setLevel(loglevel)
        file_handler = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        if not quiet:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(formatter)
            log.addHandler(stdout_handler)
        self.log = log
    def parent(self, entry):
        parent = None
        resource = entry['resource']
        if fgs.category(resource) != "DERIVED":              
            return None
        # get fhirid of aliquotgroup-parent
        parent_fhirid = fgs.parent_fhirid(resource)
        if parent_fhirid == None:
            return None
        elif parent_fhirid not in self.entrybyfhirid:
            return None
        return self.entrybyfhirid[parent_fhirid]['resource']
    def _skip(self, classname:str, trial:str, sampletype:str) -> bool:
        if classname is None or trial is None or sampletype is None:
            return False
        skipchecks = dig(self.config, f"skip/{trial}/{sampletype}")
        if skipchecks is None:
            return False
        return classname in skipchecks or "*" in skipchecks
    def _trial_from_orga(self, orga:str):
        if re.match(r"^s-snid", orga):
            return "NUM S-SNID"
        elif re.match(r"REVIVE$", orga):
            return "RAPID_REVIVE"
        else:
            return None
