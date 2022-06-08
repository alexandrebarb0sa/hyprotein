from hyprotein import _utils
import gmxapi as gmx

class Gromacs:
    __version__ = ['Gromacs', gmx.__version__]
    libname = "gromacs"

    def __init__(self, id, **kwargs) -> None:
        self.id = id
        pdb_format = kwargs.get('pdb_format', 'pdb')
        self.version = kwargs['lib']['version']
        self.path = dict(
            pdb=f"{kwargs['pdb']['dir']}/{id}.{pdb_format}",
            gromacs=f"{kwargs['lib']['dir']}",
            mdp=f"{kwargs['dir']}/{kwargs['mdp']}",
            outputs=f"{kwargs['outputs']['dir']}/{id}",
            analysis=f"{kwargs['analysis']['dir']}/{id}",
            mmpbsa=f"{kwargs['dir']}/{kwargs['mmpbsa']['mdp']}",
        )
        try:
            self.opt = kwargs['opt']
            self.opt['force_field'] = self.opt.get(
                'force_field', 'amber99sb-ildn')
            self.opt['water'] = self.opt.get('water', 'no')
        except:
            ...
        self.mmpbsa = kwargs['mmpbsa']

# PREPARING DATA STRUCTURE
# ---------------------------------------------
        self.gmx = {
            'pdb2gmx': None,
            'editconf': None,
            'grompp': None,
            'mdrun': None,
            'energy': None,
            'gyrate': None,
        }
        self.gmx = _utils.json.loads(_utils.json.dumps(
            self.gmx), object_hook=lambda item: _utils.SimpleNamespace(**item))

        for cmd in self.gmx.__dict__.keys():
            self.gmx.__dict__[cmd] = {
                'output': None,
            }
            self.gmx.__dict__[cmd] = _utils.json.loads(_utils.json.dumps(self.gmx.__dict__[cmd]),
            object_hook=lambda item: _utils.SimpleNamespace(**item))

        self.gmx.pdb2gmx.output = {
            'gro': f"{self.path['outputs']}.gro",
            'top': f"{self.path['outputs']}.top",
            'itp': f"{self.path['outputs']}.itp",
        }
        self.gmx.editconf.output = {
            'gro': f"{self.path['outputs']}.gro",
        }
        self.gmx.grompp.output = {
            'tpr': f"{self.path['outputs']}.tpr",
            'mdp': f"{self.path['outputs']}.mdp"
        }
        self.gmx.mdrun.output = {
            'gro': f"{self.path['outputs']}.gro",
            'edr': f"{self.path['outputs']}.edr",
            'log': f"{self.path['outputs']}.log",
            'trr': f"{self.path['outputs']}.trr",
            'xtc': f"{self.path['outputs']}.xtc",
        }

