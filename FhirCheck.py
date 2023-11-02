# FhirCheck is the base class for fhir checks

import sys

import fhirhelp as fh
from traction import *

class FhirCheck:

    def __init__(self, fp):
        self.fp = fp

    # info is an info log shortcut
    def info(self, message):
        self.fp.log.info(self.__class__.__name__ + ": " + message)

    # err is an error log shortcut
    def err(self, message):
        self.fp.log.error(self.__class__.__name__ + ": " + message)

    # debug is an error log shortcut
    def debug(self, message):
        self.fp.log.debug(self.__class__.__name__ + ": " + message)
        
