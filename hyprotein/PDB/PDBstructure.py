import pandas as pd

from hyprotein.PDB.PDBobject import PDBobject
from .PDBview import PDBview

class PDBstructure(PDBobject):
    """
    PDBstructure class
    """

    def __init__(self,pdb):
        self.level = "Structure"
        self.pdb = pdb
        # self.residues = PDBresidues.info(self.name)
        PDBobject.__init__(self,pdb)

    def show(self):
        """
        .show() method
        """
        PDB = self.get_lib()
        protein = PDB.show()
        view = PDBview(protein).pandas()

        return view

    def dihedrals(self):
        """
        .dihedrals() method
        """
        PDB = self.get_lib()
        protein = PDB.dihedrals()
        view = PDBview(protein).pandas()
        return view

    def set_angle(self, chain, res_id, angle_key, value):
        self.get_lib().set_angle(chain, res_id, angle_key, value)
        prompt = [f"<hyProtein:",
                  f"{self.pdb.upper()}",
                  f"Chain: {chain}",
                  f"Residue: {res_id}",
                  f"{angle_key}={value}>"
                  ]
        return ' '.join(prompt)


class PDBresidues:
    """
    PDBresidues class
    """

    def __init__(self, *args, **kwargs) -> None:
        for key in kwargs:
            setattr(self, key, kwargs[key])

    @classmethod
    def info(cls, name):
        attr = {
            'name': name,
            'total': PDB.get(name).lib.residues.total
        }
        return cls(**attr)

    def get(self):
        name = self.name
        protein = PDB.get(name).lib.to_dict()
        attr = {
            'resname': None,
            'id': None,
            'chain': None,
        }
        attr1 = None
        for chain in protein[name]:
            for id, resname in protein[name][chain].items():
                lib_attr = PDB.get(name).lib.residues.repr(chain, id)
                try:
                    assert attr.keys() == lib_attr.keys()
                    attr = dict(zip(attr, lib_attr.values()))
                    protein[name][chain][id]['residue'] = PDBresidues(**attr)
                except AssertionError as err:
                    print('Attributes from lib not matching!')
                    exit()

        return PDBview(protein).pandas()

    def __repr__(self) -> str:
        if hasattr(self, 'resname'):
            return f"<Residue {self.resname} id: {self.id}>"
        elif hasattr(self, 'total'):
            return f"<hyProtein {self.name.upper()} Residues: {self.total}>"


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
