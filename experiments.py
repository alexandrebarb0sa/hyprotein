import hyprotein as hyp

hyp.simulation.create('experiment1.yaml')

p = hyp.Protein(
    pdb=['1vii','1fsd','1le0'],
    pdb_dir='./pdbs',
    lib='biopython'
)

r = p['1vii'].structure.show().loc['1vii','A',41].values
print(r)