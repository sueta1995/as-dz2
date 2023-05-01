import re

identifier_pattern = r'^[a-zA-Z_][a-zA-Z0-9_-]*$'
number_pattern = r'[-+]?\d+$'
splitters = {' ', '=', ';', ':', '(', ')', '{', '}'}
error_status = False


def get_tokens(string):
    string += ''
    buf = ''
    result = []
    array = ['switch', 'case', 'break']

    for i in range(len(string)):
        check = False

        if string[i] not in splitters:
            buf += string[i]
        else:
            if i == len(string) - 1:
                check = True

            j = 0

            while j < 3 and buf != array[j]:
                j += 1

            if j != 3:
                print(f"Служебное слово: {buf}")

                if buf[0] == 's':
                    result += ['sw']
                elif buf[0] == 'c':
                    result += ['ca']
                elif buf[0] == 'b':
                    result += ['br', ';_']
            else:
                if re.match(identifier_pattern, buf):
                    print(f"Идентификатор: {buf}")
                    result += ['V_']
                elif re.match(number_pattern, buf):
                    print(f"Целое число: {buf}")
                    result += ['V_']
                else:
                    if buf != '':
                        print(f"Неверный формат идентификатора: {buf}")

                if string[i] != ' ':
                    print(f"Служебное слово: {string[i]}")
                    result += [string[i] + '_']

            buf = ''

    return result


def operator_switch():
    global tokens

    if ''.join(tokens[0:5]) == 'sw(_V_)_{_':
        tokens = tokens[5:]
        r = cons_case()

        if r and tokens[0] == '}_':
            tokens = tokens[1:]
        elif not r:
            print_error('Неправильная конструкция case')
        else:
            r = False

            print_error('Неправильная конструкция switch')
    else:
        r = False

        print_error('Неправильная конструкция switch')

    return r


def cons_case():
    global tokens

    if ''.join(tokens[0:3]) == 'caV_:_':
        tokens = tokens[3:]
        r = cons_case()
    else:
        r = operator()

        if r and ''.join(tokens[0:3]) == ';_br;_':
            tokens = tokens[3:]

            if tokens[0] == 'ca':
                r = cons_case()

        elif r and tokens[0] == ';_':
            tokens = tokens[1:]

            if tokens[0] == 'ca':
                r = cons_case()
        elif not r:
            print_error("Неправильный оператор")
        else:
            r = False

    return r


def operator():
    global tokens

    if tokens[0] == 'V_':
        r = assignment()
    elif tokens[0] == 'sw':
        r = operator_switch()
    else:
        r = False

    return r


def assignment():
    global tokens

    if ''.join(tokens[0:3]) == 'V_=_V_':
        tokens = tokens[3:]

        return True
    else:
        print_error("Неправильное присваивание")

        return False


def print_error(error):
    global error_status

    if not error_status:
        print(f"{error}: {' '.join(tokens)}")
        error_status = True


tokens = get_tokens(input())
print(f"Результат сканирования: {' '.join(tokens)}")

answer = operator_switch()
print(f"Вердикт: {answer}")
