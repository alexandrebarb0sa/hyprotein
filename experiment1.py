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
            name=pdb,
            path=simulation['proteins']['path'],
            lib='biopython'
        )
    })    


print(p['1vii'].structure.show() )

# a = p['1vii'].structure.show()['1vii']['A'][0]
