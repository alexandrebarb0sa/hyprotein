from .Protein import PDBObject

class Protein(PDBObject):
    """ 
    Protein class
    =============
    
    Protein class to handle PDB objects.
    
    Arguments
        PDB (dict): ...
        MD (dic): ...
    """

    def __init__(self,**kwargs):
        self.parent = None
        self.id = kwargs.get('id')
        if self.id:
            PDBObject.__init__(self,**kwargs)

        # self.structure = Structure(id,**kwargs)

    @classmethod
    def init(cls,**kwargs):
        print('oi')
        id = kwargs.get('id')
        dir = kwargs.get('dir')
        return cls(id=id,dir=dir)
  
    def __repr__(self) -> str:
        return f"<hyProtein {self.id}>"
