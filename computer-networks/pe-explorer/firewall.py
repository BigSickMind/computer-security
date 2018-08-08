import os
import pefile

list_libraries = []
list_functions = []

def initialize():
    libraries = open("network_libraries.txt")
    for lib in libraries:
        size = len(lib)
        list_libraries.append(lib[:size - 1])

    functions = open("network_functions.txt")
    for func in functions:
        size = len(func)
        list_functions.append(func[:size - 1])

initialize()

def parse_pe(pe, filename):
    pe.parse_data_directories()

    libraries = []
    functions = []

    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        flag = False
        for libs in pe.DIRECTORY_ENTRY_IMPORT:
            lib = libs.dll.decode().lower()
            if lib in list_libraries:
                for funcs in libs.imports:
                    if funcs.name != None:
                        func = funcs.name.decode()
                        if func in list_functions:
                            libraries.append(lib)
                            functions.append(func)
                            flag = True
                            break
            if flag:
                break

    
    if len(libraries) and len(functions):
        print("File: " + filename)

        print("This file is using the following network libraries and functions: ", end="")

        for lib in libraries:
            for func in functions:
                print("Lib: " + lib + " Func: " + func + "\n")

def isUsingNetwork(folder):
    directory = folder
    try:
        for file in os.listdir(directory):
            filename = os.path.join(directory, file)
            if os.path.isfile(filename):
                try:
                    pe = pefile.PE(filename, fast_load=True)
                except:
                    continue
                parse_pe(pe, filename)

            elif os.path.isdir(filename):
                isUsingNetwork(filename)
    except:
        print("No access to " + folder)

print("Enter the directory:")
directory = input()

isUsingNetwork(directory)
