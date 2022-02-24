from hyprotein.libs import pdblib

class PDBObject:
    def __init__(self,pdb) -> None:
        self.pdb = pdb
        self.id = None
        if self.level == "Protein":
            pdblib.setup(self.pdb,self.pdb_dir,self.lib)
            self.lib = pdblib.libname
        else:
            self.from_lib = pdblib.get(self.pdb)