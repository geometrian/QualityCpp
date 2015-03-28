import wx
import sys, os, traceback


try: input=raw_input
except: pass

excludes_cont = [
    "dirent-1.13",
    "CocoaWindow",
    "grub",
    "to port",
    "ToDo",
    "todo",
    "old"
]
excludes_suff = [
    "asf",
    "blend","blend1","obj","mtl","stl",
    "bmp","jpg","pfm","png","ppm","tga",
    "hdr","f32","f32z",
    "py",
    "lnk",
    #"lua",
    "opensdf","sdf","suo",
    "bin","dat","elf","img","out",
    "sogol",
    "ttf",
    "txt",
    "wav",
    "xml",
    "zip"
]

def get_file_list(path):
    result = []
    for name in os.listdir(path):
        if ".git" in name or ".build" in name or ".ides" in name: continue

        found = False
        for s in excludes_cont:
            if name in s:
                found = True
        if name.split(".")[-1] in excludes_suff:
            found = True

        if found: continue
        
##        if "." in name: raw_input(name)
        path2 = os.path.join(path,name)

        if os.path.isdir(path2):
            result += get_file_list(path2)
            continue
        result.append(path2)
    return result;

def choose_file():
    #FileDialog/DirDialog
    app = wx.PySimpleApp()
    
##    file_picker = wx.FileDialog(
##        None,
##        #wildcard=".h Header (*.h)|*.h|.CPP Source (*.cpp)|*.cpp",
##        style=wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_MULTIPLE|wx.FD_FILE_MUST_EXIST
##    )
##    file_picker.ShowModal()
##    paths = file_picker.GetPaths()
##    app.Destroy()

    file_picker = wx.DirDialog(
        None,
        #wildcard=".h Header (*.h)|*.h|.CPP Source (*.cpp)|*.cpp",
        style=wx.FD_OPEN|wx.FD_CHANGE_DIR|wx.FD_MULTIPLE|wx.FD_FILE_MUST_EXIST
    )
    file_picker.ShowModal()
    paths = get_file_list(file_picker.GetPath())
##    raw_input(paths)
    app.Destroy()
    
    return paths
def error_condition(lines,message):
    result = ""
    if len(lines) > 0:
        result += "  "+message
        if len(lines) > 1: result += "s"
        result += "\n"

        i = 0
        for line_number,line in lines:
            if i <= 20:
                line = line.replace("\t","    ")
                out_ln = "    "+str(line_number)+": \"%s\"\n" % (line)
                if len(out_ln)>79: out_ln=out_ln[:75]+"...\""
                result += out_ln
            else:
                result += "    ...\n"
                break
            i += 1

    return result

def main():
    paths = choose_file()
    if paths == [] or paths == None: sys.exit()

    for path in paths:
        file = open(path,"r")
        data = file.readlines()
        file.close()

        if len(data) > 0:
            spaced_lines_start = []
            spaced_lines_trailing = []

            line_number = 1
            for line in data:
                if len(line) >= 2:
                    if line[-1]=="\n": line=line[:-1] #remove newline
                    if line[-1] in [" ","\t"]:
                        spaced_lines_trailing.append((line_number,line))
                    if line[0] == " ":
                        spaced_lines_start.append((line_number,line))
                line_number += 1

            output = ""
            output += error_condition(spaced_lines_start,"Beginning with space(s) on line")
            output += error_condition(spaced_lines_trailing,"Trailing whitespace on line")
            if "\n" not in data[-1]: output+="Missing newline in file"
            if len(output) != 0:
                print("\""+path+"\":")
                print(output)
                input("Press ENTER to continue.")
            
    input("Press ENTER to quit.")
    
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        input()
