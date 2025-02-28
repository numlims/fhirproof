
import json

from dig import *
from AqtMatCheck import *
from PrimaryInDbCheck import *
from DatesCheck import *
from LocationCheck import *
from BehealterCheck import *
from OUCheck import *
from ParentingCheck import *
from PsnCheck import *
from RestmengeCheck import *
from DerivmatCheck import *
from MayUserEditOUCheck import *
from fhirhelp import fhirhelp as fh
import logging
import sys
from traction import *



# fhirproof reads fhir json from stdin and checks the entries
class fhirproof:

    # these variables are accessible to the fhirchecks
    entrybyfhirid = {} # entries referenced by fullUrl / fhirids, e.g. "Specimen/1037700"
    entrybysampleid = {} # entries referenced by sampleid
    shouldzerorest = {} # should restmenge be zero
    aqtgchildless = {} # is a aliquotgroup without children?


    # parent returns the entry's parent entry resource, if there is one, else none
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



    def _setuplog(self, logdir):
        # setup a logger to write to a file into logs folder
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        # log to file
        if logdir == "":
            # logdir = Path.joinpath(Path(__file__).parent.parent, 'logs/')
            logdir = "../logs"
        # file_handler = logging.FileHandler(Path.joinpath(logdir, 'fhirproof.log'))
        file_handler = logging.FileHandler(logdir + "/fhirproof.log")
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # log to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        log.addHandler(stdout_handler)
        self.log = log


    # init inits fhirproof with db target, input file, centraxx user, log dir and config
    def __init__(self, target, file, user, logdir, config=None):

        self.target = target
        # connect to db
        self.db = dbcq(target)
        # traction for queries
        self.tr = traction(self.db)

        # sys.stdin works on powershell
        textin = ""         # maybe use textin = open(0).read()
        for line in file:
            textin += line

        # the other args
        self.textin = textin
        self.user = user
        self.logdir = logdir
        
        # is the input ready for centraxx import?
        self.ok = True


    

  




