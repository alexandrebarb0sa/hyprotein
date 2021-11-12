class PDBstructure:
    def __init__(self,PDBlib):
        self.__PDBlib = PDBlib
        self.__PDBlib.get_structure()
        self.name = self.__PDBlib.name.upper()


class PDBresidues:
    def __init__(self) -> None:
        ...

    