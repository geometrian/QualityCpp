#Any line containing `numof_` is marked (as in `int numof_foo;`).  I prefer `num`.

class RuleNumOf(object):
    NAME = "Leading Space"

    @staticmethod
    def get_description(line_numbers):
        result = "Containing `numof_` on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        result = []

        line_number = 1
        for line in lines:
            if "numof_" in line:
                result.append(line_number)
            line_number += 1

        return result
