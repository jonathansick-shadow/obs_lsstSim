#!/usr/bin/env python
from glob import glob
from lsst.pipe.tasks.ingest import IngestTask
class SimIngestTask(IngestTask):
    def run(self, args):
        """Ingest all specified files and add them to the registry"""
        filenameList = sum([glob(filename) for filename in args.files], [])
        context = self.register.openRegistry(args.butler, create=args.create, dryrun=args.dryrun)
        with context as registry:
            for infile in filenameList:
                if self.isBadFile(infile, args.badFile):
                    self.log.info("Skipping declared bad file %s" % infile)
                    continue
                fileInfo, hduInfoList = self.parse.getInfo(infile)
                if self.isBadId(fileInfo, args.badId.idList):
                    self.log.info("Skipping declared bad file %s: %s" % (infile, fileInfo))
                    continue
                if self.register.check(registry, fileInfo):
                    self.log.warn("%s: already ingested: %s" % (infile, fileInfo))
                outfile = self.parse.getDestination(args.butler, fileInfo, infile)
                ingested = self.ingest(infile, outfile, mode=args.mode, dryrun=args.dryrun)
                if not ingested:
                    continue
                if 'eimage' not in outfile:
                    '''Don't add a row for the eimages since there are already rows for all amps'''
                    for info in hduInfoList:
                        self.register.addRow(registry, info, dryrun=args.dryrun, create=args.create)
            self.register.addVisits(registry, dryrun=args.dryrun)
SimIngestTask.parseAndRun()