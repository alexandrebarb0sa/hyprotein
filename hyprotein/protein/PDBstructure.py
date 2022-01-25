from re import A
import pandas as pd
from ..libs.interfaces import Interface
from .PDBobject import PDB


class PDBstructure(Interface):
    """
    PDBstructure class
    """

    def __init__(self):
        self.pdb = PDB.get()
        self.residues = PDBresidues(self.pdb)

    def show(self):
        """
        .show() method
        """
        protein = self.pdb.lib.show()
        view = PDBview(protein).pandas()

        return view

    def dihedrals(self):
        """
        .dihedrals() method
        """
        protein = self.pdb.lib.dihedrals()
        view = PDBview(protein).pandas()

        return view

    def set_angle(self, chain, res_id, angle_key, value):
        ...
        # residue = self.pdb.lib.set_angle(res,angle)


class PDBresidues:
    """
    PDBresidues class
    """

    def __init__(self,pdb=None,*args, **kwargs) -> None:
        if pdb:
            self.total = pdb.lib.residues.total
            self.protein = pdb.name

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def get(self):
        protein = self.pdb.lib.to_dict()
        name = self.pdb.name
        for chain in protein[name]:
            for id,resname in protein[name][chain].items():
                attr = self.pdb.lib.residues.constructor(chain,id)
                protein[name][chain][id]['residue'] = self.__get_residues(attr)
        return PDBview(protein).pandas()

    @classmethod
    def __get_residues(cls, attr):
        return cls(**attr)                

    def __repr__(self) -> str:
        if hasattr(self, 'resname'):
            return f"<Residue {self.resname} id: {self.id}>"
        elif hasattr(self, 'total'):
            return f"<hyProtein {self.protein.upper()} Residues: {self.total}>"


class PDBview:
    def __init__(self, protein) -> None:
        self.protein = protein
        self.name = list(self.protein.keys())[0]

    def to_dict(self):
        if isinstance(self.protein, dict):
            return self.protein

    def pandas(self):
        protein, name = self.protein, self.name
        # protein[name].update({'B':dict(list(protein[name]['A'].items())[0:5])})
        chains = list(protein[name].keys())
        columns = list(list(protein[name][chains[0]].values())[0].keys())

        idx = {chain: None for chain in chains}
        res = {chain: None for chain in chains}

        for chain in chains:
            id = protein[name][chain].keys()
            res[chain] = protein[name][chain].values()

            idx[chain] = pd.MultiIndex.from_product([list(chain), id])

            idx[chain] = [
                (name,) + x for x in idx[chain].values
            ]

            idx[chain] = pd.Index(idx[chain])

        idx = idx.values()
        idx = [item for chain in idx for item in chain]
        idx = pd.Index(idx, name=('PROTEIN', 'CHAIN', 'RES_ID'))

        res = res.values()

        data = [item for residues in res for item in residues]
        data = [d.values() for d in data]

        df = pd.DataFrame(data=data, columns=columns, index=idx)

        return df
