#Any line beginning with at least one leading space is marked.

class RuleLeadingSpace(object):
    @staticmethod
    def get_description(filename,line_numbers):
        result = "Beginning with space(s) on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(lines):
        result = []

        line_number = 1
        for line in lines:
            if len(line)>=1 and line[0]==" ":
                result.append(line_number)
            line_number += 1

        return result
