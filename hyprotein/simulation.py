from . import _utils

simulation = dict()

# Private method
def _config(cfg):
    global simulation
    if '.yaml' not in cfg:
        cfg = f"{cfg}.yaml"
    with open(cfg) as stream:
        simulation.update(_utils.yaml.safe_load(stream))
        simulation = _utils.json.loads(_utils.json.dumps(simulation),
                        object_hook=lambda item: _utils.SimpleNamespace(**item))

def setup(cfg, mode=0o700, permission=True, silent=True):
    """
    Setup the current workspace for running simulations. The default workspace tree is:

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

    :param cfg: Workspace tree directory
    :type cfg: YAML configuration file, with or without extension declared.
    :type cfg: str
    :param mode: File octal mode, like chmod options for read, write and execute
    :type mode: octal permission, default: 0o700 (file owner has perssion to read, write and execute)
    :param permission: boolean value to allow weather or not it has permisison to change file's mode of read, write and execute
    :type permission: bool (True or False)
    """

    global simulation
    if not simulation:
        _config(cfg)

    paths = {
        'proteins': _utils.os.path.normpath(_utils.os.path.join(*simulation.proteins.dir)),
        'MD': _utils.os.path.normpath(_utils.os.path.join(*simulation.MD.dir)),
        'experiment': {
            'dir': _utils.os.path.normpath(_utils.os.path.join(*simulation.experiment.dir)),
            'analysis': _utils.os.path.normpath(_utils.os.path.join(*simulation.MD.analysis.dir)),
            'outputs': _utils.os.path.normpath(_utils.os.path.join(*simulation.MD.outputs.dir)),
        }
    }

    local = _utils.os.getcwd()
    user_mode = _utils.os.umask(000)
    if permission:
        _utils.os.makedirs(simulation.path, mode, exist_ok=True)
        _utils.os.chdir(simulation.path)
        _utils.os.makedirs(paths['proteins'], mode, exist_ok=True)
        _utils.os.makedirs(paths['MD'], mode, exist_ok=True)
        try:
            _utils.os.makedirs(paths['experiment']['dir'], mode, exist_ok=False)
            _utils.os.makedirs(paths['experiment']['analysis'], mode, exist_ok=True)
            _utils.os.makedirs(paths['experiment']['outputs'], mode, exist_ok=True)
        except FileExistsError as err:
            if not silent:
                prompt = "Simulation directory already exists! Skipping..."
                _utils.info(prompt)

        _utils.os.umask(user_mode)
        _utils.os.chdir(local)

def clear(cfg=None):
    """
    Clean up the folder of the current experiment.
    :type cfg: YAML configuration file, with or without extension declared.
    :type cfg: str
    """
    global simulation
    if simulation:
        try:
            path = _utils.os.path.normpath(_utils.os.path.join(*simulation.experiment.dir))
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
        if cfg:
            _config(cfg)
            clear(cfg)
        else:
            cfg = input('YAML configuration file: ')
            clear(cfg)

def run():
    return 'run'
