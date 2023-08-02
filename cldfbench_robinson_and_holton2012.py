import pathlib

import phlorest


def fix_nexus(s):
    # The data file lists 5 duplicate cognate sets. Here we make the character
    # labels unique.
    dups = [
        '1968',  # >---332_walk-1,
        '1969',  # >---332_walk-0,
        '1970',  # >---332_walk-3,
        '1971',  # >---332_walk-2,
        '1972',  # >---332_walk-4,
    ]
    lines = []
    for line in s.split('\n'):
        words = line.split()
        if words and words[0] in dups:
            line = line.replace('_walk-', '_walk-dup-')
        lines.append(line)
    return '\n'.join(lines)


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "robinson_and_holton2012"

    def cmd_makecldf(self, args):
        self.init(args)
        
        summary = self.raw_dir.read_tree(
            'pAP_beast_dollo-relaxed-clock.mcct.trees',
            detranslate=True)
        args.writer.add_summary(summary, self.metadata, args.log)

        posterior = self.raw_dir.read_trees(
            'pAP_beast_dollo-relaxed-clock.trees.gz',
            burnin=1000, sample=1000, detranslate=True)
        args.writer.add_posterior(posterior, self.metadata, args.log)

        args.writer.add_data(
            self.raw_dir.read_nexus('AP_splits.nex', preprocessor=fix_nexus),
            self.characters,
            args.log)
