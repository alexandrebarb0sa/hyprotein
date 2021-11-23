from hyprotein.protein.PDBlib import PDBlib
from .biopython import Biopython

pdblib = PDBlib()
pdblib.register("biopython", Biopython)