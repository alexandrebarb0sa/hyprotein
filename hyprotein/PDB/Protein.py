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
        lib (str): lib used to handle PDB files, e.g: biopythom, gromacsaa, etc
    """
    level = "Protein"
    def __new__(cls, pdb:list = None,pdb_dir:str = None, lib:str = None):
        if pdb is None:
            prompt = "Protein class needs three parameters to initialize:"
            _utils.warning(prompt)
        proteins = dict()
        for p in pdb:
            instance = super(Protein, cls).__new__(cls)
            instance.__init__(p,pdb_dir,lib)
            proteins.update({
                p: instance
            })
        return proteins

    def __init__(self, pdb:list,pdb_dir:str,lib:str) -> None:
        self.pdb = pdb
        self.pdb_dir = _utils.os.path.abspath(pdb_dir)
        self.lib = lib

        PDBObject.__init__(self,pdb)

        self.structure = Structure(pdb)
    
    def __repr__(self) -> str:
        return f"<hyProtein {self.pdb} id={self.id}>"
