#Any line ending in trailing whitespace is marked.

class RuleTrailingWhitespace(object):
    @staticmethod
    def get_description(filename,line_numbers):
        result = "Trailing whitespace on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(lines):
        result = []

        line_number = 1
        for line in lines:
            if len(line)>=1 and line[-1] in [" ","\t"]:
                result.append(line_number)
            line_number += 1

        return result
