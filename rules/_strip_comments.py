import rules._line as _line


def main(lines):
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
        lines2.append(_line.Line(i+1, line,line2))

    return lines2
