import re

import _is_c_like
import _parse


#Flags empty destructor bodies, which should be "default"ed.

class RuleDestructorDefault(object):
    NAME = "Destructor \"default\""

    @staticmethod
    def get_description(line_numbers):
        result = "Possible application of \"default\" for destructor on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not _is_c_like.main(path): return [] #Can only operate on C/C++ files
        file = _parse.CFile(lines)
        file.remove_useless()

        result = []
        for line in file.lines:
            #Note can be qualified or not (MyClass::)
            find = re.search("\\s*~\\s*\\w+\\(\\s*(void)?\\s*\\)\\s*\\{\\s*\\}", line.altered)
            if find:
                result.append(line.num)

        return result
