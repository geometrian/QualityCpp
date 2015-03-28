import os

import wx


#Any path containing any of these strings is ignored
_excludes_cont = [
    ".git", ".build", ".ides",
    "dirent-1.13",
    "CocoaWindow",
    "grub",
    "to port",
    "ToDo",
    "todo",
    "old"
]
#Any path ending in any of these strings is ignored.  By specifying excludes,
#   instead of specific includes (e.g. "h", "hpp", "c", "cpp"), this rule can
#   Be used for other file types.
_excludes_suff = [
    "asf",
    "blend","blend1","obj","mtl","stl",
    "bmp","jpg","pfm","png","ppm","tga",
    "hdr","f32","f32z",
    "py","pyc",
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

def _get_file_list(path):
    if path=="": return []

    result = []
    for name in os.listdir(path):
        found = False
        for s in _excludes_cont:
            if name in s: found=True
        if name.split(".")[-1] in _excludes_suff: found=True
        if found: continue

        path2 = os.path.join(path,name)

        if os.path.isdir(path2):
            result += _get_file_list(path2)
            continue
        result.append(path2)
    return result

def choose_files():
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
    paths = _get_file_list(file_picker.GetPath())
    app.Destroy()

    if paths==None: return []
    return paths
