# FhirCheck is the base class for fhir checks

import sys

from fhirhelp import fhirhelp as fh
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
        self.fp.log.error(f"{self.__class__.__name__}: {message}")

    # debug is an error log shortcut
    def debug(self, message):
        self.fp.log.debug(f"{self.__class__.__name__}: {message}")
        
