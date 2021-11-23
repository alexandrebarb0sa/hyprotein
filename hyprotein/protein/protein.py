from .PDBobject import PDB
from .PDBstructure import PDBstructure

class Protein:
    """
    Protein class

    :param name: protein's name
    :type name: str
    :param path: protein's directory path
    :type path: str
    :param lib: library used to get protein structure access
    :type lib: str
    :param pdb_format: pdb format, like .pdb, .ent
    :type pdb_format: str
    """

    def __init__(self,name:str,path,lib,pdb_format='pdb'):
        """
        Parameters
        ---
        name:   str
            Protein name
        """
        self.name : str = name
        self.path = path
        self.pdb_format = pdb_format 
        self.lib = lib
        PDB.parser(self,name,path,pdb_format,lib)
        self.structure = PDBstructure()

