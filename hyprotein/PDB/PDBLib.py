from hyprotein.libs.interface import Interface
from hyprotein import _utils

class PDBlib:git
    def __init__(self) -> None:
<<<<<<< Updated upstream
        self._PDBLIBS = {}
        self._ARGS = {}

    # def init(self,pdb,dir,lib):
    #     dir = _utils.os.path.abspath(dir)
    #     self.lib = lib
    #     self._ARGS[pdb] = dict(zip(Interface.ARGS,[pdb,dir]))
=======
        self._PDBLIBS = dict()
        self.lib = None

    def register(self,lib,lib_type,lib_source):
        if lib not in self._PDBLIBS:
            self._PDBLIBS.update({
                lib:dict(
                    type=lib_type,
                    source=lib_source
                )
            })
>>>>>>> Stashed changes


        if lib_type not in self._PDBLIBS:
            self._PDBLIBS.update({
                lib_type:dict()
            })
        self._PDBLIBS[lib_type].update({
            lib:lib_source
        })

    def get(self,id,lib_type):
        PDBLIB = self._PDBLIBS[lib_type].get()
        if not PDBLIB:
            raise ValueError(f"'{self.lib}' is not supported.")
        return PDBLIB(**self._ARGS[pdb])

