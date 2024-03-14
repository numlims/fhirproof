# FhirCheck is the base class for fhir checks

import sys

import fhirhelp as fh
# from traction import *

class FhirCheck:

    def __init__(self, fp):
        self.fp = fp
        # take db and traction from fhirproof for shorter notation
        self.db = fp.db
        self.tr = fp.tr

    # info is an info log shortcut
    def info(self, message):
        self.fp.log.info(f"{self.__class__.__name__}: {message}")

    # err is an error log shortcut
    def err(self, message):
        self.fp.ok = False # this run is not ok
        self.fp.log.error("{self.__class__.__name__}: {message}")

    # debug is an error log shortcut
    def debug(self, message):
        self.fp.log.debug("{self.__class__.__name__}: {message}")
        
