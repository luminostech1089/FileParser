#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This modules parse the text file and provides methods to easily fetch
desired lines from file.
"""

# --- LICENSE ------------------------------------------------------------------

# Copyright (c) [2015], [Abhijit Ghongade]

# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.

# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
# ------------------------------------------------------------------------------

__version__ = '0.01'
__date__ = '2015-10-01'
__author__ = 'Abhijit Ghongade'

import re


class LogFile:
    def __init__(self, filename):
        try:
            self.file_obj = open(filename, "r")
            self.line_no = 1
            self.offset = 0
            self.total_lines = sum(1 for line in self.file_obj)
        except:
            raise Exception('Unable to open file [{}] in read mode'.format(filename))

    def searchLine(self, pattern, count=1, start_from=0, match=0):
        """
        Search string or pattern in log file and returns the lines in which
        pattern or string is found.
        :param pattern: Pattern or string to search in log file
               start_from: Line number to start from. Default is 0.
               count: Parameter to search number of occurrences of matched pattern.
               match: Exact pattern match with line.
        :return: List of tuple having first value as line in which matched pattern
                 or string is found, second value is line number, and third value
                 is pointer to previous line.
        """
        count = self.total_lines if count == 'max' else count
        if start_from > 0:
            self.goToLine(start_from)
        else:
            self.goToStart()
        isdone = False
        eof = False
        output = []
        match_pat = re.compile(pattern)
        while not eof and not isdone:
            prev = self.file_obj.tell()
            line = self.file_obj.readline()
            if not line:
                eof = True
                continue
            self.line_no += 1
            self.offset = self.file_obj.tell()
            if match:
                ismatched = match_pat.match(line)
            else:
                ismatched = match_pat.search(line)
            if ismatched:
                count -= 1
                output.append((line, self.line_no - 1, prev))
            if count == 0:
                isdone = True

        return output

    def reverseSearchFromLine(self, line_no, pattern):
        """
        Search pattern or string in reverse direction from specified line number.
        :param line_no: Line to start reverse search from.
        :param pattern: Pattern to look for.
        :return: List of tuple having first value as line in which matched pattern
                 or string is found, second value is line number, and third value
                 is pointer to previous line.
        """
        count = 1
        data = []
        output = []
        eof = False
        self.goToStart()
        if line_no > self.total_lines:
            raise ValueError('Line count exceeds total number of lines in file')
        while not eof and count <= line_no:  # Go to desired line no
            prev = self.file_obj.tell()
            line = self.file_obj.readline()
            if not line:
                eof = True
                continue
            data.append((line, count, prev))
            count += 1
        if data:
            pattern_match = re.compile(pattern)
            for index in xrange(-1, -(len(data) + 1), -1):
                line_info = data[index]
                match = pattern_match.search(line_info[0])
                if match:
                    output.append(line_info)

        return output

    def fetchDataBetweenLines(self, start_pattern, end_pattern):
        """
        Returns all the lines between the lines where start line is the line
        in which start_pattern is found and end line is the line in which
        end_pattern is found.
        :param start_pattern: Pattern to search for line to start from.
        :param end_pattern: Pattern to search for line as end.
        :return: List of string having all lines
        """
        output = []
        output1 = self.searchLine(start_pattern)
        output2 = self.searchLine(end_pattern)
        if output1 and output2:
            output.append(output1[0][0].strip())
            self.goToLine(output1[0][1] + 1)
            line_start = self.line_no
            # Read lines till end line
            while line_start < output2[0][1]:
                output.append(self.file_obj.readline().strip())
                line_start += 1
            output.append(output2[0][0].strip())

        return output

    def fetchDataBetweenLineNos(self, start_line, end_line):
        """
        Returns all the lines between start line number and end line is the
        end line number.
        :param start_line: Line number to start from.
        :param end_line: End line number.
        :return: List of string having all lines between start_line and end_line
        """
        output = []
        # Validate line numbers
        if start_line > self.total_lines or end_line > self.total_lines:
            raise ValueError('Start or end line number can not be more than total '
                             'number of lines in a file')
        if start_line < 0 or end_line < 0:
            raise ValueError('Start or end line numbers must be non zero')
        self.goToLine(start_line)
        # Read lines till end line
        while start_line <= end_line:
            output.append(self.file_obj.readline().strip())
            start_line += 1
        return output

    def fetchDataAroundLine(self, pattern, scope=0, up=None, down=None):
        """
        Search for line having specified pattern. If found return x number of
        lines(scope) above and bellow the matched line including matched line.
        if up or down scope is specified, given number of lines will be fetched
        above and below respectively from matched line.
        :param pattern: Pattern to search for line.
        :param scope: Number of lines to fetch above and below the matched line.
        :return: List of matched lines.
        """
        output = []

        if scope < 0:
            raise ValueError('Negative value of scope is not allowed')
        if up and up < 0:
            raise ValueError('Negative value for up scope is not allowed')
        if down and down < 0:
            raise ValueError('Negative value for down scope is not allowed')

        search_output = self.searchLine(pattern)

        scope_up = up if up else scope
        scope_down = down if down else scope
        if search_output:
            start_line = search_output[0][1] - scope_up
            end_line = search_output[0][1] + scope_down

            # round off start and end line values
            start_line = 1 if start_line < 1 else start_line
            end_line = self.total_lines if end_line > self.total_lines else end_line
            self.goToLine(start_line)

            while start_line <= end_line:
                output.append(self.file_obj.readline().strip())
                start_line += 1
        return output

    def goToStart(self):
        """
        Move pointer to the start of file.
        :return:
        """
        self.file_obj.seek(0, 0)
        self.line_no = 1
        self.offset = 0

    def goToLine(self, lineno):
        """
        Move file pointer to specified line number.
        :param lineno: Line number to move file pointer to.
        :return:
        """
        # Go to start and move pointer to given line no
        self.goToStart()
        line_count = 1
        eof = False
        pos = 0
        while not eof and line_count != lineno:
            line = self.file_obj.readline()
            if not line:
                eof = True
                continue
            pos = self.file_obj.tell()
            line_count += 1

        self.line_no = line_count
        self.offset = pos

    def readline(self, lineno=None):
        if lineno:
            self.goToLine(lineno)
        line = self.file_obj.readline()
        if line:  # If not EOF
            self.line_no += 1
        return line

    @property
    def currentLineNo(self):
        return self.line_no

    def __del__(self):
        if self.file_obj:
            self.file_obj.close()
