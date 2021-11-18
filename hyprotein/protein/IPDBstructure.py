import abc

class IPDBstructure(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'show') and 
                callable(subclass.show) and 
                hasattr(subclass, 'dihedrals') and 
                callable(subclass.dihedrals))

    @abc.abstractmethod
    def show(self):
        """Show residues"""
        raise NotImplementedError

    @abc.abstractmethod
    def dihedrals(self):
        """List protein's dihedral angles"""
        raise NotImplementedError        