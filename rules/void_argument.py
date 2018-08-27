import re

import rules._is_c_like as _is_c_like
import rules._parse as _parse


#Flags `void` as a way to indicate a function takes no arguments (this is a bad holdover from C).
#   Will give false positives on C files.  This is because there's no easy way to tell when a
#   C-like source file is C++.  E.g. ".h" is used widely for C++.

class RuleVoidArgument(object):
    NAME = "C `void` Function Argument"

    @staticmethod
    def get_description(line_numbers):
        result = "Possible C-like `void` function argument on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not _is_c_like.main(path): return [] #Can only operate on C/C++ files
        file = _parse.CFile(lines)
        file.remove_useless()

        result = []
        for line in file.lines:
            find = re.search("\\(\\s*void\\s*\\)", line.altered)
            if find:
                result.append(line.num)

        return result
