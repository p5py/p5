#
# Part of p5: A Python package based on Processing
# Copyright (C) 2017-2018 Abhik Pal
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

import datetime

def day():
	return datetime.datetime.now().day

def hour():
	return datetime.datetime.now().hour

def millis():
	return datetime.datetime.now().microsecond

def minute():
	return datetime.datetime.now().minute

def second():
	return datetime.datetime.now().second

def year():
	return datetime.datetime.now().year

