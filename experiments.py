import hyprotein as hyp

hyp.simulation.create('experiment1.yaml')

p = hyp.Protein(
    pdb=['1vii','1fsd','1le0'],
    pdb_dir='./pdbs',
    lib='biopython'
)

r = p['1le0'].structure.dihedrals()
