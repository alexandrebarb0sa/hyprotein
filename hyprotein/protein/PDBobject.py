from hyprotein.libs import pdblib

class PDBobject:
    """
    PDBobject class

    :param name: protein's name
    :type name: str
    :param path: protein pdb directory path
    :type path: str
    :param pdb_format: pdb format (.pdb, .ent)
    :type pdb_format: str
    :param lib: library packge to handle protein's file
    :type lib: str
    """
    def __init__(self,name,path,pdb_format,lib) -> None:
        self.name = name
        self.path = path
        self.pdb_format = pdb_format
        self.lib = lib

class PDBparser:
    """
    PDBparser class
    """
    def __init__(self) -> None:
        self.__protein = {}

    def parser(self,name,path,pdb_format,lib):
        params = {
            'name':name,
            'path':path,
            'pdb_format':pdb_format,
            'lib':lib
        }
        self.name = name
        lib = pdblib.get(params)
        self.__protein[name] = PDBobject(name,path,pdb_format,lib)

    def get(self,name=None):
        if not name:
            name = self.name
        try:
            return self.__protein[name]
        except KeyError as err:
            prompt = f'hyProtein Error: protein {err} not found'
            print(prompt)        
    
PDB = PDBparser()