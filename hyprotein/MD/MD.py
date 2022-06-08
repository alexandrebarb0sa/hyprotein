from hyprotein.PDB.PDBObject import PDBObject

class MD(PDBObject):
    def get_energy(self,energy,group,mdp):
        self.mdp(**mdp)
        return self.md.get_energy(energy,group)

    def get_gyrate(self,group,mdp):
        self.mdp(**mdp)
        return self.md.get_gyrate(group)

    def mdp(self,*args,**kwargs):
        kwargs.update({
            'pdb':{
                'dir':self.dir
            }
        })
        PDBObject.__init__(self,**kwargs)
