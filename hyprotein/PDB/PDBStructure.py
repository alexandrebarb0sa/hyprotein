from hyprotein.PDB.PDBObject import PDBObject
from .PDBData import PDBData
from hyprotein import _utils

class Structure(PDBObject):
    """
    Structure class
    """
    level = "S"
    def __init__(self,id):
        # Keep this order
        PDBObject.__init__(self,id)

    @property
    def residues(self):
        try:
            if self.__protein:
                return PDBData(self.__protein).pandas()
        except AttributeError:
            protein = self.__repr__(self.lib.protein)
            self.__protein = protein
            return PDBData(self.__protein).pandas()

    def dihedrals(self):
        """
        .dihedrals() method
        """
        protein = self.lib.dihedrals()
        protein = self.__repr__(protein)
        view = PDBData(protein).pandas()
        return view

    def set_angle(self, chain, res_id, angle_key, value):
        self.lib.set_angle(chain, res_id, angle_key, value)
        prompt = [f"<hyProtein:",
                  f"{self.id.upper()}",
                  f"Chain: {chain}",
                  f"Residue: {res_id}",
                  f"{angle_key}={value}>"
                  ]
        return ' '.join(prompt)

    def get_angle(self, chain, res_id, angle_key):
        return self.lib.get_angle(chain,res_id,angle_key)

    def __str__(self) -> str:
        chains = list(self.lib.protein[self.id].keys())
        propmt = [f"<Structure {self.id}: ",
            f"Chains={chains} ",
            f"Residues={self.lib.residues_total}",
            ">"                        
        ]
        return "".join(propmt)

    def __repr__(self,protein=None) -> str:
        if protein:
            id = self.id
            chains = protein[id].keys()
            for c in chains:
                for r in protein[id][c]:
                    protein[id][c][r]['res'] = PDBresidue(
                        pdb=self.id,
                        lib = self.lib,
                        id=r,
                        resname=protein[id][c][r]['res'],
                        parent=c
                    )
            return protein
        else:
            return self.__str__()

class PDBresidue:
    """
    PDBresidue class
    """
    level = "R"
    def __init__(self,pdb,lib, *args,**kwargs) -> None:
        self.lib = lib
        self.pdb = pdb
        self.id = kwargs.get('id',None)
        self.resname = kwargs.get('resname',None)
        self.parent = kwargs.get('parent',None)

    def set_angle(self,angle_key,value):
        self.lib.set_angle(self.parent,self.id,angle_key,value)

    def get_angle(self,angle_key):
        return self.lib.get_angle(self.parent,self.id,angle_key)

    def __repr__(self) -> str:
        return f"<Residue {self.resname} id: {self.id}>"

    def __str__(self) -> str:
        return f"<{self.resname}>"
