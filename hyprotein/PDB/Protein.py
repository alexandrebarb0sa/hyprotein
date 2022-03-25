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
        pdb (list): list of the PDB files names
        lib (str): lib used to handle PDB files, e.g: biopython, gromacs, etc
    """
    def __new__(cls, pdb:list = None,pdb_dir:str = None, pdb_lib:str = None):
        if pdb is None:
            prompt = "Protein class needs three parameters to initialize:"
            _utils.warning(prompt)
        proteins = dict()
        for p in pdb:
            instance = super(Protein, cls).__new__(cls)
            instance.__init__(p,pdb_dir,pdb_lib)
            proteins.update({
                p: instance
            })
        return proteins

    def __init__(self, pdb:str,pdb_dir:str,pdb_lib:str):
        lib.init(pdb, pdb_dir, pdb_lib)
        self.id = id = pdb
        self.parent = None
        PDBObject.__init__(self)
        self.structure = Structure(id)
  
    def __repr__(self) -> str:
        return f"<hyProtein {self.id}>"
