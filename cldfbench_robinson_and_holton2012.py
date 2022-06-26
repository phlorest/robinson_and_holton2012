import pathlib

import phlorest


class Dataset(phlorest.Dataset):
    dir = pathlib.Path(__file__).parent
    id = "robinson_and_holton2012"

    def cmd_makecldf(self, args):
        self.init(args)
        
        summary = self.raw_dir.read_tree(
            'pAP_beast_dollo-relaxed-clock.mcct.trees',
            remove_rate=True,
            detranslate=True)
        #args.writer.add_summary(summary, self.metadata, args.log)

        posterior = self.raw_dir.read_trees(
            'pAP_beast_dollo-relaxed-clock.trees.gz',
            burnin=1000, sample=1000, detranslate=True)
        args.writer.add_posterior(posterior, self.metadata, args.log)

        args.writer.add_data(
            self.raw_dir.read_nexus('AP_splits.nex'),
            self.characters,
            args.log)
