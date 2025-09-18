
import tr
from dbcq import dbcq
from dip import dig
from fhirproof.fhirhelp import fhirhelp as fh

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
import os
import json
import logging
import sys

# fhirproof reads fhir json from stdin and checks the entries
class fhirproof:

    # these variables are accessible to the fhirchecks
    entrybyfhirid = {} # entries referenced by fullUrl / fhirids, e.g. "Specimen/1037700"
    entrybysampleid = {} # entries referenced by sampleid
    shouldzerorest = {} # should restmenge be zero
    aqtgchildless = {} # is a aliquotgroup without children?
    # init inits fhirproof with db target, input file, centraxx user, log file and config
    def __init__(self, dbtarget, user, logfile, config=None, pamm=None):

        self.dbtarget = dbtarget

        # connect to db if target given
        self.db = None
        self.tr = None
        if dbtarget != None:
            self.db = dbcq(dbtarget)
            # traction for queries
            self.tr = tr.traction(self.db)

        self.user = user
        self.logfile = logfile

        self._setuplog(logfile)

        # remember the pamm path
        self.pamm_path = pamm
        
        # is the input ready for centraxx import?
        self.ok = True

    def check(self, dir, encoding=None):
    
      # the collected entries
      entries = self.entries_from_dir(dir, encoding)
    
      self.check_entries(entries)
    #`check_specimens``
    #`check_observations``

    def check_entries(self, entries):
        self.ok = True

        self.log.info(f"starting check against {self.dbtarget}")
        # initialize checks
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

        # count for some stats
        aqtg_count = 0
        master_count = 0
        derived_count = 0
        # run checks
        for entry in entries:
            # keep arrays up to date
            self.entrybyfhirid[dig(entry, "fullUrl")] = entry

            resource = dig(entry, "resource")
            if fh.resourceType(resource) == "Specimen":
              if fh.type(dig(entry, 'resource')) == "ALIQUOTGROUP":
                  aqtg_count += 1
                  if not dig(entry, "fullUrl") in self.aqtgchildless: # tmp way to prohibit overwrites
                      self.aqtgchildless[dig(entry, "fullUrl")] = True
                  aqtmat.check(entry)
  
              # print(f"entry resource: {json.dumps(dig(entry, 'resource'))}")
              sampleid = fh.sampleid(dig(entry, 'resource'))
              if sampleid == None:
                  continue
              self.entrybysampleid[sampleid] = entry
  
              if fh.type(dig(entry, 'resource')) == "DERIVED":
                  derived_count += 1
              if fh.type(dig(entry, 'resource')) == "MASTER":
                  master_count += 1
              # primary in db
              primary_in_db.check(entry)
              # dates
              dates.check(entry)
              # location
              location.check(entry)
              # behealter
              behealter.check(entry)
              # org
              ou.check(entry)
              # parenting
              parenting.check(entry)
              # psn
              psn.check(entry)
              # restmenge
              restmenge.check(entry)
              # derived material
              derivmat.check(entry)
              # edit oe?
              # mayeditou.check(entry, self.user)
            elif fh.resourceType(resource) == "Observation":
              print("todo check observation")

        restmenge.end()
        parenting.end()
        self.log.info(f"ended against {self.dbtarget}: "+
            str(aqtg_count) + " aliquot groups, " +
            str(master_count) + " master samples, " +
            str(derived_count) + " derived samples, " +
            str(len(entries)) + " total\n" )
        
        return self.ok # written by FhirCheck.err()
    #`check_observation_entries

    def _setuplog(self, logfile):
        # setup a logger to write to a file into logs folder
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        file_handler = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # log to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        log.addHandler(stdout_handler)
        self.log = log
    def entries_from_dir(self, dir, encoding=None): # todo could be static?
    
      if encoding == None:
        encoding = "utf-8"
    
      entries = []
      
      files = os.listdir(dir)
      for file in files:
        #with open(os.path.join(dir, file), "r", encoding="latin-1") as f:
        with open(os.path.join(dir, file), "r", encoding=encoding) as f:    
          jsonin = json.load(f)
    
          for entry in dig(jsonin, "entry"):
            entries.append(entry)
      return entries
    
    def parent(self, entry):
        parent = None
        resource = entry['resource']
        if fh.type(resource) != "DERIVED":              
            return None
        # get fhirid of aliquotgroup-parent
        pfhirid = fh.parent_fhirid(resource)
        if pfhirid == None:
            return None
        elif pfhirid not in self.entrybyfhirid:
            return None
        return self.entrybyfhirid[pfhirid]['resource']
  
