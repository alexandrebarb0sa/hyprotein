import hyprotein as hyp

experiment = 'experiment1'

simulation = {
    'path':'./simulations/',
    'proteins':{
        'path':'./simulations/pdbs/',
        'pdbs':['1vii','1le0','1fsd'],
        'property':['POT','RG'],
    },
    'MD':{
        'path':'./simulations/mdp/',
        'temperature':309,
    },
    'experiments':{
        'path':f"./simulations/experiments/{experiment}",
        'analysis':{
            'path':f"./simulations/experiments/{experiment}/analysis/",
            'logs':{
                'file1.dat':{
                    'steps':100,
                    'columns':['POT','RG']
                }
            }
        },
        'outputs':{
            'path':f"./simulations/experiments/{experiment}/outputs/",
        },
    }
}

hyp.simulation.workspace(simulation)

p = dict()

for pdb in simulation['proteins']['pdbs']:
    p.update({
        pdb:hyp.Protein(
            protein=pdb,
            path=simulation['proteins']['path'],
            lib='biopython'
        )
    })    

residues = p['1vii'].structure
print(residues.set_angle('A',41,'phi',0))

print(residues.dihedrals())

# p['1vii'].structure.set_angle('A',41,'phi',value=0)