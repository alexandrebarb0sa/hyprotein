from hyprotein.libs import lib
from .PDBStructure import Structure
from .PDBObject import PDBObject
from hyprotein import _utils
from hyprotein.simulation import simulation

class Protein(PDBObject):
    """ 
    Protein class
    =============
    
    Protein class to handle PDB objects.
    
    Arguments
        PDB (dict): ...
        MD (dic): ...
    """
    def __new__(cls,PDB,**kwargs):
        proteins = dict()
        for p in PDB['pdb']:
            instance = super(Protein, cls).__new__(cls)
            instance.__init__(p,dir=PDB['dir'],lib=PDB['lib'])
            proteins.update({
                p:instance
            })
        return proteins

    def __init__(self,id,**kwargs):
        self.id = id
        self.parent = None
        PDBObject.__init__(self,**kwargs)
        self.structure = Structure(id,**kwargs)
  
    def __repr__(self) -> str:
        return f"<hyProtein {self.id}>"
