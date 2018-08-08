exist_directory = {}


def get_information(index):
    dictionary = {
        0: 'protection bits',
        1: 'inode number',
        2: 'device',
        3: 'number of hard links',
        4: 'user id of owner',
        5: 'group id of owner',
        6: 'size of file',
        7: 'time of most recent access',
        8: 'time of most recent content modification',
        9: 'time of creation',
        10: 'hash of file'
    }
    return dictionary[index]


def sha256_sum(filename, blocksize=65536):
    import hashlib
    hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def write_to_file(directory, parameters):
    with open("base_of_files.txt", 'a') as output_parameters:
        output_parameters.write(directory + '\t')
        for i in range(len(parameters)):
            if i == len(parameters) - 1:
                output_parameters.write(str(parameters[i]) + '\n')
            else:
                output_parameters.write(str(parameters[i]) + '\t')


def read_from_file():
    files = {}
    with open("base_of_files.txt", 'r+') as input_parameters:
        for line in input_parameters:
            splited_line = line.split('\t')
            length = len(splited_line)
            params_len = len(splited_line[length - 1])
            if splited_line[length - 1][params_len - 1] == '\n':
                x = splited_line[length - 1][0:(params_len - 1)]
                splited_line[length - 1] = x
            files[splited_line[0]] = splited_line[1:]
    return files


def check_file(directory, parameters, files):
    if directory not in files:
        print("New file or directory: {}\n".format(directory))
    else:
        flag = False
        for i in range(len(parameters)):
            if files[directory][i] != parameters[i]:
                if not flag:
                    flag = True
                    print("In the file {} have been changed next parameters: \n".format(directory))
                if flag:
                    old_value = files[directory][i]
                    new_value = parameters[i]
                    if 7 <= i <= 9:
                        from datetime import datetime
                        old_value = datetime.fromtimestamp(int(files[directory][i])).strftime('%Y-%m-%d %H:%M:%S')
                        new_value = datetime.fromtimestamp(int(parameters[i])).strftime('%Y-%m-%d %H:%M:%S')
                    print("Parameter: {} ".format(get_information(i)))
                    print("Old value: {}".format(old_value))
                    print("New value: {}\n".format(new_value))
        exist_directory[directory] = True


def list_of_files(directory, method, files=None):
    try:
        import os
        for file in os.listdir(directory):
            filename = os.path.join(directory, file)
            if os.path.isfile(filename):
                info = os.stat(filename)
                parameters = []
                for i in range(len(info)):
                    parameters.append(str(info[i]))
                parameters.append(str(sha256_sum(filename)))
                if method == '1':
                    write_to_file(filename, parameters)
                elif method == '2':
                    check_file(filename, parameters, files)
            if os.path.isdir(filename):
                list_of_files(filename, method, files)
    except:
        print("You haven't got permissions to read attributes of this file or folder {}\n".format(directory))


def disk_auditor():
    print("Type command: ", end="")
    command = input()
    if command == "create copy of area" or command == "1" or command == "create":
        print("Type directory: ", end="")
        directory = input()
        print()
        try:
            open("base_of_files.txt", 'r+').truncate()
            list_of_files(directory, '1')
            print("Successfully created a copy of the area {}".format(directory))
        except:
            print("Oops!\n")
    elif command == "check area" or command == "2" or command == "check":
        print("Type directory: ", end="")
        directory = input()
        print()
        files = read_from_file()
        for file in files.keys():
            exist_directory[file] = False
        try:
            list_of_files(directory, '2', files)
        except:
            print("Oops!\n")
        for file in exist_directory.keys():
            if not exist_directory[file]:
                print("No file in directory: {}\n".format(file))
    elif command == "help":
        print("\n1    create copy of area")
        print("2    check selected area\n")


if __name__ == '__main__':
    disk_auditor()
