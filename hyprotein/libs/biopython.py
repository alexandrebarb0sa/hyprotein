from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser
from pandas.core.algorithms import value_counts

from hyprotein.protein.interfaces import IPDBstructure

class Biopython(IPDBstructure):
    def __init__(self, name, path, pdb_format, lib) -> None:
        self.__version__ = ['Biopython', Bio_version]
        self.protein = name
        self.name = lib
        self.path = f"{path}{self.protein}.{pdb_format}"
        self.pdb = self.PDB.pdb(self.protein, self.path)
        self.residues = self.PDB.residues(self.pdb)

    def show(self):
        protein,name,pdb = self.pdb.unpack()
    
        chains = pdb.get_chains()
        for chain in chains:
            residues = list(chain.get_residues())
            protein[name][chain.id] = {res.id[1]:res.resname for res in residues}
        return protein

    def dihedrals(self):
       ...


    class PDB:
        def __init__(self, *args, **kwargs) -> None:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        @classmethod
        def pdb(cls, name, path):
            pdb = PDBParser().get_structure(name, path)[0]
            pdb.atom_to_internal_coordinates()

            protein = {
                name: {
                    chain.id: None for chain in list(pdb.get_chains())
                }
            }
            
            for chain in pdb.get_chains():
                protein[name][chain.id] = list(chain.get_residues())

            def unpack():
                """unpack() method returns a tuple with three values:

                name: protein's name
                protein: dictionary structure of protein
                pdb: biopython PDB object

                """
                return (protein.copy(),name,pdb)

            attr = {
                'name': name,
                'protein': protein,
                'lib':pdb,
                'unpack':unpack
            }
            return cls(**attr)

        @classmethod
        def residues(cls, pdb):
            pdb = pdb.lib
            residues = list(pdb.get_residues())
            total = len(residues)
            attr = {
                'total': total,
                'list': residues,
            }
            return cls(**attr)