#Split first layer of braces.  E.g. "a{b}c{d{e}f}g" |-> ["a","{b}","c","{d{e}f}","g"] 
def str_first(string):
    result = []
    current = ""
    counter = 0
    for c in string:
        if c == "{":
            if counter == 0:
                if len(current) > 0:
                    result.append(current)
                    current = ""
            counter += 1
            current += "{"
        elif c == "}":
            assert counter >= 1
            if counter == 1:
                if len(current) > 0:
                    result.append(current+"}")
                    current = ""
            else:
                current += "}"
            counter -= 1
        else:
            current += c
    if len(current) > 0:
        result.append(current)
    return result
#Split all layers of braces.  E.g. "a{b}c{d{e}f}g" |-> ["a",["b"],"c",["d",["e"],"f"],"g"]
def str_all(string):
    temp = str_first(string)
    result = []
    for elem in temp:
        if elem[0] == "{":
            result.append(str_all(elem[1:-1]))
        else:
            result.append(elem)
    return result

if __name__ == "__main__":
    test = "a{b}c{d{e}f}g"
    print(test)
    print(str_first(test))
    print(str_all(test))
    input()
