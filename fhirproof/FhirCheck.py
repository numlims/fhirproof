# automatically generated, DON'T EDIT. please edit FhirCheck.ct from where this file stems.
import sys

from fhirproof.fhirhelp import fhirhelp as fh
from dip import dig, dis
# from traction import *
class FhirCheck:

    def __init__(self, fp):
        """
        """
        self.fp = fp

        self.db = fp.db
        self.tr = fp.tr
    def check(self, entry):
        """
         check remembers the entry so its filename can be accessed by the log functions.
        """
        self.entry = entry
    # info is an info log shortcut
    def info(self, message):
        """
        """
        self.fp.log.info(f"{dig(self.entry, '_filename')}: {self.__class__.__name__}: {message}")
    # err is an error log shortcut
    def err(self, message):
        """
        """
        self.fp.ok = False # this run is not ok
        self.fp.log.error(f"{dig(self.entry, '_filename')}: {self.__class__.__name__}: {message}")
    # debug is an error log shortcut
    def debug(self, message):
        """
        """
        self.fp.log.debug(f"{dig(self.entry, '_filename')}: {self.__class__.__name__}: {message}")
        
