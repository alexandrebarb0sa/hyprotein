from hyprotein.protein.IPDBstructure import IPDBstructure

class PDBstructure(IPDBstructure):
    def __init__(self,name,PDBlib):
        self.__PDBlib = PDBlib
        self.name = name
    def show(self):
        return 

    def dihedrals(self):
        return self.__PDBlib.dihedrals()


class PDBresidues:
    def __init__(self) -> None:
        ...

    