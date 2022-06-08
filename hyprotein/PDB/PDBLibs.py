class PDBlibs:
    def __init__(self) -> None:
        self.libs_set = dict()

    def register(self,lib,source):
        if lib not in self.libs_set.keys():
            self.libs_set.update({lib:source})

    def get(self,id=None,**kwargs):
        lib = kwargs.get('lib')['name']
        lib = self.libs_set[lib]
        if lib is None:
            raise ValueError(f"'{lib}' is not defined.")
        if id is not None:
            return lib(id,**kwargs)
        else:
            return lib(**kwargs)

    def set_lib(self,lib,libtype):
        self.libs_set[libtype] = lib