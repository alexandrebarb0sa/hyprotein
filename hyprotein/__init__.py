from rich.console import Console
from . import simulation

__version__ = "2.0.0"

console = Console()

class hyWarnings:
    """
    hyWarnings class handles with terminal warnings info.
    """
    def __init__(self,origin) -> None:
        self.origin = origin
    def warning(self,prompt):
        console.print(
            f"[reverse red]<[bold]hyProtein WARNING[/bold]:{self.origin}>[/]")
        print(f"{prompt}")
    def info(self,prompt):
        console.print(
            f"[reverse yellow]<[bold]hyProtein INFO[/bold]:{self.origin}>[/]")
        print(f"{prompt}")

simulation._warnings = hyWarnings('simulation')