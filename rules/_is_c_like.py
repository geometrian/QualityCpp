def main(path):
    return\
        path.endswith(  ".h") or\
        path.endswith(".hpp") or\
    \
        path.endswith(  ".c") or\
        path.endswith( ".cc") or\
        path.endswith(".cpp") or\
        path.endswith(".cxx")
