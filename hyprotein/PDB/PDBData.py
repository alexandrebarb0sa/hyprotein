import pandas as pd

class PDBData:
    def __init__(self, protein) -> None:
        self.protein = protein
        self.pdb = list(self.protein.keys())[0]

    def to_dict(self):
        if isinstance(self.pdb, dict):
            return self.pdb

    def pandas(self):
        pdb, protein = self.pdb, self.protein
        # pdb[protein].update({'B':dict(list(pdb[protein]['A'].items())[0:5])})
        chains = list(protein[pdb].keys())
        columns = list(list(protein[pdb][chains[0]].values())[0].keys())
        # columns = [item.upper() for item in columns]

        idx = {chain: None for chain in chains}
        res = {chain: None for chain in chains}

        for chain in chains:
            id = protein[pdb][chain].keys()
            res[chain] = protein[pdb][chain].values()

            idx[chain] = pd.MultiIndex.from_product([list(chain), id])

            idx[chain] = [
                (pdb,) + x for x in idx[chain].values
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
