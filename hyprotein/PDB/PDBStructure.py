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

    @property
    def residues(self):
        try:
            if self.__protein:
                return PDBData(self.__protein).pandas()
        except AttributeError:
            protein = self.from_lib.protein
            pdb = self.pdb
            chains = protein[self.pdb].keys()
            for c in chains:
                for res_id in protein[pdb][c]:
                    protein[pdb][c][res_id]['res'] = PDBresidue(
                        pdb=self.pdb,
                        lib = self.from_lib,
                        id=res_id,
                        resname=protein[pdb][c][res_id]['res'],
                        parent=c
                    )
            self.__protein = protein
            # print(self.__protein)
            return PDBData(self.__protein).pandas()

    def dihedrals(self):
        """
        .dihedrals() method
        """
        protein = self.from_lib.dihedrals()
        view = PDBData(protein).pandas()
        return view

    def set_angle(self, chain, res_id, angle_key, value):
        self.from_lib.set_angle(chain, res_id, angle_key, value)
        prompt = [f"<hyProtein:",
                  f"{self.pdb.upper()}",
                  f"Chain: {chain}",
                  f"Residue: {res_id}",
                  f"{angle_key}={value}>"
                  ]
        return ' '.join(prompt)

    def get_angle(self, chain, res_id, angle_key):
        return self.from_lib.get_angle(chain,res_id,angle_key)

    def __str__(self) -> str:
        chains = list(self.from_lib.protein[self.pdb].keys())
        propmt = [f"<Structure {self.pdb}: ",
            f"Chains={chains} ",
            f"Residues={self.from_lib.residues_total}",
            ">"                        
        ]
        return "".join(propmt)

    def __repr__(self) -> str:
        return self.__str__()


class PDBresidue:
    """
    PDBresidue class
    """
    level = "R"
    def __init__(self,pdb,lib, *args,**kwargs) -> None:
        self.from_lib = lib
        self.pdb = pdb
        self.id = kwargs.get('id',None)
        self.resname = kwargs.get('resname',None)
        self.parent = kwargs.get('parent',None)

    def set_angle(self,angle_key,value):
        self.from_lib.set_angle(self.parent,self.id,angle_key,value)

    def get_angle(self,angle_key):
        return self.from_lib.get_angle(self.parent,self.id,angle_key)

    def __repr__(self) -> str:
        return f"<Residue {self.resname} id: {self.id}>"

    def __str__(self) -> str:
        return f"<{self.resname}>"
