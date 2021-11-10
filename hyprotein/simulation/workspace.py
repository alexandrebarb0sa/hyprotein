import os
import shutil
import json
from types import SimpleNamespace

def workspace(simulation,reset=False):
    """
    Create a current workspace for the running simulations. The default workspace tree is:

    :param folder: Workspace tree directory

    :type: dict
    """

    simulation = json.loads(json.dumps(simulation), object_hook=lambda item: SimpleNamespace(**item))
    
    if reset:
        try:
            shutil.rmtree(simulation.experiments.path)
        except FileNotFoundError as err:
            print('>>> HYPROTEIN warnings:\nStart a new simulation workspace.')
        exit()

    __mkdirs(simulation.proteins.path,mode=0o777,permission=True)
    __mkdirs(simulation.MD.path,mode=0o777,permission=True)
    __mkdirs(simulation.experiments.analysis.path,mode=0o777,permission=True)
    __mkdirs(simulation.experiments.outputs.path,mode=0o777,permission=True)

def __mkdirs(path,mode,permission):
    if permission:
        old_mask=os.umask(000)
        os.makedirs(path,mode=mode,exist_ok=True)
        os.umask(old_mask)
    else:
        os.makedirs(path,exist_ok=True)
