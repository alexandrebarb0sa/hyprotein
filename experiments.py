import hyprotein as hyp

hyp.simulation.setup('experiment1.yaml')

p = hyp.Protein(
    PDB = dict(
        pdb=['1vii', '1fsd', '1le0'],
        dir='./simulation/pdbs',
        lib=['biopython']
    )
)

s = p['1le0'].structure
res = s.residues.loc['1le0','A',1]['res']
print(res.phi_psi())

