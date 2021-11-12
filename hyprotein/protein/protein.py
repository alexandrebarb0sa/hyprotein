from .PDBObject import PDBobject

class Protein(PDBobject):
    '''
    Protein class

    :param name: protein's name
    :type: str()
    :param path: protein's directory path
    :type: str()
    :param lib: library used to get protein structure access
    :type: str()
    :param pdb_format: pdb format, like .pdb, .ent
    '''

    def __init__(self,name,path,lib,pdb_format='pdb'):
        super().__init__(name,path,lib,pdb_format)        
        self.structure = self.get_structure()
