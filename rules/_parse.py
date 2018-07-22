import itertools
import re

import rules._line as _line
import rules._strip_comments as _strip_comments


class CList(object):
    def __init__(self, bool_expr, elements):
        self.bool_expr = bool_expr
        self.elements = elements
    def get_repr(self,depth):
        def get_indent(depth): return "    "*depth
        result = get_indent(depth)
        if self.bool_expr==None: result+="<else>"
        else: result+="\""+self.bool_expr+"\""
        result += ":\n"
        for elem in self.elements:
            if type(elem)==type([]):
                for clist in elem:
                    result += clist.get_repr(depth+1)
                result += get_indent(depth+1) + "<end>\n"
            else:
                result += get_indent(depth+1) + repr(elem) + "\n"
        return result
    def __repr__(self):
        return self.get_repr(0)

class File(object):
    def __init__(self,lines):
        self.lines = [_line.Line(i+1,lines[i],lines[i]) for i in range(len(lines))]
    def __repr__(self):
        return "".join([line.__repr__() for line in self.lines])

class GFile(File):
    def __init__(self,lines):
        File.__init__(self,lines)
class CFile(File):
    def __init__(self,lines):
        File.__init__(self,lines)

    def remove_useless(self):
        lines = [line.real for line in self.lines]
        self.lines = []
        for line in _strip_comments.main(lines):
            altered = line.altered.strip()
            if len(altered) > 0:
                self.lines.append(_line.Line(line.num,line.real,altered))

    #Return a CList; define a CList as a boolean expression and a list of items, with each item being either a
    #   line of the file or a list of CLists.  The special conditional value "None" indicates an else block.
    #   Each list of CLists corresponds to a block of preprocessed options.  For example, if the file was:
    #       int a;
    #       #if FOO
    #           int b;
    #       #elif BAR
    #           int c;
    #       #else
    #           int d;
    #       #endif
    #       int e;
    #   Then the output would be:
    #       CList("true",[
    #           "int a;",
    #           [
    #               CList("FOO",[
    #                   "   int b;"
    #               ]),
    #               CList("BAR",[
    #                   "   int c;"
    #               ]),
    #               CList(None,[
    #                   "   int d;"
    #               ])
    #           ]
    #           "int e;"
    #       ])
    def get_preprocessed(self):
        lines = []
        for line in self.lines:
            macro_new = re.match("#\\s*if(def)?\\s*", line.altered)
            if macro_new:
                lines.append(( -1, line.altered[len(macro_new.group(0)):] ))
                continue
            macro_opt_elif = re.match("#\\s*elif\\s*", line.altered)
            if macro_opt_elif:
                lines.append(( -2, line.altered[len(macro_opt_elif.group(0)):] ))
                continue
            macro_opt_else = re.match("#\\s*else\\s*", line.altered)
            if macro_opt_else:
                lines.append(( -2, None ))
                continue
            macro_end = re.match("#\\s*endif\\s*", line.altered)
            if macro_end:
                lines.append(( -3, ))
                continue
            lines.append(line)
##        s = ""
##        for line in lines: s+=str(line)
##        input(s)

        def parse_block(lines,result):
            counter = 0
            for i in range(len(lines)):
                line = lines[i]
                if counter == 0:
                    if type(line)==type(()) and line[0]==-1:
                        counter += 1
                        options = []
                        option = CList(line[1],[])
                        continue
                    result.elements.append(line)
                else:
                    if type(line) == type(()):
                        if   line[0] == -1:
                            counter += 1
                        elif line[0] == -2:
                            if counter == 1:
                                if len(option.elements) > 0:
                                    options.append(option)
                                option = CList(line[1],[])
                                continue
                        else: #line[0] == -3
                            counter -= 1
                            if counter == 0:
                                if len(option.elements) > 0:
                                    options.append(option)
                                if len(options) > 0:
                                    for option in options:
                                        elements = list(option.elements)
                                        option.elements = []
                                        parse_block(elements,option)
                                    result.elements.append(options)
                                continue
                    option.elements.append(line)
        #lines = ["a",(-1,"FOO"),"b",(-3,),"c"]
        #lines = ["a",(-1,"FOO"),"b",(-2,None),"c",(-3,),"d"]
        #lines = ["a",   (-1,"FOO"), "b", (-1,"BAR"),"c",(-3,), "d", (-2,"BAZ"), "e", (-2,None), "f", (-3,),   "g"]
        line=CList("true",[]); parse_block(lines,line)

##        def get_output(block,level=0):
##            def get_line(string): return "".join([">>>" for i in range(level)]) + string + "\n"
##            s = ""
##            for item in block:
##                if type(item) == type([]):
##                    s += get_line("~~~~")
##                    for option in item:
##                        s += get_output(option,level+1)
##                        s += get_line("~~~~")
##                else:
##                    s += get_line(item.altered)
##            return s
##        input(get_output(subblock))

        return line
    #A generator that attempts to output the preprocessor permutations of a file in an intelligent way by generating
    #   Permutations of the file generated with various defines enabled.  If this is not computationally practical (e.g.,
    #   there are too many boolean variables, and since not includes are processed, there's no way of knowing which are
    #   valid, and we want to check all paths anyway), we simply generate one version with all paths enabled.  This can
    #   lead to incorrect result.
    def versions_iterator(self, limit=8):
        clist = self.get_preprocessed()
        elems = []
        
        bool_exprs = set()
        def add_bool_exprs(elements):
            for elem in elements:
                if type(elem) == type([]):
                    for clist in elem:
                        bool_exprs.add(clist.bool_expr)
                        add_bool_exprs(clist.elements)
        #TODO: remove numeric-only?
        add_bool_exprs(clist.elements)
        bool_exprs.discard(None)

        def add_lines(elements,true_combo):
            for elem in elements:
                if type(elem) == type([]):
                    for i in range(len(elem)):
                        if elem[i].bool_expr in true_combo or elem[i].bool_expr == None:
                            add_lines(elem[i].elements,true_combo)
                            break
                else:
                    result.append(elem)

        if len(bool_exprs) > limit:
            result = []
            add_lines(clist.elements,bool_exprs)
            yield result
        else:
            for true_combo in itertools.chain.from_iterable(itertools.combinations(bool_exprs,r) for r in range(len(bool_exprs)+1)): #powerset
                result = []
                add_lines(clist.elements,true_combo)
                yield result
