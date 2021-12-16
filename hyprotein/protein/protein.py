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

    def __init__(self,protein:str,path,lib,pdb_format='pdb'):
        """
        Parameters
        ---
        protein:   str
            Protein protein
        """
        self.name:str = protein
        self.path = path
        self.pdb_format = pdb_format 
        self.lib = lib
        PDB.parser(protein,path,pdb_format,lib)
        self.structure = PDBstructure(PDB.get(protein))

