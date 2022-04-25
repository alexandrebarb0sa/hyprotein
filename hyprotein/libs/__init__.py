from hyprotein.PDB.PDBLib import PDBlib
from .biopython import Biopython

lib = PDBlib()
lib.register("biopython",libtype='PDB',source=Biopython)