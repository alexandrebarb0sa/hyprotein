from . import _utils

simulation = dict()

# Private method
def _setup(config):
    global simulation
    if '.yaml' not in config:
        config = f"{config}.yaml"
    with open(config) as stream:
        simulation.update({
            'config': _utils.yaml.safe_load(stream)
        })
    simulation = _utils.json.loads(_utils.json.dumps(simulation['config']),
                            object_hook=lambda item: _utils.SimpleNamespace(**item))

def create(config, mode=0o700, permission=True, silent=True):
    """
    Create a current workspace for running simulations. The default workspace tree is:

    [Simulation's tree structure]

    ├── simulation
    │   ├── pdbs
    │   ├── mdp
    │   └── experiments
    │       ├── experiment 1
    │       │   ├── analysis
    │       │   └── outputs
    │       └── experiment 2 (etc.)
    │           ├── analysis
    │           └── outputs    

    :param config: Workspace tree directory
    :type config: YAML configuration file, with or without extension declared.
    :type config: str
    :param mode: File octal mode, like chmod options for read, write and execute
    :type mode: octal permission, default: 0o700 (file owner has perssion to read, write and execute)
    :param permission: boolean value to allow weather or not it has permisison to change file's mode of read, write and execute
    :type permission: bool (True or False)
    """

    global simulation
    if not simulation:
        _setup(config)

    path = {
        'proteins': simulation.proteins.dir,
        'MD': simulation.MD.dir,
        'experiment': {
            'dir': simulation.experiment.name,
            'analysis': _utils.os.path.join(simulation.experiment.name,simulation.experiment.analysis.dir),
            'outputs': _utils.os.path.join(simulation.experiment.name,simulation.experiment.outputs.dir)
        }
    }

    local = _utils.os.getcwd()
    user_mode = _utils.os.umask(000)
    if permission:
        _utils.os.makedirs(simulation.root, mode, exist_ok=True)
        _utils.os.chdir(simulation.root)
        _utils.os.makedirs(path['proteins'], mode, exist_ok=True)
        _utils.os.makedirs(path['MD'], mode, exist_ok=True)
        try:
            _utils.os.makedirs(path['experiment']['dir'], mode, exist_ok=False)
            _utils.os.makedirs(path['experiment']['analysis'], mode, exist_ok=True)
            _utils.os.makedirs(path['experiment']['outputs'], mode, exist_ok=True)
        except FileExistsError as err:
            if not silent:
                prompt = "Simulation directory already exists! Skipping..."
                _utils.info(prompt)

        _utils.os.umask(user_mode)
        _utils.os.chdir(local)

def clear(config=None):
    """
    Clean up the folder of the current experiment.
    :type config: YAML configuration file, with or without extension declared.
    :type config: str
    """
    global simulation
    if simulation:
        try:
            path = _utils.os.path.join(simulation.root,simulation.experiment.name)
            prompt = "Confirm to clean up the experiment folder [y/n]: "
            _utils.info()
            opt = input(prompt)
            if opt in ['y','Y']:
                _utils.shutil.rmtree(path)
                _utils.warning("Experimento directory removed!")
            elif opt in ['n','N']:
                pass
            else:
                print('Option not valid, try again...')
                clear()
        except FileNotFoundError as err:
            prompt = 'Simulation directory not found!\n'
            _utils.warning(prompt)
    else:
        if config:
            _setup(config)
            clear(config)
        else:
            config = input('YAML configuration file: ')
            clear(config)

def run():
    return 'run'
