class PDBlib:
    def __init__(self) -> None:
        self._PDBLIBS = {}
    def register(self,lib,source):
        self._PDBLIBS[lib] = source

    def get(self,params):
        lib = params.get('lib')
        PDBLIB = self._PDBLIBS.get(lib)
        if not PDBLIB:
            raise ValueError(f"'{lib}' is not supported.")
        self.lib = PDBLIB(**params)
        return self.lib