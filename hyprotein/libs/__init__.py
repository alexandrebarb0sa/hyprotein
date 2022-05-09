from hyprotein.PDB.PDBLib import PDBlib
from .biopython import Biopython
from .gromacs import Gromacs

lib = PDBlib()
lib.register("biopython",libtype='PDB',source=Biopython)
lib.register("gromacs",libtype='MD',source=Gromacs)