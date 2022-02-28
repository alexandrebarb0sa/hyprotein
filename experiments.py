import hyprotein as hyp

hyp.simulation.create('experiment1.yaml')

p = hyp.Protein(
    pdb=['1vii','1fsd','1le0'],
    pdb_dir='./pdbs',
    lib='biopython'
)

s = p['1vii'].structure
res = s.residues.loc['1vii']

print(s.set_angle('A',41,'psi',0))
print(s.get_angle('A',41,'psi'))