import os
import uuid
import time
import json
from .assign3Files.assign3cup import a3cup
from .assign3Files.assign3lex import a3lex

class assignment3:
    def __init__(self, subprocess, lex_code, cup_code, stduID):
        self.subprocess = subprocess
        self.lex_code = lex_code
        self.cup_code = cup_code
        self.stduID = stduID

    def run_a3(self):
        lex = a3lex()
        cup = a3cup()
        return f'lex: {lex} <br><br> cup: {cup} <br> stdudentID: {self.stduID}'

