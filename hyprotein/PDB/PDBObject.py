from hyprotein.libs import pdblib

class PDBobject:
    def __init__(self,pdb) -> None:
        self.pdb = pdb
        self.id = None
        if self.level == "Protein":
            pdblib.setup(self.pdb,self.pdb_dir,self.lib)
        self.lib = pdblib.lib
            
    def get_lib(self):
        return pdblib.get(self.pdb)