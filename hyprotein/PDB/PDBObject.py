from hyprotein.libs import lib

class PDBObject:
    def __init__(self,**kwargs) -> None:
        if kwargs.get('mdp',None):
            self.md = lib.get(self.id,**kwargs)
        else:
            self.lib = lib.get(self.id,**kwargs)

    def get_level(self):
        return self.level

    def get_id(self):
        """Return the id."""
        return self.id
        
    def get_parent(self):
        """Return the parent Entity object."""
        return self.parent

