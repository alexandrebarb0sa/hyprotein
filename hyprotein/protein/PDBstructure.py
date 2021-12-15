import pandas as pd
from .interfaces import IPDBstructure
from .PDBobject import PDB

class PDBstructure(IPDBstructure):
    """
    PDBstructure class
    """

    def __init__(self):
        pdb = PDB.get()
        self.name = pdb.name
        self.residues = PDBresidues.info(pdb)

    def show(self):
        """
        show() method
        """
        pdb = PDB.get(self.name)
        name = pdb.name
        p = pdb.lib.show()

        chains = p[name].keys()

        for chain in chains:
            count = 0
            for res_id,resname in p[name][chain].items():
                p[name][chain][res_id] = PDBresidues.residue(resname, res_id)
                count += 1
        return p

    def dihedrals(self):
        """
        dihedrals() method
        """
        pdb = PDB.get(self.name).lib
        pdb = pdb.dihedrals()
        print(pdb)
        return ''


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
