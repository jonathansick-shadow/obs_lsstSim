#!/usr/bin/env python
#
# LSST Data Management System
# Copyright 2008-2015 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <https://www.lsstcorp.org/LegalNotices/>.
#
import numpy

from lsst.pipe.base.argumentParser import ArgumentParser
from lsst.pipe.tasks.processCcd import ProcessCcdTask
from .eimageIsr import EimageIsrTask


class ProcessEimageConfig(ProcessCcdTask.ConfigClass):
    """Config for ProcessEimage"""

    def setDefaults(self):
        ProcessCcdTask.ConfigClass.setDefaults(self)
        self.isr.retarget(EimageIsrTask)
        self.calibrate.repair.doInterpolate = False
        self.calibrate.repair.doCosmicRay = False
        self.calibrate.measurePsf.psfDeterminer['pca'].reducedChi2ForPsfCandidates = 3.0
        self.calibrate.measurePsf.psfDeterminer['pca'].spatialReject = 2.0
        self.calibrate.measurePsf.psfDeterminer['pca'].nIterForPsf = 0
        self.calibrate.measurePsf.psfDeterminer['pca'].tolerance = 0.01


class ProcessEimageTask(ProcessCcdTask):
    """Process an Eimage CCD

    This variant of processCcdTask loads e-images as post-ISR images
    """
    ConfigClass = ProcessEimageConfig
    _DefaultName = "processEimage"

    def __init__(self, **kwargs):
        """Construct a ProcessEimageTask
        """
        ProcessCcdTask.__init__(self, **kwargs)
        numpy.random.seed(self.config.rngSeed)

    @classmethod
    def _makeArgumentParser(cls):
        """Create an argument parser
        """
        parser = ArgumentParser(name=cls._DefaultName)
        parser.add_id_argument("--id", "eimage", "data ID, e.g. visit=1 raft=2,2 sensor=1,1 snap=0")
        return parser
