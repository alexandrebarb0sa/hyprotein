from hyprotein.libs import lib

class PDBObject:
    def __init__(self,**kwargs) -> None:
        self.pdb = lib.get(self.id,'PDB',**kwargs)

    def get_level(self):
        return self.level

    def get_id(self):
        """Return the id."""
        return self.id
        
    def get_parent(self):
        """Return the parent Entity object."""
        return self.parent



