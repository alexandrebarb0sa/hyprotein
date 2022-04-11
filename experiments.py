import hyprotein as hyp

hyp.simulation.setup('experiment1.yaml')

p = hyp.Protein(
    pdb=['1vii','1fsd','1le0'],
    pdb_dir='./simulation/pdbs',
    pdb_lib='biopython'
)

s = p['1le0'].structure
print(s)