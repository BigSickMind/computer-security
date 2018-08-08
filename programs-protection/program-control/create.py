import os

FILENAME_IN = 'main1.exe'
FILENAME_ADD = 'main2.exe'
FILENAME_STICK = 'main2.exe'


def write_data(file_name, data1, data2, name1, name2):
    with open(file_name, 'bw') as f:
        f.write(data1)  # first file

        towrite = '1[]1'.encode('utf-8') + name1.encode('utf-8')
        f.write(bytes(towrite))
        f.write(data1)  # second file

        towrite = '1[]2'.encode('utf-8') + name2.encode('utf-8')
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


def main():
    stick_files(FILENAME_IN, FILENAME_ADD, FILENAME_STICK)
    os.remove('main1.exe')


if __name__ == '__main__':
    main()
