import os
import pefile

from utils import disable_file_system_redirection


def help():
    print('1  Scanning by signatures')
    print('2  Scanning by hash\n')


def init():
    signature = '12 FF 15 89 40 00 00 8B D0 B9 24 27 00 00 E8 A9'
    lst = []
    for item in signature.split():
        lst.append(int(item, 16))
    st_signature = bytes(lst)
    st_hash = "c85fdeb424b2de117a2cf609f01dfcfd0ac4c237408223e6bdac01b4b6fb398d"
    return st_signature, st_hash


def is_dll(pe):
    if hasattr(pe, 'FILE_HEADER'):
        if pe.FILE_HEADER.IMAGE_FILE_DLL:
            return True

    if hasattr(pe, 'OPTIONAL_HEADER'):
        if pe.OPTIONAL_HEADER.AddressOfEntryPoint == 0:
            return True
    return False


def parse_pe(pe):
    hash_code = ''

    if not is_dll(pe):
        name = pe.sections[0].Name.decode('utf-8')[1:5]
        if name == 'text':
            hash_code = pe.sections[0].get_hash_sha256()
    return hash_code


def search_virus(folder):
    directory = folder
    try:
        for file in os.listdir(directory):
            filename = os.path.join(directory, file)
            if os.path.isfile(filename):
                try:
                    pe = pefile.PE(filename, fast_load=True)
                except:
                    continue
                hash_code = parse_pe(pe)
                if mode == 1:
                    with open(filename, 'rb') as input_file:
                        if st_signature in input_file.read():
                            print('Found virus in file {}\n'.format(filename))
                elif mode == 2:
                    if hash_code == st_hash:
                        print('Found virus in file {}\n'.format(filename))
            elif os.path.isdir(filename):
                search_virus(filename)
    except:
        print("No access to {}\n".format(folder))


if __name__ == '__main__':
    st_signature, st_hash = init()

    help()
    print('Choose the mode of antivirus: ', end='')
    mode = int(input())
    print()
    print('Enter the directory: ', end='')
    directory = input()
    print()

    from time import clock
    start = clock()
    with disable_file_system_redirection():
        search_virus(directory)
    from datetime import timedelta
    print(str(timedelta(seconds=(clock() - start))))
