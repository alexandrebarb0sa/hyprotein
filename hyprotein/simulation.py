import os
import shutil
import yaml
import json
from types import SimpleNamespace

simulation = dict()
_warnings = None

# Private method
def _setup(config):
    global simulation
    if '.yaml' not in config:
        config = f"{config}.yaml"
    with open(config) as stream:
        simulation.update({
            'config': yaml.safe_load(stream)
        })
    simulation = json.loads(json.dumps(simulation['config']),
                            object_hook=lambda item: SimpleNamespace(**item))

def create(config, mode=0o700, permission=True):
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
            'analysis': os.path.join(simulation.experiment.name,simulation.experiment.analysis.dir),
            'outputs': os.path.join(simulation.experiment.name,simulation.experiment.outputs.dir)
        }
    }

    local = os.getcwd()
    if permission:
        user_mode = os.umask(000)
        os.makedirs(simulation.root, mode, exist_ok=True)
        os.chdir(simulation.root)
        os.makedirs(path['proteins'], mode, exist_ok=True)
        os.makedirs(path['MD'], mode, exist_ok=True)
        try:
            os.makedirs(path['experiment']['dir'], mode, exist_ok=False)
            os.makedirs(path['experiment']['analysis'], mode, exist_ok=True)
            os.makedirs(path['experiment']['outputs'], mode, exist_ok=True)
        except FileExistsError as err:
            prompt = "Simulation directory already exists! Skipping..."
            _warnings.info(prompt)

    os.umask(user_mode)
    os.chdir(local)

def clear(config):
    """
    Clean up the folder of the current experiment.
    :type config: YAML configuration file, with or without extension declared.
    :type config: str
    """
    global simulation
    if simulation:
        try:
            path = os.path.join(simulation.root,simulation.experiment.name)
            shutil.rmtree(path)
            prompt = "Experiment folder cleaned!"
            _warnings.warning(prompt)
        except FileNotFoundError as err:
            prompt = 'Start a new simulation'
    else:
        if config:
            _setup(config)
            clear(config)
        else:
            exit()

def run():
    return 'run'
