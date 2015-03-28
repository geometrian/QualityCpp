#In C++ prior to C++0x (C++11), files must end in a newline.  Although codifying it in
#   a standard seems extreme, there are admittedly good reasons to do it.  It simplifies
#   preprocessing and plays more nicely with terminal tools.
#Because of the widespread prevalence of noncompliant code, all compilers will accept
#   code without a trailing newline, although some will complain.
#For portable, correct code, having a trailing newline is good practice.

class RuleFinalNewline(object):
    NAME = "Final Newline"
    
    @staticmethod
    def get_description(line_numbers):
        result = "Missing final newline in file"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if lines[-1][-1] != "\n":
            return [len(lines)]
        return []
