# automatically generated, DON'T EDIT. please edit FhirCheck.ct from where this file stems.
import sys

from dip import dig, dis
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
    def info(self, message):
        """
         info is an info log shortcut.
         
         when called in subclasses, super().check(entry) must be called first
         (especially in end-checks when err refers to different entries), so
         that the log message gives the file name of the corresponding entry.
        """
        self.fp.log.info(f"{dig(self.entry, '_filename')}: {self.__class__.__name__}: {message}")
    def err(self, message, entry=None):
        """
         err is called when an error was found for a sample.  it logs the
         error message, and changes fp.ok und fp._accept to record the error.
         
         when called in subclasses, super().check(entry) must be called first
         (especially in end-checks when err refers to different entries), so
         that the log message gives the file name of the corresponding entry.
        """
        self.fp.ok = False # this run is not ok
        filename = dig(self.entry, '_filename')
        self.fp._accept[filename] = False
        self.fp.log.error(f"{filename}: {self.__class__.__name__}: {message}")
    def debug(self, message):
        """
         debug is an error log shortcut.
         
         when called in subclasses, super().check(entry) must be called first
         (especially in end-checks when debug refers to different entries), so
         that the log message gives the file name of the corresponding entry.
        """
        self.fp.log.debug(f"{dig(self.entry, '_filename')}: {self.__class__.__name__}: {message}")
        
