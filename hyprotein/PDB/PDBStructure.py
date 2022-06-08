from hyprotein.PDB.PDBObject import PDBObject
from .PDBView import PDBView

class Structure(PDBObject):
    """
    Structure class
    """
    level = "S"
    def __init__(self,id,**kwargs):
        self.id = id
        PDBObject.__init__(self,**kwargs)
        self.__lib = self.lib
        del(self.lib)

    def get_residues(self):
        try:
            if self.__protein:
                return PDBView(self.__protein).pandas()
        except AttributeError:
            protein = self.__repr__(self.__lib.protein2dict)
            self.__protein = protein
            return PDBView(self.__protein).pandas()

    def get_dihedrals(self):
        """
        .get_dihedrals() method
        """
        protein = self.__lib.dihedrals()
        protein = self.__repr__(protein)
        view = PDBView(protein).pandas()
        return view

    def set_angle(self, chain, res_id, angle_key, value):
        self.__lib.set_angle(chain, res_id, angle_key, value)
        prompt = [f"<hyProtein:",
                  f"{self.id.upper()}",
                  f"Chain: {chain}",
                  f"Residue: {res_id}",
                  f"{angle_key}={value}>"
                  ]
        return ' '.join(prompt)

    def get_angle(self, chain, res_id, angle_key):
        return self.__lib.get_angle(chain,res_id,angle_key)

    def get_property(self,propery=None,mdp=None):
        ...

    def __str__(self) -> str:
        chains = list(self.__lib.protein2dict[self.id].keys())
        propmt = [f"<Structure {self.id}: ",
            f"Chains={chains} ",
            f"Residues={self.__lib.residues_total}",
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
                        id = r,
                        resname=protein[id][c][r]['res'],
                        parent = c,
                        pdb=self.__lib                                                                       
                    )
            return protein
        else:
            return self.__str__()

class PDBresidue:
    """
    PDBresidue class
    """
    level = "R"
    def __init__(self,id,resname,parent,pdb) -> None:
        self.id = id
        self.__lib = pdb
        self.resname = resname
        self.parent = parent

    def set_angle(self,angle_key,value):
        self.__lib.set_angle(self.parent,self.id,angle_key,value)

    def get_angle(self,angle_key):
        return self.__lib.get_angle(self.parent,self.id,angle_key)

    def phi_psi(self):
        phi = self.__lib.get_angle(self.parent, self.id,'phi')
        psi = self.__lib.get_angle(self.parent, self.id, 'psi')
        return (phi,psi)

    def __repr__(self) -> str:
        return f"<Residue {self.resname} id: {self.id}>"

    def __str__(self) -> str:
        return f"<{self.resname}>"
