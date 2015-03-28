#Any line beginning with at least one leading space is marked.

class RuleLeadingSpace(object):
    NAME = "Leading Space"

    @staticmethod
    def get_description(line_numbers):
        result = "Beginning with space(s) on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        result = []

        line_number = 1
        for line in lines:
            if len(line)>=2 and line[0]==" ":
                result.append(line_number)
            line_number += 1

        return result
