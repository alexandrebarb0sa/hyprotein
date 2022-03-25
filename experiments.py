import hyprotein as hyp

hyp.simulation.create('experiment1.yaml')

p = hyp.Protein(
    pdb=['1vii','1fsd','1le0'],
    pdb_dir='./pdbs',
    pdb_lib='biopython'
)

s = p['1le0'].structure
res = s.residues.loc['1le0']
print(s)