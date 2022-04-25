
class PDBlib:
    def __init__(self) -> None:
        self.libset = dict(
            PDB=None,
            MD=None,
        )

    def register(self,libname,libtype,source):
        if self.libset[libtype] is None:
            self.libset[libtype] = source

    def get(self,id,libtype='PDB',**kwargs):
        lib = self.libset.get(libtype)
        if lib is None:
            raise ValueError(f"'{lib}' is not defined.")
        return lib(id,**kwargs)

    def set_lib(self,lib,libtype):
        self.libset[libtype] = lib