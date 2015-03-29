import io
import os
import re

#Any unnecessarily qualified object instance is marked.  See
#   http://stackoverflow.com/questions/29293136/compiler-warning-for-unnecessary-namespaces


###Note excluding system headers
##include_regex = re.compile("^\s*#\s*include\s*\"[^\"]+\"")


def _strip_comments(lines):
    lines2 = []
    comment_mode = False

    for i in range(len(lines)):
        line = lines[i]
        line2 = ""
        j = 0
        while j < len(line):
            if not comment_mode:
                if line[j]=="/" and j+1<len(line) and (line[j+1]=="*" or line[j+1]=="/"):
                    if line[j+1] == "/":
                        line2 += "\n"
                        break
                    else: comment_mode=True
                    j += 2
                else:
                    line2 += line[j]
                    j += 1
            else:
                if line[j]=="*" and j+1<len(line) and line[j+1]=="/":
                    comment_mode = False
                    j += 2
                else:
                    if line[j] == "\n":
                        line2 += "\n"
                    j += 1
        lines2.append(line2)
    return lines2

#Based on an extremely simple lexical analysis/preprocessing.  Makes no attempt to parse
#   "#include"s or "#define"s.  As such, this does not catch any issues related to
#   macroed namespaces (and indeed, it may report false positives for such).  Searches
#   in all preprocessor branches (in a sane way, so e.g. this code, which has mismatched
#   braces lexically, won't screw it up):
#       #if 1
#           namespace Foo {
#       #else
#           namespace FooBar {
#       #endif
#               /*...*/
#           }
#   Does not search in comments.  TODO: maybe should?  It also definitely doesn't work
#   well (if at all) with using declarations

class RuleUnnecessaryQualification(object):
    NAME = "Unnecessary Qualification"
    
    @staticmethod
    def get_description(line_numbers):
        result = "Unecessary qualification on line"
        if len(line_numbers)>1: result+="s"
        return result

    @staticmethod
    def rule(path,lines):
        if not (\
            path.endswith(".h") or\
            path.endswith(".hpp") or\
            path.endswith(".c") or\
            path.endswith(".cc") or\
            path.endswith(".cpp") or\
            path.endswith(".cxx")\
        ): return [] #Can only operate on C/C++ files

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

        #Remove comments
        lines2 = _strip_comments(lines)

        #Create a recursive stack of nested preprocessor conditionals and extract a recursive stack of
        #   C/C++ tokens.  For the regular expression sorcery used to do this, see this:
        #   #https://deplinenoise.wordpress.com/2012/01/04/python-tip-regex-based-tokenizer/
        regex = re.compile(
            "(::)|"+          #scope
            "(\\s+)|"+        #whitespace
            "(\\{)|"+         #open brace
            "(\\})|"+         #close brace
            "([a-zA-Z]+\\w*)" #identifier
        )
        class Stack(object):
            def __init__(self, lines,offset, level):
                self.elements_sections = [[]]

                self.level = level

                self.start = offset

                i = offset + 1
                while i < len(lines):
                    line = lines[i]
                    if   "#if" in line:
                        element = Stack(lines,i,level+1)
                        self.elements_sections[-1].append(element)
                        i = element.end
                    elif "#elif" in line or "#else" in line:
                        self.elements_sections.append([])
                    elif "#endif" in line:
                        break
                    else:
                        self.elements_sections[-1].append( (i+1,line) )
                    i += 1

                self.end = i
            def get_tokens(self):
                tokens = []
                for section in self.elements_sections:
                    section_tokens = []
                    for element in section:
                        if type(element) == type(()):
                            for match in re.finditer(regex,element[1]):
                                scope, whitespace, openbrace, closebrace, iden = match.groups()
                                #raw_input((scope, whitespace, iden))
                                if        scope!=None: section_tokens.append((element[0],     scope))
                                elif  openbrace!=None: section_tokens.append((element[0], openbrace))
                                elif closebrace!=None: section_tokens.append((element[0],closebrace))
                                elif       iden!=None: section_tokens.append((element[0],      iden))
                        else:
                            section_tokens.append(element.get_tokens())
                    tokens.append(section_tokens)
                return tokens
            def __repr__(self):
                def get_indent(level):
                    return "  "*level
                result = get_indent(2*self.level)+"begin stack\n"
                for section in self.elements_sections:
                    result += get_indent(2*self.level+1)+"begin section\n"
                    for element in section:
                        if type(element) == type(()):
                            result += get_indent(2*self.level+2)+"Line %d: \"%s\"\n" % (element[0],element[1][:-1])
                        else:
                            result += str(element) #recurse
                    result += get_indent(2*self.level+1)+"end section\n"
                result += get_indent(2*self.level)+"end stack\n"
                return result
        stack = Stack(lines2,0, 0)
