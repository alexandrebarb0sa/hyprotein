from hyprotein.libs import lib

class PDBObject:
    def __init__(self,id=None) -> None:
        if id:
            self.id = id
        self.lib = lib.get(self.id)

    def get_level(self):
        return self.level

    def get_id(self):
        """Return the id."""
        return self.id
        
    def get_parent(self):
        """Return the parent Entity object."""
        return self.parent