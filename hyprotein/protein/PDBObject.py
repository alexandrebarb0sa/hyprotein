from ..libs import *
from .PDBstructure import PDBstructure

class PDBobject:
    def __init__(self,name,path,lib,pdb_format):
        self.name = name
        self.path = path
        self.lib = lib
        self.format = pdb_format

    def get_structure(self):
        PDBlib = self.parse_lib()
        return PDBstructure(self.name,PDBlib)

    def parse_lib(self):
        if self.lib == "biopython":
            return Biopython(self.name,self.path,self.format)
