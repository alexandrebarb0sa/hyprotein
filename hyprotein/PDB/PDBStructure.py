from hyprotein.PDB.PDBObject import PDBobject
from .PDBData import PDBData

class Structure(PDBobject):
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
        view = PDBData(protein).pandas()
        return view

    def dihedrals(self):
        """
        .dihedrals() method
        """
        PDB = self.get_lib()
        protein = PDB.dihedrals()
        view = PDBData(protein).pandas()
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

        return PDBData(protein).pandas()

    def __repr__(self) -> str:
        if hasattr(self, 'resname'):
            return f"<Residue {self.resname} id: {self.id}>"
        elif hasattr(self, 'total'):
            return f"<hyProtein {self.name.upper()} Residues: {self.total}>"
