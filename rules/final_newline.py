#In C++ prior to C++0x (C++11), all nonempty files must end in a newline.  Although
#   codifying it in a standard seems extreme, there are admittedly good reasons to do
#   it.  It simplifies preprocessing and plays more nicely with terminal tools.  See
#   e.g. http://stackoverflow.com/questions/729692/why-should-files-end-with-a-newline
#Because of the widespread prevalence of noncompliant code, all compilers will accept
#   code without a trailing newline, although some will complain (see e.g.
#   "Weof-newline").
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
        if len(lines) == 0: #Empty files are not considered by the standard to be lacking a newline.
            return []
        if lines[-1][-1] != "\n":
            return [len(lines)]
        return []
