import os
import traceback

import files

#List of rules to use
import rules.leading_space
import rules.trailing_whitespace
rules = [
    #Comment out any here that you don't want.
    rules.leading_space.RuleLeadingSpace,
    rules.trailing_whitespace.RuleTrailingWhitespace
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

        lines2 = []
        for line in lines:
            if line.endswith("\n"): lines2.append(line[:-1])
            else:                   lines2.append(line     )

        output = ""
        for rule in rules:
            occurred = rule.rule(lines2)
            if len(occurred) > 0:
                output += TERMINAL_INDENT+rule.get_description(filename,occurred)+"\n"

                num_output_lines = 0
                last_line_number = -1
                for line_number in range(1,len(lines2)+1,1):
                    if line_number in occurred:
                        if num_output_lines >= MAX_OUTPUT_PER_FILE-1:
                            output += TERMINAL_INDENT+TERMINAL_INDENT+"[more occurrence(s) follow]\n"
                            break
                        if last_line_number!=-1 and last_line_number+1<line_number:
                            output += TERMINAL_INDENT+TERMINAL_INDENT+"...\n"
                            num_output_lines += 1

                        out_ln = TERMINAL_INDENT+TERMINAL_INDENT+"%d: \"%s\"\n" % (line_number,lines2[line_number-1])
                        out_ln = out_ln.replace("\t",TERMINAL_INDENT)
                        if len(out_ln)>TERMINAL_WIDTH-1: out_ln=out_ln[:TERMINAL_WIDTH-5]+"...\"\n"
                        output += out_ln

                        num_output_lines += 1
                        last_line_number = line_number
        if len(output) > 0:
            print("\""+path+"\":")
            print(output[:-1])
            if PAUSE_FILE: input(TERMINAL_INDENT+"Press ENTER to continue.")
    if PAUSE_COMPLETE: input("Press ENTER to quit.")

if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        input()
