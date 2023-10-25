# FhirCheck is the base class for fhir checks

import logging
from pathlib import Path
import sys

import fhirhelp as fh
from traction import *

class FhirCheck:

    def __init__(self):
        # setup a logger to write to a file into logs folder
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        # log to file
        file_handler = logging.FileHandler( Path.joinpath(Path(__file__).parent.parent, 'logs/fhirproof.log'))
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        # log to stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(formatter)
        log.addHandler(stdout_handler)

    # info is an info log shortcut
    def info(message):
        log.info(message)

    # error is an error log shortcut
    def error(message):
        log.error(message)

    # debug is an error log shortcut
    def debug(message):
        log.debug(message)
        