##        print(stack); raw_input()

        #For each line in this recursive stack, get the associated list of tokens.  This produces
        #   another recursive stack, with each element a token instead of a line.
        tokens = stack.get_tokens()
##        def print_tokens(tokens,depth):
##            for token in tokens:
##                if type(token) == type([]):
##                    print("  "*depth + "begin")
##                    print_tokens(token,depth+1)
##                    print("  "*depth + "end")
##                else:
##                    print("  "*depth + "%d: \"%s\""%token)
##        print_tokens(tokens,0); raw_input()

        #Flatten this stack into a list of tokens broken up by namespace declarations, open braces, and closing braces.
        #   Then find any overqualified tokens
        result = []
        def flatten(stack_base, tokens, depth):
##            def print_stacks(with_unfinished=True):
##                if with_unfinished: print("  "*depth + "Stack is now: "+str(namespace_stack)+" + "+str(unfinished_stacks))
##                else:               print("  "*depth + "Stack is now: "+str(namespace_stack))
            i = 0
            namespace_stack = list(stack_base)
            unfinished_stacks = []
            while i < len(tokens):
                element = tokens[i]
##                print_stacks()
##                print("  "*depth + "ELEMENT: "+str(element))
                if type(element) == type([]):
##                    print("  "*depth + "begin")
                    ret = flatten(namespace_stack, element, depth+1)
                    if len(ret) > 0:
##                        print("  "*depth + "Got unfinished stack: "+str(ret))
                        for us in unfinished_stacks: assert len(us)==len(ret) #Different preprocessor sides have different depths.  Not implemented!
                        unfinished_stacks.append(ret)
##                        print_stacks()
##                    print("  "*depth + "end")
                    i += 1
                else:
                    line_number,token = element
                    if token == "namespace": #[namespace] [name] [{]
                        assert i+2 < len(tokens) and type(tokens[i+1])==type(()) and type(tokens[i+2])==type(())
                        namespace = tokens[i+1][1]
                        #Skip brace
                        namespace_stack.append(namespace+"{")
##                        print_stacks()
                        i += 3
                    elif token == "{": #block
                        namespace_stack.append(token)
##                        print_stacks()
                        i += 1
                    elif token == "}": #end block or namespace
                        namespace_stack = namespace_stack[:-1]
##                        print_stacks()
                        i += 1
                    else: #an identifier or keyword
                        T = [token]
                        while i+1<len(tokens) and type(tokens[i+1])==type(()) and tokens[i+1][1]=="::":
                            T.append(tokens[i+2][1])
                            i += 2
                        def check(stack,T):
##                            print("Checking: "+str(stack))
                            if len(stack)==0: return
                            elem0 = stack[0]
                            if type(elem0) == type(""):
                                if T[0] == elem0[:-1]:
                                    result.append(line_number)
                                    return
                                check(stack[1:],T)
                            else:
                                for substack in elem0:
                                    check(substack,T)
                        if len(unfinished_stacks)>0: check(namespace_stack+[unfinished_stacks],T)
                        else:                        check(namespace_stack,T)
                        i += 1
            if len(unfinished_stacks)>0: namespace_stack.append(unfinished_stacks)
##            print_stacks(False)
            if len(namespace_stack) > len(stack_base):
                return list(namespace_stack[len(stack_base):])
            return []
        flatten([], tokens, 0)

##        tokens = []
##        for token in lexer.ppTokens(minWs=True):
##            if token.lineNum==0: continue #Whitespace, apparently.
##            tokens.append((token.lineNum,token.t))

##        #If there's a stack underflow here, it probably means your code has mismatched braces.  Check it with
##        #   a real compiler.
##        stack = []
##        i = 0
##        while True:
##            if i==len(tokens): break
##            line_number,token = tokens[i]
##            if   token == "namespace": #[namespace] [name] [{]
##                namespace = tokens[i+1][1]
##                stack.append(namespace+"{")
##                i += 3


        return result
