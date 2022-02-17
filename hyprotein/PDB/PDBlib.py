from hyprotein.libs.interface import Interface

class PDBlib:
    def __init__(self) -> None:
        self._PDBLIBS = {}
        self._ARGS = {}
        self.lib = None

    def setup(self,pdb,pdb_dir,lib):
        self.lib = lib
        self._ARGS[pdb] = dict(zip(Interface.ARGS,[pdb,pdb_dir]))

    def register(self,lib,source):
        self._PDBLIBS[lib] = source

    def get(self,pdb):
        PDBLIB = self._PDBLIBS.get(self.lib)
        if not PDBLIB:
            raise ValueError(f"'{self.lib}' is not supported.")
        return PDBLIB(**self._ARGS[pdb])
