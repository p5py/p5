#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017 Abhik Pal
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import sys
from . import _p5

# we should be parsing sys args here and expose a series of commands
# similar to processing-java.
#
# relevant output from `processing-java --help`:
#
#     --help               Show this help text. Congratulations.
#    
#     --sketch=<name>      Specify the sketch folder (required)
#     
#     --output=<name>      Specify the output folder (optional and
#                          cannot be the same as the sketch folder.)
#                          
#     --force              The sketch will not build if the output
#                          folder already exists, because the contents
#                          will be replaced. This option erases the
#                          folder first. Use with extreme caution!
#                          
#     --build              Preprocess and compile a sketch into .class files.
#     
#     --run                Preprocess, compile, and run a sketch.
#     
#     --present            Preprocess, compile, and run a sketch in presentation mode.
#    
#     --export             Export an application.
#     
#     --no-java            Do not embed Java. Use at your own risk!
#     
#     --platform           Specify the platform (export to application only).
#                          Should be one of 'windows', 'macosx', or 'linux'.
#
                                                                                    
