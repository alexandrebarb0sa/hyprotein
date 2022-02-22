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
        self.__lib = self.get_lib()

    @property
    def protein(self):
        try:
            if self.__protein:
                ...
        except AttributeError:
            parse = self.__lib.protein
            self._repr_residue(parse)
        return self.__protein

    def _repr_residue(self,parse):
        protein = parse
        pdb = self.pdb
        chains = protein[self.pdb].keys()
        for c in chains:
            for res_id in protein[pdb][c]:
                protein[pdb][c][res_id]['RESIDUE'] = PDBresidues(
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
        parse = self.__lib.dihedrals()
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


class PDBresidues:
    """
    PDBresidues class
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
        return f"{self.resname}"

    def __repr__(self) -> str:
        return f"<Residue {self.resname} id: {self.id}>"
