import re

import rules._is_c_like as _is_c_like
import rules._parse as _parse


#If a method is marked override, ensure it is marked virtual too.

class RuleAlphabetizeExplicitInlineStaticVirtual(object):
    NAME = "Alphabetize \"explicit\"/\"inline\"/\"static\"/\"virtual\""

    @staticmethod
    def get_description(line_numbers):
        result = "Possible out-of-alphabetic-order keywords on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not _is_c_like.main(path): return [] #Can only operate on C/C++ files
        file = _parse.CFile(lines)
        file.remove_useless()

        result = []
        for line in file.lines:
            text = line.altered.strip()

            find = re.search("virtual\\s+inline", text)
            if find:
                result.append(line.num)
                continue

            find = re.search("inline\\s+explicit", text)
            if find:
                result.append(line.num)
                continue

            find = re.search("static\\s+inline", text)
            if find:
                result.append(line.num)
                continue

        return result
