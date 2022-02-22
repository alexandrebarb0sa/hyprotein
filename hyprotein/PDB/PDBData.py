import pandas as pd

class PDBData:
    def __init__(self, protein) -> None:
        self.protein = protein
        self.name = list(self.protein.keys())[0]

    def to_dict(self):
        if isinstance(self.protein, dict):
            return self.protein

    def pandas(self):
        protein, name = self.protein, self.name
        # protein[name].update({'B':dict(list(protein[name]['A'].items())[0:5])})
        chains = list(protein[name].keys())
        columns = list(list(protein[name][chains[0]].values())[0].keys())

        idx = {chain: None for chain in chains}
        res = {chain: None for chain in chains}

        for chain in chains:
            id = protein[name][chain].keys()
            res[chain] = protein[name][chain].values()

            idx[chain] = pd.MultiIndex.from_product([list(chain), id])

            idx[chain] = [
                (name,) + x for x in idx[chain].values
            ]

            idx[chain] = pd.Index(idx[chain])

        idx = idx.values()
        idx = [item for chain in idx for item in chain]
        idx = pd.Index(idx, name=('PROTEIN', 'CHAIN', 'RES_SEQ'))

        res = res.values()

        data = [item for residues in res for item in residues]
        data = [d.values() for d in data]

        df = pd.DataFrame(data=data, columns=columns, index=idx)

        return df
