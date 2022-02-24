from hyprotein.PDB.PDBObject import PDBObject
from .PDBData import PDBData
from hyprotein import _utils

class Structure(PDBObject):
    """
    Structure class
    """
    level = "S"
    def __init__(self,pdb):
        # Keep this order
        self.pdb = pdb
        PDBObject.__init__(self,pdb)
        #--------------------------

    @property
    def residues(self):
        Residues = _utils.namedtuple("Residues",["pdb","total"])
        return Residues(self.pdb,self.from_lib.residues_total)

    @property
    def protein(self):
        try:
            if self.__protein:
                ...
        except AttributeError:
            parse = self.from_lib.protein
            self._repr_residue(parse)
        return self.__protein

    def _repr_residue(self,parse):
        protein = parse
        pdb = self.pdb
        chains = protein[self.pdb].keys()
        for c in chains:
            for res_id in protein[pdb][c]:
                protein[pdb][c][res_id]['RESIDUE'] = PDBresidue(
                    id=res_id,
                    resname=protein[pdb][c][res_id]['RESIDUE'],
                    parent=c
                )
        self.__protein = protein        
        return self.__protein

    def show(self):
        """
        show() method
        """
        view = PDBData(self.protein).pandas()
        return view

    def dihedrals(self):
        """
        .dihedrals() method
        """
        parse = self.from_lib.dihedrals()
        self._repr_residue(parse)

        view = PDBData(self.protein).pandas()
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

    def __str__(self) -> str:
        chains = list(self.protein[self.pdb].keys())
        propmt = [f"<Structure {self.pdb}: ",
            f"Chains={chains} ",
            f"Residues={self.from_lib.residues_total}",
            ">"                        
        ]
        return "".join(propmt)

    def __repr__(self) -> str:
        return self.__str__()


class PDBresidue(PDBObject):
    """
    PDBresidue class
    """

    def __init__(self, *args,**kwargs) -> None:
        self.id = kwargs.get('id',None)
        self.resname = kwargs.get('resname',None)
        self.parent = kwargs.get('parent',None)
        self.level = "R"

    def set_phi(self):
        ...

    def get_phi(self):
        ...

    def set_psi(self):
        ...

    def get_psi(self):
        ...

    def __str__(self) -> str:
        return f"<Residue {self.resname} id: {self.id}>"

    def __repr__(self) -> str:
        return f"{self.resname}"
