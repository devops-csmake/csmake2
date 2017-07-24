# <copyright>
# (c) Copyright 2017 Hewlett Packard Enterprise Development LP
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# </copyright>
from Csmake.CsmakeModuleAllPhase import CsmakeModuleAllPhase
from Csmake.FileManager import MetadataFileTracker
from Csmake.MetadataManager import MetadataWarning, MetadataCurrent
import re
import copy

class translatePackageName(CsmakeModuleAllPhase):
    """Purpose: Allow a single name to be used in the metadata for a dependent
                package.  
       Type: Module   Library: csmake (core)
       Description:
           The metadata may include dependent names for packages.  Not every
           packaging scheme follows the same naming or naming conventions for
           packages.

           This module allows the build developer to define the desired
           translation from the name for a package used in the metadata to
           a name that suits the packaging scheme.

           A Packager derived module, for example, may consult this section
           for the apropos package name for a given package.

           The section should be defined with an id that is the canonical name
           for the package desired to be used in the metadata surrounded by
           tildes to avoid any overlapping ids.

           The lookup will look for a section defined:
                [translatePackageName@~~<package>~~]
               (where <package> is the canonical name desired for the package)

       Phases: *any*
       Options:
           <key> - <package name(s)>
                   Where <key> is the packaging scheme target
                   <package name(s)> is the name(s) of the package
                        in the given format
           ~~format~~ - Modules invoking this section should supply this field
                        however, if this is supplied in the build spec, then
                        this value will override what the calling section
                        attempts to define.
                        If this section is undefined, the original string
                        will be passed through.
       Example:
           [metadata@myproduct]
           name: myproduct
           depends: python, anotherproduct

           #The ~~ avoids collision with the python section
           [translatePackageName@~~anotherproduct~~]
           rpm=another-project, another-project-devel
           alpine=anotherpjt

           [translatePackageName@~~python~~]
           rpm=python-minimal, python-devel
           debian=python, python-dev

           [Shell@python]
           command=python -m myMod
    """

    def __init__(self, env, log):
        CsmakeModuleAllPhase.__init__(self, env, log)
        self.files = MetadataFileTracker(self, self.log, self.env)
        self.id = None

    def __repr__(self):
        return "<<translatePackageName step definition>>"

    def __str__(self):
        return "<<translatePackageName metadata step definition>>"

    def default(self, options):
        actualId = self.actualId.strip('~')
        self.log.passed()
        if '~~format~~' not in options:
            return actualId
        transFormat = options['~~format~~']
        if transFormat not in options:
            self.log.info(
                "Package '%s' had no translation defined for format (%s)", actualId, transFormat)
            return actualId
        transId = options[transFormat]
        self.log.debug(
            "Translating: %s to %s (%s)",
            actualId,
            transId,
            transFormat )
        return transId
