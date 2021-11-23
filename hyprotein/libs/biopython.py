from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser

from hyprotein.protein.interfaces import IPDBstructure

class Biopython(IPDBstructure):
    def __init__(self, name, path, pdb_format, lib) -> None:
        self.__version__ = ['Biopython', Bio_version]
        self.protein = name
        self.name = lib
        self.path = f"{path}{self.protein}.{pdb_format}"
        self.pdb = self.PDB.pdb(self.protein, self.path)
        self.residues = self.PDB.residues(self.pdb.lib)

    def show(self):
        p,protein,pdb = self.pdb.unpack()
        chains = pdb.get_chains()
        for chain in chains:
            residues = list(chain.get_residues())
            p[protein][chain.id] = {res.id[1]:res.resname for res in residues}
        return p

    def dihedrals(self):
        d = dict()
        p,protein,pdb = self.pdb.unpack()

        for chains in pdb.get_chains():
            chain = chains.id
            p[protein][chain] = {}
            for res in pdb.get_residues():
                resname = res.resname
                id = res.id[1]

                phi = res.internal_coord.get_angle('phi')
                phi = round(phi, 5) if phi else None

                psi = res.internal_coord.get_angle('psi')
                psi = round(psi, 5) if psi else None

                p[protein][chain].update({
                    (id,resname): {
                        'phi': phi,
                        'psi': psi
                    }
                })

        return p

    class PDB:
        def __init__(self, *args, **kwargs) -> None:
            for key in kwargs:
                setattr(self, key, kwargs[key])

        @classmethod
        def pdb(cls, protein, path):
            pdb = PDBParser().get_structure(protein, path)[0]
            pdb.atom_to_internal_coordinates()
            chains = pdb.get_chains()

            to_dict = {
                protein: {
                    chain.id: None for chain in chains
                }
            }

            def unpack():
                """unpack() method returns a tuple with three values:

                protein: protein's name
                to_dict: dictionary structure of protein
                pdb: biopython PDB object

                """
                return (to_dict,protein,pdb)

            attr = {
                'protein': protein,
                'lib': pdb,
                'to_dict': to_dict,
                'unpack':unpack
            }
            return cls(**attr)

        @classmethod
        def residues(cls, pdb):
            residues = list(pdb.get_residues())
            total = len(residues)
            attr = {
                'total': total,
                'list': residues,
            }
            return cls(**attr)