def make_alph():
    alph = ""
    for i in range(ord('a'), ord('z') + 1):
        alph += chr(i)
    for i in range(ord('!'), ord('A') - 1):
        alph += chr(i)
    for i in range(ord('а'), ord('я') + 1):
        alph += chr(i)
    alph += 'ё'
    alph += ' '
    alph += "\""
    return alph


def read_keys_from_file():
    all_generated_keys = []
    generated_keys = {}
    with open('generated_keys.txt', 'r') as input_keys:
        for line in input_keys:
            if line[len(line) - 1] == '\n':
                line = line[:len(line) - 1]
            splited_line = line.split('\t')
            keys = []
            generated_key = eval(splited_line[0])
            mod = (generated_key[0] + generated_key[1]) % generated_key[2]
            for i in range(len(splited_line)):
                generated_key = eval(splited_line[i])
                keys.append(generated_key)
                all_generated_keys.append(generated_key)
            generated_keys[mod] = keys
    return all_generated_keys, generated_keys


def generate_keys(count):
    all_generated_keys, generated_keys = read_keys_from_file()

    from random import randint
    mod = randint(2, 1000)
    while mod in generated_keys.keys():
        mod = randint(2, 1000)

    new_generated_keys = []
    for i in range(count):
        a = randint(2, 1e9)
        n = randint(2, 1e5)
        b = randint(2, 1e9)
        while (a + b) % n != mod or (a, b, n) in all_generated_keys or (b, a, n) in all_generated_keys or (
                a, b, n) in new_generated_keys or (b, a, n) in new_generated_keys:
            b = randint(2, 1e9)
        new_generated_keys.append((a, b, n))

    with open('generated_keys.txt', 'w') as output_keys:
        for key in generated_keys:
            for i in range(len(generated_keys[key])):
                if i < len(generated_keys[key]) - 1:
                    output_keys.write(str(generated_keys[key][i]) + '\t')
                else:
                    output_keys.write(str(generated_keys[key][i]) + '\n')

        for i in range(len(new_generated_keys)):
            if i < len(new_generated_keys) - 1:
                output_keys.write(str(new_generated_keys[i]) + '\t')
            else:
                output_keys.write(str(new_generated_keys[i]) + '\n')

    print('Generation is finished successfully\n')


def encrypt(file, input_key):
    try:
        key = (input_key[0] + input_key[1]) % input_key[2]
    except:
        print('Not enough parameters of key\n')
        return

    text = ""
    try:
        with open(file, 'r', encoding='utf-8') as input_text:
            for line in input_text:
                text += line
    except IOError:
        print("You haven't access to this file, encryption is failed\n")
        return

    encrypted_text = ""
    for letter in text:
        encrypted_text += chr(ord(letter) ^ key)

    with open('encrypted_file.txt', 'w', encoding='utf-8') as output_text:
        output_text.write(encrypted_text)

    print('Encryption is finished successfully\n')


def decrypt(file, input_key):
    try:
        key = (input_key[0] + input_key[1]) % input_key[2]
    except:
        print('Not enough parameters of key\n')
        return

    encrypted_text = ""
    try:
        with open(file, 'r', encoding='utf-8') as input_text:
            for line in input_text:
                encrypted_text += line
    except IOError:
        print("You haven't access to this file, decryption is failed\n")
        return

    text = ""
    for letter in encrypted_text:
        text += chr(ord(letter) ^ key)

    with open('decrypted_file.txt', 'w', encoding='utf-8') as output_text:
        output_text.write(text)

    print('Decryption is finished successfully\n')


def file_encryption():
    print('1    generate keys')
    print('2    encrypt file')
    print('3    decrypt file\n')

    print("Type command: ", end="")
    command = input()
    print()

    if command == 'generate keys' or command == 'g' or command == 'generate' or command == '1':
        print('Number of keys to generate: ', end="")
        count = int(input())
        print()
        generate_keys(count)
    elif command == 'encrypt file' or command == 'encrypt' or command == 'e' or command == '2':
        print('Select the file to encrypt: ', end="")
        file = input()
        print('\nSelect the key to encrypt: ', end="")
        input_key = eval(input())
        print()
        encrypt(file, input_key)
    elif command == 'decrypt file' or command == 'decrypt' or command == 'd' or command == '3':
        print('Select the file to decrypt: ', end="")
        file = input()
        print('\nSelect the key to decrypt: ', end="")
        input_key = eval(input())
        print()
        decrypt(file, input_key)


if __name__ == '__main__':
    file_encryption()
