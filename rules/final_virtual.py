import io
import os
import re

import _debrace
import _is_c_like
import _parse


#Attempts to find structs and classes that can be marked with the "final" C++ keyword;
#   classes that are parents (or children, by my convention, even though it is
#   unnecessary) should have a virtual destructor.  Classes that are not inheritable,
#   including children, should have a final modifier.

class RuleFinalVirtual(object):
    NAME = "Final/Virtual Use"
    
    @staticmethod
    def get_description(line_numbers):
        if len(line_numbers) == 1:
            result = "Possible class with final/virtual mismatch begins definition on line"
        else:
            result = "Possible classes with final/virtual mismatch begin definitions on lines"
        return result

    @staticmethod
    def rule(path,lines):
        if not _is_c_like.main(path): return [] #Can only operate on C/C++ files
        file = _parse.CFile(lines)
        file.remove_useless()

        result = set()
        for file_version in file.versions_iterator():
##            print("~~~~BEGIN~~~~")
            temp_str = "".join([line.altered+"\n" for line in file_version])
            blocks = _debrace.str_all(temp_str)
##            if len(blocks) == 1: continue #Cannot contain any classes/structs
##            for elem in blocks:
##                print(elem)
##            raw_input()

            #                    (start/ws)       (type)    ws  (name) (ws final)? (ws : ws (access)? ws (parent))? ws* end
            regex_defopen = "(\\A|(?<!enum)\\s+)(class|struct)\\s+(\\w+)(\\s+final)?(\\s*:\\s*(\\w+)?\\s+([\\w:]+))?\\s*\\Z"

            RuleFinalVirtual._index = 0
            indices = []
            def parse_blocks(blocks):
                for i in range(len(blocks)):
                    block_i = blocks[i]
                    if type(block_i) == type(""): #note implies type(blocks[i+1])==type([])
##                        print(("block",block_i))
                        find1 = re.search(regex_defopen, block_i)
                        if find1:
                            _,classname,name,ws_final,_,access,parent = find1.groups()
                            has_final = ws_final is not None
##                            print(("FOUND",find.groups()))
##                            print(("FOUND!!!",classname,name,ws_final,access,parent))
##                            raw_input()

                            class_contents = "".join([block for block in blocks[i+1] if type(block)==type("")])
##                            raw_input(class_contents)
                            find2 = re.search("(\\A|\\s+)(virtual\\s+)?(inline\\s+)?~\\s*"+name+"\\s*\\(", class_contents)
                            if find2:
                                _,virt,_ = find2.groups()
                                has_virt = virt != None
                            else:
                                has_virt = False

                            bad = False
                            if parent == None: #not a child, but may be a parent
                                #if a parent, then should have virtual but not have final.
                                if has_virt and not has_final: pass
                                #otherwise, should not have virtual and should have final.
                                elif not has_virt and has_final: pass
                                else: bad = True
                            else: #a child.  May be a parent
                                if not has_virt: bad=True #Children should have virtual destructors
                                #final may or may not be appropriate
                            if bad:
                                offset = len(block_i) - len(find1.group()) #offset from block start to match start
                                while block_i[offset]!="c": offset+=1 #offset from match start to class definition beginning
##                                print("BLOCK:     \""+block_i+"\"")
##                                print("GROUP:     \""+find1.group()+"\" ("+str(offset)+")")
##                                print("REMAINDER: \""+temp_str[RuleMissingFinal._index+offset:]+"\"")
                                indices.append(RuleFinalVirtual._index+offset)
                        RuleFinalVirtual._index += len(block_i)
                    else:
                        RuleFinalVirtual._index += 1
                        parse_blocks(block_i)
                        RuleFinalVirtual._index += 1
            parse_blocks(blocks)

            i = 0
            length = 0
##            print(indices)
            for line in file_version:
                length += len(line.altered)+1
                while len(indices) > 0:
                    index = indices[0]
                    if length > index:
                        result.add(line.num)
                        indices=indices[1:]
                    else:
                        break
##            raw_input("Done:"+str(result))

##            print("~~~~~END~~~~~")
        return sorted(list(result))
