from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser
from pandas.core.algorithms import value_counts

from hyprotein.protein.interfaces import IPDBstructure

class Biopython(IPDBstructure):
    def __init__(self, name, path, pdb_format, lib) -> None:
        self.__version__ = ['Biopython', Bio_version]
        self.name = name
        self.lib = lib
        self.path = f"{path}{name}.{pdb_format}"
        self.pdb = PDBParser().get_structure(self.name, self.path)[0]
        self.pdb.atom_to_internal_coordinates()

        # self.pdb = self.PDB.pdb(name, self.path)
        # self.residues = self.PDB.residues(self.pdb)

    def to_dict(self):
        name = self.name

        protein = {
            name: {
                chain.id: None for chain in list(self.pdb.get_chains())
            }
        }        

        for chain in self.pdb.get_chains():
            c = chain.id
            residues = list(chain.get_residues())
            protein[name][c] = {res.id[1]:{'residue':res.resname} for res in residues}
        return protein

    def show(self):
        return self.to_dict()

    def dihedrals(self):
        protein = self.to_dict()
        name = self.name

        for chain in self.pdb.get_chains():
            residues = chain.get_residues()
            c = chain.id
            for res in residues:
                r = res.id[1]

                phi = res.internal_coord.get_angle('phi')
                phi = round(phi,5) if isinstance(phi,float) else phi
                psi = res.internal_coord.get_angle('psi')
                psi = round(psi,5) if isinstance(psi,float) else psi

                protein[name][c][r] = {
                    'residue':res.resname,
                    'phi': phi,
                    'psi': psi
                }

        return protein

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