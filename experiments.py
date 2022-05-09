import hyprotein as hyp

hyp.simulation.setup('experiment1.yaml')


p = hyp.Protein(
    PDB = dict(
        pdb=['1vii', '1fsd', '1le0'],
        dir='./simulation/pdbs',
        lib=['biopython']
    ),
    MD = dict(
        simulation='experiment1',
        dir='./simulation/mdp',
        lib=[{'gromacs':'4.6.7'}],
        property=['POT','RG'],
        analysis=dict(
            dir='./simulation/experiment1/analysis'
        ),
        outputs=dict(
            dir='./simulation/experiment1/outputs'
        )
    )
)

s = p['1le0'].structure.get_property(['POT','RG'],mdp=None)
# p['1le0'].structure.property['POT']

