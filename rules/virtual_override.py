import re

import rules._is_c_like as _is_c_like
import rules._parse as _parse


#If a method is marked `override`, ensure it is marked `virtual` too.

class RuleVirtualOverride(object):
    NAME = "Virtual/Override"

    @staticmethod
    def get_description(line_numbers):
        result = "Possible method"
        if len(line_numbers)>1: result+="s"
        result += " tagged `override` but without `virtual` qualifier"
        if len(line_numbers)>1: result+="s"
        result += " on line"
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

            find = re.search("(inline\\s+)?virtual\\s+.*", text)
            if find: continue

            #                 (ret)  ws (qual::) (method)\(  args... \) ??? override
            find = re.search("(\\w+)\\s*(\\w+::)?(\\w+)\\([^\\(\\)]*\\)([^;\\{]*\\s+)?override", text)
            if find:
                result.append(line.num)

        return result
