from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser

from hyprotein.protein.PDBstructure import PDBstructure

class Biopython(PDBstructure):
    def __init__(self,name,path,pdb_format) -> None:
        self.info = ['Biopython',Bio_version]
        self.name = name
        self.path = f"{path}{name}.{pdb_format}"

    def get_structure(self):
        self.pdb = PDBParser().get_structure(self.name,self.path)[0]
        self.pdb.atom_to_internal_coordinates()
        self.__chains = self.pdb.child_dict

    @property
    def chains(self,msg):
        print(msg)
        return list(self.__chains.keys())

    def residues(self,chain):
        r = {c:None for c in list(self.__chains.keys())}
        return r

    def show(self):
        ...

    def dihedrals(self):
        ...
