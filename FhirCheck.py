# FhirCheck is the base class for fhir checks

import sys

import fhirhelp as fh
from traction import *

class FhirCheck:

    def __init__(self, fp):
        self.fp = fp

    # info is an info log shortcut
    def info(self, message):
        self.fp.log.info(message)

    # err is an error log shortcut
    def err(self, message):
        self.fp.log.error(message)

    # debug is an error log shortcut
    def debug(self, message):
        self.fp.log.debug(message)
        
