import email
import re
domain_template = re.compile(r"(([a-zA-Z0-9]+(-[a-zA-Z0-9]+)*\.)+[a-z]{2,10})")

def isSpam(file):
    try:
        fl = open(file, 'r').read()
    except UnicodeDecodeError:
        try:
            fl = open(file, 'r', encoding='cp1252').read()
        except UnicodeDecodeError:
            print("Message has invalid encoding")
            exit()

    msg = email.message_from_string(fl)

    spam = 0

    counter_apparently_to = 0

    from_str = ''
    return_path = ''

    in_reply_to = []
    references = []

    domain_from = ''
    domain_message_id = ''


    to = ['smirnoved5@mail.ru', 'lester0@rambler.ru', 'lester0578@gmail.com']
    found_to = False

    needed_fields = {
        'to': False,
        'from': False,
        'return-path': False,
        'received': False
    }

    received_fields = []

    for string in msg._headers:
        field = string[0].lower()
        if field == "from":
            needed_fields[field] = True
            flag = True
            for j in range(1, len(string)):
                pos_dog = string[j].find('@')
                if pos_dog == -1 or pos_dog == 0:
                    spam += 30
                    print("Incorrect type of template ****@***.**** in field From " + string[j] + '\n')
                    flag = False
                    break
                flag = False
                i = pos_dog
                while i > 0 and string[j][i] != '<' and string[j][i] != ' ':
                    i -= 1
                from_str = string[j][(i):(len(string[j]) - 1)]
                domain_from = from_str[(pos_dog + 1):len(from_str)]
                break

            if flag:
                spam += 10
                print("Not found email of sender\n")

        elif field == "return-path":
            needed_fields[field] = True
            if string[1][0] == '<' and string[1][1] == '>':
                return_path = ''
            else:
                return_path = string[1][1:(len(string[1]) - 1)]

        elif field == 'message-id':
            pos_dog = string[1].find('@')
            if pos_dog == -1 or pos_dog == 0:
                spam += 30
                print("Incorrect type of template ****@***.**** in field Message-ID " + string[1] + '\n')
                continue
            if pos_dog + 1 < len(string[1]) and string[1][pos_dog + 1].isalpha():
                domain_message_id = string[1][(pos_dog + 1):(len(string[1]) - 1)]
            else:
                spam += 30
                print("Incorrect type of template ****@***.**** in field Message-ID " + string[1] + '\n')

        elif (field == 'to' or field == 'cc' or field == 'bcc') and not found_to:
            if field == 'to':
                needed_fields[field] = True
            for j in range(1, len(string)):
                for mails in to:
                    pos = string[j].find(mails)
                    if pos != -1:
                        found_to = True
                        break
                        
        elif field == 'received':
            needed_fields[field] = True
            received_fields.append(string[1])

        elif field == "apparently-to":
            counter_apparently_to += 1

        elif field == 'in-reply-to':
            in_reply_to = [string[j] for j in range(1, len(string))]

        elif field == 'references':
            references = [string[j] for j in range(1, len(string))]

    prev_from_domain = ''
    for num, content in enumerate(received_fields):
        start = re.search('from|by', content)
        if hasattr(start, 'group'):
            found = start.group(0)
            start = content.find(found) + len(found) + 1
            was_from = False
            if content[start - 2] == 'm':
                was_from = True
            from_domain = ''
            if was_from:
                from_domain = content[start: content.find(' ', start)]
                start += len(from_domain)

                if re.search('[a-zA-Z]', from_domain) is None:
                    from_domain = ''
                else:
                    if domain_template.search(from_domain) is None:
                        print("Invalid data in 'Received', field num " + str(num + 1) + " : after 'from' domain " + from_domain + " is invalid\n")
                        spam += 30
                        break

                if content[start + 1] != '(':
                    print("Invalid data in 'Received', field num " + str(num + 1) + ": no brackets with ip of sender\n")
                    spam += 10
                    break

                in_brackets = content[start + 1: content.find(')', start + 1)]
                start = content.find(' ', len(in_brackets) + 1) + 1
                from_domain_inbrackets = domain_template.search(in_brackets)
                if not hasattr(from_domain_inbrackets, 'group'):
                    print("After word 'from', in brackets, in 'Received' field num " + str(num + 1) + ", sender's domain is not provided\n")
                    spam += 30
                    break
                else:
                    from_domain_inbrackets = from_domain_inbrackets.group(0)
                    if from_domain_inbrackets[-1] == '.':
                        from_domain_inbrackets = from_domain_inbrackets[:-1]
                    if from_domain == '':
                        from_domain = from_domain_inbrackets
                    elif 'helo' not in in_brackets.lower() and from_domain != from_domain_inbrackets:
                        print("After word 'from', in 'Received' field num " + str(num + 1) + ", sender's domain is not corresponding to one"
                              " that provided dns postback\n")
                        spam += 10
                        break

            if was_from:
                start = content.find('by', start + 1)
            if start == -1:
                if not was_from and (num != 0 or num != len(received_fields) - 1):
                    print("Invalid values in 'Received', field num " + str(num + 1) + "\n")
                    spam += 30
                    break
            else:
                if was_from:
                    start += 3
                by_domain = content[start: content.find(' ', start)]
                start += len(by_domain) + 1
                if re.search('[a-zA-Z]', by_domain) is None:
                    by_domain = ''
                else:
                    if domain_template.search(by_domain) is None:
                        print("Invalid data in 'Received', field num " + str(num + 1) + " : after 'by' domain " + by_domain + " is invalid\n")
                        spam += 30
                        break

                if prev_from_domain != '' and prev_from_domain != by_domain:
                    print("'Chain is broken' 'from' " + prev_from_domain + " domain doesn't match with 'by' domain " + by_domain + "\n")
                    spam += 30
                    break

            prev_from_domain = from_domain
        else:
            print("Wrong field num " + str(num + 1) + " 'Received': has no 'from' and 'by'\n")
            spam += 30
            break

    for x in needed_fields:
        if not needed_fields[x]:
            print("There is now field " + x + " in message\n")
            spam += 30

    if needed_fields['to'] and not found_to:
        spam += 10
        print("Not found my emails in receivers in fields To, CC or BCC\n")

    if needed_fields['return-path'] and (from_str != return_path or return_path == ''):
        if return_path == '':
            spam += 30
            print("No email in return-path\n")
        else:
            spam += 10
            print("Field From " + from_str + " and field Return-Path " + return_path + " doesn't match\n")

    elif domain_from != domain_message_id:
        spam += 10
        print("Domain From " + domain_from + " and domain Message-Id " + domain_message_id + " doesn't match\n")

    if counter_apparently_to >= 2:
        spam += 10
        print("Too much Apparently-To fields in message\n")

    for x in in_reply_to:
        if x not in references:
            spam += 30
            print("There is no email " + x + " in references\n")
            break

    print("The spam rating of email: " + str(spam) + "\n")

    if spam < 30:
        print("This message " + file + " isn't spam")
    else:
        print("This message " + file + " is spam")

if __name__ == '__main__':
    print("Enter the file:")
    file = input()

    isSpam(file)

