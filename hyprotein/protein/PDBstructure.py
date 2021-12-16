import pandas as pd
from .interfaces import IPDBstructure
from .PDBobject import PDB

class PDBstructure(IPDBstructure):
    """
    PDBstructure class
    """

    def __init__(self,pdb):
        self.pdb = pdb
        # self.residues = PDBresidues.info(pdb)

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

class PDBresidues:
    """
    PDBresidues class
    """

    def __init__(self, *args, **kwargs) -> None:
        for key in kwargs:
            setattr(self, key, kwargs[key])

    # Factory function to do a class initialization with different purposes

    @classmethod
    def info(cls, pdb):
        attr = {
            'protein': pdb.name,
            'total': pdb.lib.residues.total
        }
        return cls(**attr)

    @classmethod
    def residue(cls, resname, ID):
        attr = {
            'resname': resname,
            'id': ID,
        }
        return cls(**attr)

    def __repr__(self) -> str:
        if hasattr(self, 'resname'):
            return f"<hyProtein {self.resname} ID: {self.id}>"
        elif hasattr(self, 'protein'):
            return f"<hyProtein {self.protein.upper()} Residues: {self.total}>"

class PDBview:
    def __init__(self,protein) -> None:
        self.protein = protein
        self.name = list(self.protein.keys())[0]

    def to_dict(self):
        if isinstance(self.protein,dict):
            return self.protein
        
    def pandas(self):
        protein,name = self.protein,self.name
        # protein[name].update({'B':dict(list(protein[name]['A'].items())[0:5])})
        chains = list(protein[name].keys())
        columns = list(list(protein[name][chains[0]].values())[0].keys())

        idx = {chain:None for chain in chains}
        res = {chain:None for chain in chains}

        for chain in chains:
            id = protein[name][chain].keys()
            res[chain] = protein[name][chain].values()

            idx[chain] = pd.MultiIndex.from_product([list(chain),id])

            idx[chain] = [
                (name,) + x for x in idx[chain].values
            ]

            idx[chain] = pd.Index(idx[chain])

        idx = idx.values()
        idx = [item for chain in idx for item in chain]
        idx = pd.Index(idx, name=('PROTEIN','CHAIN','RES_ID'))

        res = res.values()

        data = [item for residues in res for item in residues]
        data = [d.values() for d in data]

        df = pd.DataFrame(data=data,columns=columns,index=idx)

        return df
        