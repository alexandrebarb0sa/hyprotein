from hyprotein.libs.interface import Interface
from hyprotein import _utils

class PDBlib:
    def __init__(self) -> None:
        self._PDBLIBS = {}
        self._ARGS = {}
        self.lib = None

    def init(self,pdb,dir,lib):
        dir = _utils.os.path.abspath(dir)
        self.lib = lib
        self._ARGS[pdb] = dict(zip(Interface.ARGS,[pdb,dir]))

    def register(self,lib,source):
        self._PDBLIBS[lib] = source

    def get(self,pdb):
        PDBLIB = self._PDBLIBS.get(self.lib)
        if not PDBLIB:
            raise ValueError(f"'{self.lib}' is not supported.")
        return PDBLIB(**self._ARGS[pdb])
