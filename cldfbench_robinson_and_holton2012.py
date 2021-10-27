import re
import pathlib

import nexus
import phlorest


def fix_nexus(p):
    """
    Separate the charlabels in a nexus file with commas.
    """
    text = p.read_text(encoding='utf8')
    occs = list(re.finditer(r'(?P<charlabel>[0-9]+\s+[0-9]+_[a-z_0-9.]+-[0-9]+)\n', text))
    new, i = [], 0
    for j, m in enumerate(occs, start=1):
        new.append(text[i:m.start()])
        new.append(m.group('charlabel') + ',' if j != len(occs) else '' + '\n')
        i = m.end()
    new.append(text[i:])
    return nexus.NexusReader.from_string(''.join(new))


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "robinson_and_holton2012"

    def cmd_makecldf(self, args):
        self.init(args)
        with self.nexus_summary() as nex:
            self.add_tree_from_nexus(
                args,
                self.read_nexus(
                    self.raw_dir / 'pAP_beast_dollo-relaxed-clock.mcct.trees', remove_rate=True),
                nex,
                'summary',
                detranslate=True,
            )
        posterior = self.sample(
            self.remove_burnin(
                self.read_gzipped_text(self.raw_dir / 'pAP_beast_dollo-relaxed-clock.trees.gz'),
                1000,
            ),
            detranslate=True,
            as_nexus=True)

        with self.nexus_posterior() as nex:
            for i, tree in enumerate(posterior.trees.trees, start=1):
                self.add_tree(args, tree, nex, 'posterior-{}'.format(i))

        self.add_data(args, fix_nexus(self.raw_dir / 'AP_splits.nex'))
