from Bio import __version__ as Bio_version
from Bio.PDB import PDBList, Selection, Polypeptide, vectors
from Bio.PDB.PDBParser import PDBParser

from hyprotein.libs.interface import Interface

class Biopython(Interface):
    __version__ = ['Biopython', Bio_version]
    libname = "biopython"
    def __init__(self, id, **kwargs) -> None:
        self.id = id
        pdb_format = kwargs.get('pdb_format','pdb')
        dir = f"{kwargs.get('dir')}/{id}.{pdb_format}"
        self.api = PDBParser().get_structure(self.id, dir)[0]
        self.api.atom_to_internal_coordinates()
        self.residues = self.Residues(self.api)
        self.residues_total = len(list(self.api.get_residues()))
        # self.residues.get(id,chain)

    # Represents protein in dict form
    @property
    def protein2dict(self):
        pdb = self.id
        protein = {
            pdb: {
                chain.id: None for chain in list(self.api.get_chains())
            }
        }
        for chain in self.api.get_chains():
            c = chain.id
            _residues = list(chain.get_residues())
            protein[pdb][c] = {res.id[1]: {
                'res': res.resname,
                'het': res.id[0]
                } for res in _residues}
        return protein

    def dihedrals(self):
        protein = self.protein2dict
        pdb = self.id

        for chain in self.api.get_chains():
            residues = chain.get_residues()
            c = chain.id
            for res in residues:
                #Verify if res is a HETATM
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

                    # _res = res.__class__.__repr__
                    # res.__class__.__repr__ = self.__repr(res)

                    protein[pdb][c][r] = {
                        'res': res.resname,
                        'het': res.id[0],
                        'phi': phi,
                        'psi': psi
                    }

                    # res.__class__.__repr__ = _res

        return protein

    def set_angle(self, chain, res_id, angle_key, value):
        self.residues.get(chain,res_id).internal_coord.set_angle(
            angle_key, value)

    def get_angle(self, chain, res_id, angle_key):
        return self.residues.get(chain, res_id).internal_coord.get_angle(
            angle_key)

    def __repr(self,res):
        return lambda res: f"{res.resname}"
            
    class Residues:
        def __init__(self, lib) -> None:
            self.api = lib
            self.total = len(list(self.api.get_residues()))

        def repr(self, chain, id):
            for res in self.api.child_dict[chain]:
                if id in res.id:
                    attr = {
                        'resname': res.resname,
                        'id': res.id[1],
                        'chain': res.parent.id,
                    }
                    return attr

        def get(self,chain,res_id):
            for res in self.api.child_dict[chain]:
                if res_id in res.id:
                    return res
