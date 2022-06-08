from hyprotein.PDB.PDBObject import PDBObject
from hyprotein.PDB.PDBStructure import Structure
from hyprotein.MD.MD import MD

class Protein(MD,PDBObject):
    def __new__(cls,id=None,**kwargs):
        pdbs = kwargs.get('pdb')
        kwargs.pop('pdb')
        if pdbs:
            dir = kwargs.get('dir')
            lib,version = kwargs.get('lib'), kwargs.get('version')
            proteins = dict()
            for id in pdbs:
                instance = super(Protein, cls).__new__(cls)
                instance.__init__(id=id,**kwargs)
                proteins.update({
                    id: instance
                })
            return proteins
        else:
            return super(Protein,cls).__new__(cls)

    level = 'P'
    def __init__(self,id=None,**kwargs) -> None:
        self.parent = None
        self.id = id
        self.dir = kwargs['dir']
        PDBObject.__init__(self,**kwargs)
        self.structure = Structure(id,**kwargs)

    def __repr__(self) -> str:
        return f"<hyProtein {self.id}>"
