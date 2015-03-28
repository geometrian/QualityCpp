#Any line ending in trailing whitespace is marked.

class RuleTrailingWhitespace(object):
    NAME = "Trailing Whitespace"

    @staticmethod
    def get_description(line_numbers):
        result = "Trailing whitespace on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        result = []

        line_number = 1
        for line in lines:
            if len(line)>=2 and line[-2] in [" ","\t"]: #Note line[-1] is the newline
                result.append(line_number)
            line_number += 1

        return result
