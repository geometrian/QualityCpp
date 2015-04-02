import os
import traceback

import files

#List of rules to use
import rules.final_newline
import rules.numof
import rules.leading_space
import rules.trailing_whitespace
import rules.unnecessary_qualification
rules = [
    #Comment out any here that you don't want.
    rules.final_newline.RuleFinalNewline,
    rules.numof.RuleNumOf,
    rules.leading_space.RuleLeadingSpace,
    rules.trailing_whitespace.RuleTrailingWhitespace,
    rules.unnecessary_qualification.RuleUnnecessaryQualification
]

#Configuration
TERMINAL_INDENT = "  "
TERMINAL_WIDTH = 80
MAX_OUTPUT_PER_FILE = 20
PAUSE_FILE = True
PAUSE_COMPLETE = True


try: input=raw_input
except: pass


def main():
    paths = files.choose_files()

    for path in paths:
        filename = os.path.basename(path)

        file = open(path,"r")
        lines = file.readlines()
        file.close()

        output = ""
        for rule in rules:
            try:
                occurred = rule.rule(path,lines)
            except:
                print("Error occurred while applying rule \"%s\" to \"%s\":" % (rule.NAME,path))
                traceback.print_exc()
                occurred = []
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
            print("\""+path+"\":")
            print(output[:-1])
            if PAUSE_FILE: input(TERMINAL_INDENT+"Press ENTER to continue.")
    print("All files (%d) processed!"%len(paths))
    if PAUSE_COMPLETE: input("Press ENTER to quit.")

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        input()
