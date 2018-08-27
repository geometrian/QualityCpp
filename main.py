import os
import sys
import traceback

import files

#List of rules to use
import rules.alphabetize_explicit_inline_static_virtual
import rules.destructor_default
import rules.final_newline
import rules.final_virtual
import rules.numof
import rules.leading_space
import rules.trailing_whitespace
import rules.unnecessary_qualification
import rules.virtual_override
import rules.void_argument
rules = [
    #Comment out any here that you don't want.
    rules.alphabetize_explicit_inline_static_virtual.RuleAlphabetizeExplicitInlineStaticVirtual,
    rules.destructor_default.RuleDestructorDefault,
    rules.final_newline.RuleFinalNewline,
    rules.final_virtual.RuleFinalVirtual,
    rules.numof.RuleNumOf,
    rules.leading_space.RuleLeadingSpace,
    rules.trailing_whitespace.RuleTrailingWhitespace,
    rules.unnecessary_qualification.RuleUnnecessaryQualification,
    rules.virtual_override.RuleVirtualOverride,
    rules.void_argument.RuleVoidArgument
]

#Configuration
TERMINAL_INDENT = "  "
TERMINAL_WIDTH = 80
MAX_OUTPUT_PER_FILE = 20
PAUSE_ON_FILEWARNING = True
PAUSE_ON_COMPLETE = True


try: input=raw_input
except: pass


def main():
    paths = files.choose_files()

    path_index = 0
    for path in paths:
        filename = os.path.basename(path)

        try:
            file = open(path,"r",encoding="utf8")
            lines = file.readlines()
            file.close()
        except:
            sys.stdout.write("\n")
            print("Error occurred while attempting to read file \"%s\":" % (path))
            traceback.print_exc()
            input()

        msg = "Processing file "+str(path_index+1)+" of "+str(len(paths))+": \""
        if len(msg)+len(path)+1<TERMINAL_WIDTH:
            msg += path+"\""
            msg += " "*(TERMINAL_WIDTH-len(msg)-1)
        else:
            msg += path[:TERMINAL_WIDTH-len(msg)-5] + "\"..."
        sys.stdout.write("\r"+msg); sys.stdout.flush()

        output = ""
        for rule in rules:
            try:
                occurred = rule.rule(path,lines)
            except:
                sys.stdout.write("\n")
                print("Error occurred while applying rule \"%s\" to \"%s\":" % (rule.NAME,path))
                traceback.print_exc()
                input()
            if len(occurred) > 0:
                len_largest_line_number = len(str(occurred[-1]))
                
                output += TERMINAL_INDENT+rule.get_description(occurred)+"\n"

                num_output_lines = 0
                last_line_number = -1
                for line_number in range(1,len(lines)+1,1):
                    if line_number in occurred:
                        if num_output_lines >= MAX_OUTPUT_PER_FILE-1:
                            output += TERMINAL_INDENT+TERMINAL_INDENT+"[more occurrence(s) follow]\n"
                            break
                        if last_line_number!=-1 and last_line_number+1<line_number:
                            output += TERMINAL_INDENT+TERMINAL_INDENT+"...\n"
                            num_output_lines += 1

                        out_ln = TERMINAL_INDENT+TERMINAL_INDENT+\
                            (len_largest_line_number-len(str(line_number)))*" " + str(line_number)+\
                            ": \""+lines[line_number-1]
                        if out_ln.endswith("\n"): out_ln=out_ln[:-1]
                        out_ln += "\"\n"
                        out_ln = out_ln.replace("\t",TERMINAL_INDENT)
                        if len(out_ln)>TERMINAL_WIDTH-1: out_ln=out_ln[:TERMINAL_WIDTH-5]+"...\"\n"
                        output += out_ln

                        num_output_lines += 1
                        last_line_number = line_number
        if len(output) > 0:
            sys.stdout.write("\r"+" "*(TERMINAL_WIDTH-1)+"\r");
            print("\""+path+"\":")
            print(output[:-1])
            if PAUSE_ON_FILEWARNING: input(TERMINAL_INDENT+"Press ENTER to continue.")
        path_index += 1
    sys.stdout.write("\r"+" "*(TERMINAL_WIDTH-1)+"\r");
    print("All files (%d) processed!"%len(paths))
    if PAUSE_ON_COMPLETE: input("Press ENTER to quit.")

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        input()
