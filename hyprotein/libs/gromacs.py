from hyprotein import _utils
import gmxapi as gmx

class Gromacs:
    # __version__ = ['Gromacs', gmx.__version__]
    libname = "gromacs"
    def __init__(self,id,**kwargs) -> None:
        self.id = id
        pdb_format = kwargs.get('pdb_format','pdb')
        dir = f"{kwargs.get('dir')}/{id}.{pdb_format}"
# ---------------------------------------------------------
# Preparing data structure
# ---------------------------------------------------------
        self.gromacs = {
            'version': None,            
            'gmx': {
                'pdb2gmx':None,
                'editconf':None,
                'grompp':None,
                'mdrun':None,
                'energy':None,
                'gyrate':None,
            },
            'pdb': None,
            'property': None,
            'analysis': None,
            'outputs': None,
            'mdp': None            
        }
        self.gromacs = _utils.json.loads(_utils.json.dumps(
            self.gromacs), object_hook=lambda item: _utils.SimpleNamespace(**item))
        # self.gromacs.gmx = _utils.json.loads(_utils.json.dumps(
            # self.gromacs.gmx), object_hook=lambda item: _utils.SimpleNamespace(**item))

        for cmd in self.gromacs.gmx.__dict__.keys():
            self.gromacs.gmx.__dict__[cmd] = {
                'opt':None,
                'output':None,
                'cli':None
            }
            self.gromacs.gmx.__dict__[cmd] = _utils.json.loads(_utils.json.dumps(self.gromacs.gmx.__dict__[cmd]),
            object_hook=lambda item: _utils.SimpleNamespace(**item))

        self.gromacs.pdb = self.id
        self.gromacs.property = {prop:None for prop in kwargs.get('MD').get('property')}
        self.gromacs.version = kwargs.get('MD').get('lib')[0]
        self.gromacs.analysis = kwargs.get('MD').get('analysis')
        self.gromacs.outputs = kwargs.get('MD').get('outputs')

        # [VAR_STYLE][GROMACS][PROPERTY] gromacs.property['POT'].output['xvg']
        for prop in self.gromacs.property.keys():
            self.gromacs.property[prop] = {
                'value': None,
                'output': None,
            }
            self.gromacs.property[prop] = _utils.json.loads(_utils.json.dumps(
                self.gromacs.property[prop]), object_hook=lambda item: _utils.SimpleNamespace(**item))

            if prop in ['SOL', 'Sol', 'sol']:
                self.gromacs.property['SOL'].output = {
                    'polar': {
                        'xvg': None,
                    },
                    'apolar': {
                        'xvg': None,
                    }
                }
            else:
                self.gromacs.property[prop].output = {
                    'xvg': None,
                }


        self.gromacs.gmx.pdb2gmx.output = {
            'gro': None,
            'top': None,
            'itp': None,
        }
        self.gromacs.gmx.editconf.output = {
            'gro': None,
        }
        self.gromacs.gmx.grompp.output = {
            'tpr': None,
            'mdp': None
        }
        self.gromacs.gmx.mdrun.output = {
            'gro': None,
            'edr': None,
            'log': None,
            'trr': None,
            'xtc': None,
        }

    def gromacsIO(self, gmx_cmd=None, property=None, dir=False, format=".ent"):
        prot = {
            'filename': None,
            'output': None,
            'analysis': None,
        }
        prot = _utils.json.loads(_utils.json.dumps(
            prot), object_hook=lambda item: _utils.SimpleNamespace(**item))

        prot.filename = "{}pdb{}{}".format(
            self.simulation['proteins']['dir'], self.pdb, format)
        prot.analysis = "{}{}/".format(self.gromacs.results.analysis, self.pdb)
        prot.output = "{}{}/".format(self.gromacs.results.outputs, self.pdb)

        if dir == True:
            try:
                _utils.os.mkdir(prot.output)
            except OSError as error:
                _utils.shutil.rmtree(prot.output)
                _utils.os.mkdir(prot.output)
            try:
                _utils.os.mkdir(prot.analysis)
            except OSError as error:
                _utils.shutil.rmtree(prot.analysis)
                _utils.os.mkdir(prot.analysis)

        if property is not None:
            self.gromacs.property[property].output['xvg'] = "{}{}_{}{}".format(
                prot.analysis, self.pdb, property, '.xvg')

        if property == "SOL":
            self.gromacs.property[property].output['polar']['xvg'] = "{}{}_{}polar{}".format(
                prot.analysis, self.pdb, property, '.xvg')
            self.gromacs.property[property].output['apolar']['xvg'] = "{}{}_{}apolar{}".format(
                prot.analysis, self.pdb, property, '.xvg')

        if gmx_cmd == 'pdb2gmx':
            self.pdbfile = prot.filename
            self.gromacs.gmx.pdb2gmx.output['gro'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.gro')
            self.gromacs.gmx.pdb2gmx.output['top'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.top')
            self.gromacs.gmx.pdb2gmx.output['itp'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.itp')

        if gmx_cmd == 'editconf':
            self.gromacs.gmx.editconf.output['gro'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.gro')

        if gmx_cmd == 'grompp':
            self.gromacs.gmx.grompp.output['tpr'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.tpr')
            self.gromacs.gmx.grompp.output['mdp'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.mdp')

        if gmx_cmd == 'mdrun':
            self.gromacs.gmx.mdrun.output['gro'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.gro')
            self.gromacs.gmx.mdrun.output['edr'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.edr')
            self.gromacs.gmx.mdrun.output['log'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.log')
            self.gromacs.gmx.mdrun.output['trr'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.trr')
            self.gromacs.gmx.mdrun.output['xtc'] = '{}{}_{}{}'.format(
                prot.output, self.pdb, gmx_cmd, '.xtc')

# ---------------------------------------------------------
# RUNNING SIMULATION FOR EACH PDB
# ---------------------------------------------------------
    def run(self, protein):
        for pdb in self.gromacs.pdbs:
            self.pdb = pdb

            protein[pdb].update({
                'property': dict(),
            })

            self.pdb2gmx()
            self.editconf()

            for prop in self.gromacs.property.keys():
                prop = prop.upper()

                if self.gromacs.implicit.mode and prop in self.gromacs.implicit.property:
                    self.implicit = True
                else:
                    self.implicit = False

                protein[pdb]['property'].update({
                    prop: None,
                })

                self.gromacsIO(pdb, property=prop)

                # Potential energy
                if prop == 'POT':
                    self.grompp()
                    self.mdrun()
                    # self.mdrun(rerun=True)
                    self.g_energy(group=prop)
                    protein[pdb]['property'][prop] = self.gromacs.property[prop].value

                # Radius of Gyration
                if prop == 'RG':
                    self.grompp()
                    self.mdrun()
                    self.gyrate(group='C-alpha')
                    protein[pdb]['property'][prop] = self.gromacs.property[prop].value

                # Solvation energy
                if prop == 'SOL':
                    self.grompp()
                    self.mdrun()
                    # self.mdrun(rerun=True)
                    self.g_mmpbsa(group='Protein')
                    protein[pdb]['property'][prop] = self.gromacs.property[prop].value

# ----------------------------------------------------------
# Step #1: pdb2gmx
# ----------------------------------------------------------
    def pdb2gmx(self):

        self.gromacsIO(gmx_cmd='pdb2gmx', dir=True)

        self.gromacs.gmx.pdb2gmx.cli = gmx.commandline_operation(
            'gmx',
            arguments=['pdb2gmx', '-ignh', '-ff',
                       'amber99sb-ildn', '-water', 'none', '-ter'],
            input_files={'-f': self.pdbfile},
            output_files={
                '-p': self.gromacs.gmx.pdb2gmx.output['top'],
                '-o': self.gromacs.gmx.pdb2gmx.output['gro'],
                '-i': self.gromacs.gmx.pdb2gmx.output['itp']
            }
        )
        cmd = self.gromacs.gmx.pdb2gmx.cli
        cmd.run()

        if cmd.output.erroroutput.result() != '':
            print(cmd.output.erroroutput.result())

# ----------------------------------------------------------
# Step #2: editconf
# ----------------------------------------------------------
    def editconf(self):

        self.gromacsIO(gmx_cmd='editconf')

        self.gromacs.gmx.editconf.cmd = gmx.commandline_operation(
            'gmx',
            arguments=['editconf', '-c', '-d', '1', '-bt', 'cubic'],
            input_files={
                '-f': self.gromacs.gmx.pdb2gmx.output['gro']
            },
            output_files={
                '-o': self.gromacs.gmx.editconf.output['gro'],
            }
        )
        cmd = self.gromacs.gmx.editconf.cmd
        cmd.run()

        if cmd.output.erroroutput.result() != '':
            print(cmd.output.erroroutput.result())

# ----------------------------------------------------------
# Step #3: grompp
# ----------------------------------------------------------
    def grompp(self):

        self.gromacsIO(gmx_cmd='grompp')

        if self.implicit:

            self.gromacs.gmx.grompp.cmd = {
                'grompp -maxwarn 1 ': ' ',
                '-f': self.gromacs.mdp,
                '-c': self.gromacs.gmx.editconf.output['gro'],
                '-p': self.gromacs.gmx.pdb2gmx.output['top'],
                '-o': self.gromacs.gmx.grompp.output['tpr'],
                '-po': self.gromacs.gmx.grompp.output['mdp'],
            }

            cmd = ". /home/hyprotein/gmx-{}/bin/GMXRC;".format(
                self.gromacs.implicit.version)
            cmd += ' '.join("{:<4}{}".format(key, val)
                            for (key, val) in self.gromacs.gmx.grompp.cmd.items())
            cmd += ' > /dev/null 2>&1'

            result = _utils.subprocess.Popen(
                cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
            erro = result.stderr.read().decode("ascii", "ignore")

        else:
            self.gromacs.gmx.grompp.cmd = gmx.commandline_operation(
                'gmx',
                arguments=['grompp', '-maxwarn', '1'],
                input_files={
                    '-f': self.gromacs.mdp,
                    '-c': self.gromacs.gmx.editconf.output['gro'],
                    '-p': self.gromacs.gmx.pdb2gmx.output['top'],
                },
                output_files={
                    '-o': self.gromacs.gmx.grompp.output['tpr'],
                    '-po': self.gromacs.gmx.grompp.output['mdp']
                }
            )
            cmd = self.gromacs.gmx.grompp.cmd
            cmd.run()

            if cmd.output.erroroutput.result() != '':
                print(cmd.output.erroroutput.result())

# ----------------------------------------------------------
# Step #4: mdrun
# ----------------------------------------------------------
    def mdrun(self, rerun=False):

        self.gromacsIO(gmx_cmd='mdrun')

        if self.implicit:
            if rerun:
                self.gromacs.gmx.mdrun.cmd = {
                    'mdrun': "",
                    '-s': self.gromacs.gmx.grompp.output['tpr'],
                    '-rerun': self.gromacs.gmx.editconf.output['gro'],
                    '-e': self.gromacs.gmx.mdrun.output['edr'],
                }

                cmd = ". /home/hyprotein/gmx-{}/bin/GMXRC;".format(
                    self.gromacs.implicit.version)
                cmd += ' '.join("{:<7}{}".format(key, val)
                                for (key, val) in self.gromacs.gmx.mdrun.cmd.items())
                result = _utils.subprocess.Popen(
                    cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
                erro = result.stderr.read().decode("ascii", "ignore")

            else:
                self.gromacs.gmx.mdrun.cmd = {
                    'mdrun': "",
                    '-s': self.gromacs.gmx.grompp.output['tpr'],
                    '-c': self.gromacs.gmx.mdrun.output['gro'],
                    '-e': self.gromacs.gmx.mdrun.output['edr'],
                    '-o': self.gromacs.gmx.mdrun.output['trr'],
                    '-x': self.gromacs.gmx.mdrun.output['xtc'],
                    '-g': self.gromacs.gmx.mdrun.output['log'],
                }

                cmd = ". /home/hyprotein/gmx-{}/bin/GMXRC;".format(
                    self.gromacs.implicit.version)
                cmd += ' '.join("{:<4}{}".format(key, val)
                                for (key, val) in self.gromacs.gmx.mdrun.cmd.items())
                result = _utils.subprocess.Popen(
                    cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
                erro = result.stderr.read().decode("ascii", "ignore")

        else:
            if rerun:
                self.gromacs.gmx.mdrun.cmd = gmx.commandline_operation(
                    'gmx',
                    arguments=['mdrun', '-v'],
                    input_files={
                        '-s': self.gromacs.gmx.grompp.output['tpr'],
                        '-rerun': self.gromacs.gmx.editconf.output['gro'],
                    },
                    output_files={
                        '-e': self.gromacs.gmx.mdrun.output['edr'],
                    }
                )
                cmd = self.gromacs.gmx.mdrun.cmd
                cmd.run()

                if cmd.output.erroroutput.result() != '':
                    print(cmd.output.erroroutput.result())

            else:
                self.gromacs.gmx.mdrun.cmd = gmx.commandline_operation(
                    'gmx',
                    arguments=['mdrun', '-v'],
                    input_files={
                        '-s': self.gromacs.gmx.grompp.output['tpr'],
                    },
                    output_files={
                        '-c': self.gromacs.gmx.mdrun.output['gro'],
                        '-e': self.gromacs.gmx.mdrun.output['edr'],
                        '-o': self.gromacs.gmx.mdrun.output['trr'],
                        '-x': self.gromacs.gmx.mdrun.output['xtc'],
                        '-g': self.gromacs.gmx.mdrun.output['log'],
                    }
                )
                cmd = self.gromacs.gmx.mdrun.cmd
                cmd.run()

                if cmd.output.erroroutput.result() != '':
                    print(cmd.output.erroroutput.result())


# ----------------------------------------------------------
# GROMACS PROPERTIES CALCULATION
# ----------------------------------------------------------

    def g_energy(self, group):

        opt = {
            "POT": "9",
        }

        cmd = {
            "echo {} | gmx energy".format(opt[group]): '',
            '-f': self.gromacs.gmx.mdrun.output['edr'],
            '-o': self.gromacs.property[group].output['xvg']
        }
        cmd = ' '.join("{:<4}{}".format(key, val)
                       for (key, val) in cmd.items())

        result = _utils.subprocess.Popen(
            cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
        erro = result.stderr.read().decode("ascii", "ignore")

        cmd = "tail " + self.gromacs.property[group].output['xvg'] + " -n 1"
        result = _utils.subprocess.Popen(cmd, shell=True, stdout=_utils.subprocess.PIPE)

        self.gromacs.property[group].value = result.stdout.read().decode(
            "ascii", "ignore").split()[-1]

    def g_mmpbsa(self, group, prop='SOL', mdp='mmpbsa.mdp'):

        opt = {
            'System': '0',
            'Protein': '1',
            'C-alpha': '3',
        }

        cmd = {
            'gmx': "trjconv",
            '-f': self.gromacs.gmx.mdrun.output['trr'],
            '-o': self.gromacs.gmx.mdrun.output['xtc'],
        }

        cmd = ' '.join("{:<4}{}".format(key, val)
                       for (key, val) in cmd.items())
        result = _utils.subprocess.Popen(
            cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
        erro = result.stderr.read().decode("ascii", "ignore")

        g_mmpbsa = {
            'echo {} | g_mmpbsa'.format(opt[group]): '',
            '-f': self.gromacs.gmx.mdrun.output['xtc'],
            '-s': self.gromacs.gmx.grompp.output['tpr'],
            '-i': "{}{}".format(self.simulation['MD']['mdp']['dir'], mdp),
            '-nomme': '',
            '-pbsa': '',
            '-nodiff': '',
            '-pol': self.gromacs.property[prop].output['polar']['xvg'],
            '-apol ': self.gromacs.property[prop].output['apolar']['xvg'],
        }

        cmd = ". /home/hyprotein/gmx-{}/bin/GMXRC;".format(
            self.gromacs.implicit.version)
        cmd += "export GMXLIB='/home/hyprotein/gmx-{}/share/gromacs/top';".format(
            self.gromacs.implicit.version)
        cmd += "export PATH=${PATH}:~/g_mmpbsa/bin/;"
        cmd += ' '.join("{:<8}{}".format(key, val)
                        for (key, val) in g_mmpbsa.items())

        result = _utils.subprocess.Popen(
            cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
        erro = result.stderr.read().decode("ascii", "ignore")

        cmd = "tail " + \
            self.gromacs.property[prop].output['polar']['xvg'] + " -n 1"
        polar = _utils.subprocess.run(
            cmd, shell=True, stdout=_utils.subprocess.PIPE, universal_newlines=True)

        cmd = "tail " + \
            self.gromacs.property[prop].output['apolar']['xvg'] + " -n 1"
        apolar = _utils.subprocess.run(
            cmd, shell=True, stdout=_utils.subprocess.PIPE, universal_newlines=True)

        self.gromacs.property[prop].value = float(
            polar.stdout.split()[1]) + float(apolar.stdout.split()[1])

    def gyrate(self, group, prop='RG'):

        opt = {
            'System': '0',
            'Protein': '1',
            'C-alpha': '3',
        }

        cmd = {
            'echo {} | gmx gyrate'.format(opt[group]): '',
            '-f': self.gromacs.gmx.mdrun.output['trr'],
            '-s': self.gromacs.gmx.mdrun.output['gro'],
            '-o': self.gromacs.property[prop].output['xvg']
        }
        cmd = ' '.join("{:<4}{}".format(key, val)
                       for (key, val) in cmd.items())

        result = _utils.subprocess.Popen(
            cmd, stdout=_utils.subprocess.PIPE, stderr=_utils.subprocess.PIPE, shell=True)
        erro = result.stderr.read().decode("ascii", "ignore")

        cmd = "tail " + self.gromacs.property[prop].output['xvg'] + " -n 1"

        result = _utils.subprocess.Popen(cmd, shell=True, stdout=_utils.subprocess.PIPE)

        self.gromacs.property[prop].value = result.stdout.read().decode(
            "ascii", "ignore").split()[1]
