from hyprotein.PDB.PDBLibs import PDBlibs
from .biopython import Biopython
from .gromacs import Gromacs

lib = PDBlibs()
lib.register("biopython",source=Biopython)
lib.register("gromacs",source=Gromacs)