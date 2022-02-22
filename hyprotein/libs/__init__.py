from hyprotein.PDB.PDBLib import PDBlib
from .biopython import Biopython

pdblib = PDBlib()
pdblib.register("biopython", Biopython)