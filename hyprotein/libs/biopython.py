from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser
from pandas.core.algorithms import value_counts

from hyprotein.libs.interface import Interface

class Biopython(Interface):
    def __init__(self, pdb, pdb_dir, pdb_format=".pdb") -> None:
        self.__version__ = ['Biopython', Bio_version]
        self.lib_name = 'biopython'
        self.pdb = pdb
        self.dir = f"{pdb_dir}/{pdb}{pdb_format}"
        self.lib = PDBParser().get_structure(self.pdb, self.dir)[0]
        self.lib.atom_to_internal_coordinates()
        self.residues = self.Residues(self.lib)
        # self.residues.get(id,chain)

    def to_dict(self):
        pdb = self.pdb
        protein = {
            pdb: {
                chain.id: None for chain in list(self.lib.get_chains())
            }
        }
        for chain in self.lib.get_chains():
            c = chain.id
            residues = list(chain.get_residues())
            protein[pdb][c] = {res.id[1]: {'residue': res.resname}
                                for res in residues}
        return protein

    def show(self):
        return self.to_dict()

    def dihedrals(self):
        protein = self.to_dict()
        pdb = self.pdb

        for chain in self.lib.get_chains():
            residues = chain.get_residues()
            c = chain.id
            for res in residues:
                #Verifying if res is not a HETATM
                if res.id[0].strip():
                    ...
                else:
                    r = res.id[1]
                    phi = res.internal_coord.get_angle('phi')
                    phi = round(phi, 5) if isinstance(phi, float) else phi

                    phi = res.internal_coord.get_angle('phi')
                    phi = round(phi, 5) if isinstance(phi, float) else phi
                    psi = res.internal_coord.get_angle('psi')
                    psi = round(psi, 5) if isinstance(psi, float) else psi

                    protein[pdb][c][r] = {
                        'residue': res.resname,
                        'phi': phi,
                        'psi': psi
                    }
        return protein

    def set_angle(self, chain, res_id, angle_key, value):
        self.residues.get(chain,res_id).internal_coord.set_angle(
            angle_key, value)
            
    class Residues:
        def __init__(self, lib) -> None:
            self.lib = lib
            self.total = len(list(self.lib.get_residues()))

        def repr(self, chain, id):
            for res in self.lib.child_dict[chain]:
                if id in res.id:
                    attr = {
                        'resname': res.resname,
                        'id': res.id[1],
                        'chain': res.parent.id,
                    }
                    return attr

        def get(self,chain,res_id):
            for res in self.lib.child_dict[chain]:
                if res_id in res.id:
                    return res
