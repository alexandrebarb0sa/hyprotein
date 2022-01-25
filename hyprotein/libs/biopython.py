from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser
from pandas.core.algorithms import value_counts

from hyprotein.libs.interfaces import Interface

class Biopython(Interface):
    def __init__(self, name, path, pdb_format, lib) -> None:
        self.__version__ = ['Biopython', Bio_version]
        self.name = name
        self.lib = lib
        self.path = f"{path}{name}.{pdb_format}"
        self.biopython = PDBParser().get_structure(self.name, self.path)[0]
        self.biopython.atom_to_internal_coordinates()
        self.residues = self.Residues(self.biopython)

        # self.residues.get(id,chain)

    def to_dict(self):
        name = self.name
        protein = {
            name: {
                chain.id: None for chain in list(self.biopython.get_chains())
            }
        }
        for chain in self.biopython.get_chains():
            c = chain.id
            residues = list(chain.get_residues())
            protein[name][c] = {res.id[1]:{'residue':res.resname} for res in residues}
        return protein

    def show(self):
        return self.to_dict()

    def dihedrals(self):
        protein = self.to_dict()
        name = self.name

        for chain in self.biopython.get_chains():
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

    def set_angle(self,chain,res_id,angle_key,value):
        self.residues.get(res_id,chain).internal_coord.set_angle(angle_key,value)

    class Residues:
        def __init__(self,biopython) -> None:
            self.__biopython = biopython
            self.total = len(list(self.__biopython.get_residues()))

        def constructor(self,chain,id):
            for res in self.__biopython.child_dict[chain]:
                if id in res.id:
                    attr = {
                        'resname': res.resname,
                        'id': res.id[1],
                        'chain': res.parent.id,
                        # 'set_angle': res.internal_coord.set_angle,
                        # 'get_angle': res.internal_coord.get_angle,
                    }                                        
                    return attr