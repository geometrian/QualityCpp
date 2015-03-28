import os
import re

#Any unnecessarily qualified object instance is marked.  See
#   http://stackoverflow.com/questions/29293136/compiler-warning-for-unnecessary-namespaces

###Note excluding system headers
##include_regex = re.compile("^\s*#\s*include\s*\"[^\"]+\"")

#Requires CPIP (http://cpip.sourceforge.net/index.html)
try:
    #To install, do not use the setup.py script; it is broken.  Instead, just copy the "cpip" folder
    #   into "[python]/Lib/site-packages/".
    from cpip.core import IncludeHandler
    from cpip.core import PpLexer
    from cpip.core import PragmaHandler
    CPIP_available = True
except:
    CPIP_available = False
    print("Skipping unnecessary qualification rule; CPIP not available!  See this rule for installation instructions.")


class RuleUnnecessaryQualification(object):
    NAME = "Unnecessary Qualification"
    
    @staticmethod
    def get_description(line_numbers):
        result = "Unecessary qualification on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not CPIP_available: return []
        if not (\
            path.endswith(".h") or\
            path.endswith(".hpp") or\
            path.endswith(".c") or\
            path.endswith(".cc") or\
            path.endswith(".cpp") or\
            path.endswith(".cxx")\
        ): return [] #Can only operate on C/C++ files

        includes = IncludeHandler.CppIncludeStdOs(
            theUsrDirs=[],
            theSysDirs=[]
        )
        pragma = PragmaHandler.PragmaHandlerNull()
        #cpip/core/PpLexer.py:204
        lexer = PpLexer.PpLexer(path,includes,None,None,pragma,None,None)
        tokens = []
        for token in lexer.ppTokens(minWs=True):
            if token.lineNum==0: continue #Whitespace, apparently.
            tokens.append((token.lineNum,token.t))

        result = []

        #If there's a stack underflow here, it probably means your code has mismatched braces.  Check it with
        #   a real compiler.
        stack = []
        i = 0
        while True:
            if i==len(tokens): break
            line_number,token = tokens[i]
            if   token == "namespace": #[namespace] [name] [{]
                namespace = tokens[i+1][1]
                stack.append(namespace+"{")
                i += 3
            elif token == "{": #block
                stack.append(token)
                i += 1
            elif token == "}":
                stack = stack[:-1]
                i += 1
            else:
                T = [token]
                while tokens[i+1][1] == "::":
                    T.append(tokens[i+2][1])
                    i += 2
                current_namespace = []
                for entry in stack:
                    if entry != "{":
                        current_namespace.append(entry[:-1])
                #print(current_namespace)
                while len(current_namespace) > 0:
                    if T[0] == current_namespace[0]:
                        result.append(line_number)
                        break
                    current_namespace = current_namespace[1:]
                i += 1
        
        #print(path)

##        #Evaluate preprocessor
##        reached = []
##        def preprocess(dir,lines):
##            lines2 = []
##            for line_number,line in lines:
##                if include_regex.match(line) != None:
##                    include = line.split("\"")[1]
##                    path2 = os.path.normpath(os.path.join(dir,include))
##                    if path2 in reached: continue
##                    reached.append(path2)
##                    #raw_input("Including \"%s\"" % (include))
##
##                    file = open(path2,"r")
##                    include_file = file.readlines()
##                    file.close()
##
##                    lines2 += preprocess(os.path.dirname(path2),zip( [None]*len(include_file), include_file ))
##                lines2.append((line_number,line))
##            return lines2
##        lines2 = preprocess(os.path.dirname(path),zip( range(1,len(lines)+1,1), lines ))
##        #raw_input(lines2)

        return result
