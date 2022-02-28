import abc

class Interface(metaclass=abc.ABCMeta):
    
    # Defaul args that interface libs had to have
    ARGS = {
        'pdb':None,
        'pdb_dir':None
    }

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'dihedrals') and
                callable(subclass.dihedrals))

    @abc.abstractmethod
    def dihedrals(self):
        """List protein's dihedral angles"""
        raise NotImplementedError

    @abc.abstractmethod
    def set_angle(self, chain, res_id, angle_key, value):
        """Sets a new angle value for a specified residue from an indicated chain"""
        raise NotImplementedError
