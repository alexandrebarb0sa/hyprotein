import hyprotein as hyp

# hyp.simulation.setup('experiment1.yaml')

experiment="experiment1"
pdbs = ['1fsd', '1le0', '1vii']
properties = ['POT', 'RG']

PDB=dict(
    pdb=pdbs,
    dir="./simulation/pdbs",
    lib = dict(
        name='biopython',
        version=None
    )
)

MD=dict(
    dir="./simulation/mdp",
    mdp="energy_min.mdp",
    lib=dict(
        name='gromacs',
        version='2021',
        dir='/home/hyprotein/gmx-2021'
    ),
    analysis=dict(
        dir=f"./simulation/{experiment}/analysis"
    ),
    outputs=dict(
        dir=f"./simulation/{experiment}/outputs"
    ),
    opt = dict(
        force_field='amber99sb-ildn',
        water='none'
    ),
    mmpbsa = dict(
        mdp="mmpbsa.mdp",
        lib=dict(
            name='gromacs',
            version='4.6.7',
            dir='/home/hyprotein/gmx-4.6.7'
        ),
    )
)

protein = hyp.Protein(**PDB)
r = protein['1le0'].structure.get_residues()

for pdb in pdbs:
    edr = protein[pdb].get_energy(energy=['Potential'],group=['Protein'],mdp=MD)
    rg = protein[pdb].get_gyrate(group='C-alpha',mdp=MD)
    sol = protein[pdb].get_energy(energy=['SOL'],group=['Protein'],mdp=MD)
    print(pdb,edr,rg,sol)

