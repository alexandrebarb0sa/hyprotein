import os
import inspect
import shutil
import yaml
import json
from types import SimpleNamespace
from rich.console import Console
from collections import namedtuple

console = Console()

def warning(prompt=""):
    origin = os.path.basename(inspect.stack()[1].filename)
    console.print(
        f"[reverse red]<[bold]hyProtein WARNING[/bold]:{origin}>[/]")
    print(f"{prompt}")

def info(prompt=""):
    origin = os.path.basename(inspect.stack()[1].filename)
    console.print(
        f"[reverse yellow]<[bold]hyProtein INFO[/bold]:{origin}>[/]")
    print(f"{prompt}")