# RUNNING SIMULATION
# ---------------------------------------------
    def run(self,cmd=""):
        GMXRC = f". {self.path['gromacs']}/bin/GMXRC;"
        GMXLIB = f"export GMXLIB='{self.path['gromacs']}/share/gromacs/top';"
        if cmd:
            cmd = "".join(f" {k} {v}" for k, v in cmd.items())
            cmd = " ".join(cmd.split())
        cmd = ''.join([GMXRC,GMXLIB,cmd])
        cmd = _utils.subprocess.Popen(
            cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
        stderr = cmd.stderr.read().decode("ascii", "ignore")
        cmd.kill()
        return cmd,stderr

# Step #1: pdb2gmx
# ---------------------------------------------
    def pdb2gmx(self):
        self.run()
        cmd = gmx.commandline_operation(
            'gmx',
            arguments=[
                'pdb2gmx', '-ignh', '-ff', self.opt['force_field'],
                '-water', self.opt['water'], '-ter'
            ],
            input_files={'-f': self.path['pdb']},
            output_files={
                '-p': self.gmx.pdb2gmx.output['top'],
                '-o': self.gmx.pdb2gmx.output['gro'],
                '-i': self.gmx.pdb2gmx.output['itp']
            }
        )
        cmd.run()
        if cmd.output.erroroutput.result() != '':
            print(cmd.output.erroroutput.result())
        del(cmd)

# Step #2: editconf
# ---------------------------------------------
    def editconf(self):
        self.run()
        cmd = gmx.commandline_operation(
            'gmx',
            arguments=['editconf', '-c', '-d', '1', '-bt', 'cubic'],
            input_files={
                '-f': self.gmx.pdb2gmx.output['gro']
            },
            output_files={
                '-o': self.gmx.editconf.output['gro'],
            }
        )
        cmd.run()
        if cmd.output.erroroutput.result() != '':
            print(cmd.output.erroroutput.result())
        del(cmd)

# Step #3: grompp
# ---------------------------------------------
    def grompp(self):
        if _utils.version.parse(self.version) < _utils.version.parse('5.0.0'):
            cmd = {
                'grompp': '',
                '-maxwarn': '1',
                '-f': self.path['mdp'],
                '-c': self.gmx.editconf.output['gro'],
                '-p': self.gmx.pdb2gmx.output['top'],
                '-o': self.gmx.grompp.output['tpr'],
                '-po': self.gmx.grompp.output['mdp'],
            }
            cmd,stderr = self.run(cmd)
        else:
            self.run()
            cmd = gmx.commandline_operation(
                'gmx',
                arguments=['grompp', '-maxwarn', '1'],
                input_files={
                    '-f': self.path['mdp'],
                    '-c': self.gmx.editconf.output['gro'],
                    '-p': self.gmx.pdb2gmx.output['top'],
                },
                output_files={
                    '-o': self.gmx.grompp.output['tpr'],
                    '-po': self.gmx.grompp.output['mdp']
                }
            )
            cmd.run()
            if cmd.output.erroroutput.result() != '':
                print(cmd.output.erroroutput.result())
            del(cmd)

# Step #4: mdrun
# ---------------------------------------------
    def mdrun(self, rerun=False):
        self.pdb2gmx()
        self.editconf()
        self.grompp()

        if _utils.version.parse(self.version) < _utils.version.parse('5.0.0'):
            cmd = {
                'mdrun': "",
                '-s': self.gmx.grompp.output['tpr'],
                '-c': self.gmx.mdrun.output['gro'],
                '-e': self.gmx.mdrun.output['edr'],
                '-o': self.gmx.mdrun.output['trr'],
                '-x': self.gmx.mdrun.output['xtc'],
                '-g': self.gmx.mdrun.output['log'],
            }
            cmd,stderr = self.run(cmd)

            if rerun:
                cmd = {
                    'mdrun': '',
                    '-s': self.gmx.grompp.output['tpr'],
                    '-rerun': self.gmx.editconf.output['gro'],
                    '-e': self.gmx.mdrun.output['edr'],
                }
                cmd,stderr = self.run(cmd)

        else:
            self.grompp()
            cmd = gmx.commandline_operation(
                'gmx',
                arguments=['mdrun', '-v'],
                input_files={
                    '-s': self.gmx.grompp.output['tpr'],
                },
                output_files={
                    '-c': self.gmx.mdrun.output['gro'],
                    '-e': self.gmx.mdrun.output['edr'],
                    '-o': self.gmx.mdrun.output['trr'],
                    '-x': self.gmx.mdrun.output['xtc'],
                    '-g': self.gmx.mdrun.output['log'],
                }
            )
            cmd.run()
            if cmd.output.erroroutput.result() != '':
                print(cmd.output.erroroutput.result())

            if rerun:
                cmd = gmx.commandline_operation(
                    'gmx',
                    arguments=['mdrun', '-v'],
                    input_files={
                        '-s': self.gmx.grompp.output['tpr'],
                        '-rerun': self.gmx.editconf.output['gro'],
                    },
                    output_files={
                        '-e': self.gmx.mdrun.output['edr'],
                    }
                )
                cmd.run()
                if cmd.output.erroroutput.result() != '':
                    print(cmd.output.erroroutput.result())
        del(cmd)

# GROMACS PROPERTIES CALCULATION
# ---------------------------------------------
    def get_energy(self,energy,group):
# TODO - Implementar o rerun
# TODO - Remember to kill process

        if set(energy).issubset(['SOL','Sol','sol']):
            self.version = self.mmpbsa['lib']['version']
            self.path['gromacs'] = self.mmpbsa['lib']['dir']
            self.mdrun(rerun=False)
            return self.g_mmpbsa(*group)

        self.mdrun(rerun=False)

        if _utils.version.parse(self.version) <= _utils.version.parse('5.0.0'):
            # Total - Energy
            opt = {
                "Potential": "9",
            }
        else:
            opt = {
                "Potential": "11",
            }

        result = dict()
  
        for edr in energy:
            cmd = {
                'echo': f"{opt[edr]} |",
                'gmx': 'energy',
                '-f': self.gmx.mdrun.output['edr'],
                '-o': f"{self.path['analysis']}_{edr}.xvg"
            }
            cmd,stderr = self.run(cmd)

            cmd = {
                'tail': f"{self.path['analysis']}_{edr}.xvg",
                '-n': '1'
            }
            cmd, stderr = self.run(cmd)

            try:
                result.update({
                    edr: cmd.stdout.read().decode("ascii", "ignore").split()[-1]
                })
            except IndexError:
                print(stderr)
                
            cmd.kill()
            del(cmd)
        return result

    def g_mmpbsa(self, group):
        opt = {
            'System': '0',
            'Protein': '1',
            'C-alpha': '3',
        }

        cmd = {
            'gmx': "trjconv",
            '-f': self.gmx.mdrun.output['trr'],
            '-o': self.gmx.mdrun.output['xtc'],
        }
        cmd, stderr = self.run(cmd)

        cmd = {
            'echo ': f"{opt[group]} | ",
            'g_mmpbsa': '',
            '-f': self.gmx.mdrun.output['xtc'],
            '-s': self.gmx.grompp.output['tpr'],
            '-i': f"{self.path['mmpbsa']}",
            '-nomme': '',
            '-pbsa': '',
            '-nodiff': '',
            '-pol': f"{self.path['analysis']}_polar.xvg",
            '-apol': f"{self.path['analysis']}_apolar.xvg",
        }
        cmd, stderr = self.run(cmd)

        result = dict()

        cmd = {
            'tail': f"{self.path['analysis']}_polar.xvg",
            '-n': '1'
            }
        cmd, stderr = self.run(cmd)
        try:
            result['polar'] = cmd.stdout.read().decode("ascii", "ignore").split()[-1]
        except IndexError:
            print(stderr)

        cmd = {
            'tail': f"{self.path['analysis']}_apolar.xvg",
            '-n': '1'
        }
        cmd, stderr = self.run(cmd)
        try:
            result['apolar'] = cmd.stdout.read().decode("ascii", "ignore").split()[1]
        except IndexError:
            print(stderr)

        result = {
            'SOL': result['polar'] + result['apolar']
        }

        cmd.kill()
        del(cmd)
        return result

    def get_gyrate(self,group='C-alpha'):
        opt = {
            'System': '0',
            'Protein': '1',
            'C-alpha': '3',
        }

        cmd = {
            'echo': f"{opt[group]} |",
            'gmx': 'gyrate',
            '-f': self.gmx.mdrun.output['trr'],
            '-s': self.gmx.mdrun.output['gro'],
            '-o': f"{self.path['analysis']}_gyrate.xvg"
        }
        cmd,stderr = self.run(cmd)

        cmd = {
            'tail': f"{self.path['analysis']}_gyrate.xvg",
            '-n': '1'
        }
        cmd, stderr = self.run(cmd)

        result = dict(
            gyrate = cmd.stdout.read().decode("ascii", "ignore").split()[1]
        )
        return result
