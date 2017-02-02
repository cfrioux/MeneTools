# Copyright (c) 2012, Sven Thiele <sthiele78@gmail.com>
#
# This file is part of pyasp.
#
# pyasp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyasp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyasp.  If not, see <http://www.gnu.org/licenses/>.import random

import sys

def quote(s):
    return '"' + s + '"'

def unquote(s):
    if s[:1] == '"' and s[-1:] == '"':
        return s[1:-1]
    else:
        return s

# code taken from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
import locale

def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)

def get_max_width(table, index):
    """Get the maximum width of the given column index"""

    return max([len(format_num(row[index])) for row in table])


def pprint_table(table, out=sys.stdout):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """

    col_paddings = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out
# end stealing code
