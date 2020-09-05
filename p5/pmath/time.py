#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2019 Abhik Pal
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

import time
import builtins


def millis():
    return int((time.perf_counter() - builtins.start_time) * 1000)


def day():
    return int(time.strftime("%d"))


def hour():
    return int(time.strftime("%H"))


def minute():
    return int(time.strftime("%M"))


def second():
    return int(time.strftime("%S"))


def year():
    return int(time.strftime("%Y"))
