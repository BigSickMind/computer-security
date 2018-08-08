import os
from time import sleep, time

import psutil

FILE = 'main1.exe'
CUR_FILE = 'main2.exe'


def timeout():
    sleep(5)
    print("Waiting 5 sec")
    return True


def write_data(file_name, data1, data2, name1, name2):
    #print('Saving data with delimiter: {} {} in file {}'.format(name1, name2, file_name))
    with open(file_name, 'bw') as f:
        f.write(data1)  # first file

        towrite = '1[]1'.encode('utf-8') + name1.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data1)  # second file

        towrite = '1[]2'.encode('utf-8') + name2.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data2)  # third file


def add_files(file1, file2, file_cur):
    with open(file1, 'rb') as f:
        file = f.read()

    with open(file2, 'rb') as f:
        file_add = f.read()
    print(file1[-5])
    print(file2[-5])
    write_data(file_cur, file, file_add, file1[-5], file2[-5])


def get_files(file_cur):
    print('Start getting files {}'.format(file_cur))
    with open(file_cur, 'rb') as f:
        stick = f.read()

    eof1 = stick.find(bytes('1[]1'.encode('utf-8')))
    eof2 = stick.find(bytes('1[]2'.encode('utf-8')))
    file_name1 = 'tmp' + chr(int(stick[eof1 + 4])) + '.exe'
    file_name2 = 'tmp' + chr(int(stick[eof2 + 4])) + '.exe'
    for idx in range(5):
        print(chr(int(stick[eof1 + idx])), end='')
    print()
    print(file_name1)
    print(file_name2)
    print('index: ' + str(eof1))
    print('index: ' + str(eof2))

    file1 = stick[eof1+5:eof2]
    file2 = stick[eof2+5:]

    with open(file_name1, 'wb') as f:
        f.write(file1)
    with open(file_name2, 'wb') as f:
        f.write(file2)

    add_files(file_name2, file_name1, FILE)
    os.remove(file_name1)
    os.remove(file_name2)


def exist_process():
    start_time = time()
    for num, proc in enumerate(psutil.process_iter()):
        if proc.name() == FILE:
            print("Time on process finding {}\n".format(time() - start_time))
            return True
    print("Time on process finding {}\n".format(time() - start_time))
    return False


def exist_file():
    print('File deleted? {}\n'.format(FILE))
    return os.path.exists(FILE)


def restore_process():
    os.startfile(FILE)
    print("Process {} restored\n".format(FILE))


def restore_file():
    file = CUR_FILE
    get_files(file)
    print("File {} restored\n".format(FILE))


def main():
    print("Start finding {}\n".format(FILE))
    while timeout():
        if not exist_file():
            print("File {} deleted\n".format(FILE))
            restore_file()
        if not exist_process():
            print("Process {} deleted\n".format(FILE))
            restore_process()


if __name__ == '__main__':
    main()
