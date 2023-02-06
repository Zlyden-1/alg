import re

with open('resources/Bartenev_LSA.txt', 'r') as file:
    input_algorithm = file.read()


def is_valid_algorithm(algorithm):
    if not re.fullmatch(r'[XYWUDsf0-9]*', algorithm):
        raise TypeError('Ошибка. Алгоритм содержит некорректные символы.')
    return algorithm


def is_valid_commands(commands):
    # проверка наличия и правильной позиции Ys Yf
    if not(commands.count('Ys') == 1 and commands.count('Yf') == 1):
        raise TypeError('Ошибка. Более одной открывающей Ys или закрывающей Yf команды.')
    if not(commands[0] == 'Ys' and commands[-1] == 'Yf'):
        raise TypeError('Ошибка. Открывающая Ys или закрывающая Yf команда находятся в середине алгоритма.')

    # проверка под каждую U есть D
    for command in commands:
        if re.fullmatch(r'X\d+U\d+', command):
            u_number = command.split('U')[1]
            if commands.count(f'D{u_number}') < 1:
                raise TypeError(f'Ошибка. Нет команды D{u_number}, на которую ссылается {command}.')
            if commands.count(f'D{u_number}') > 1:
                raise TypeError(f'Ошибка. Более одной команды D{u_number}, на которую ссылается {command}.')

        if re.fullmatch(r'WU\d+', command):
            u_number = command.split('U')[1]
            if commands.count(f'D{u_number}') < 1:
                raise TypeError(f'Ошибка. Нет команды D{u_number}, на которую ссылается {command}.')
            if commands.count(f'D{u_number}') > 1:
                raise TypeError(f'Ошибка. Более одной команды D{u_number}, на которую ссылается {command}.')

    return commands


def input_binary_code():
    binary_code = input('Введите бинарный код, либо оставьте поле пустым: ')
    if not re.fullmatch(r'[0-1]+|', binary_code):
        while not re.fullmatch(r'[0-1]+|', binary_code):
            binary_code = input(
                f'Ошибка. Бинарный код может состоять только из 0 и 1, либо быть пустым.\nВведите бинарный код, либо оставьте поле пустым: ')
    return binary_code


def parse_algorithm(algorithm):
    commands = []

    pattern = r'Ys|Yf|Y\d+|X\d+U\d+|WU\d+|D\d+'
    word = ''
    for symbol in algorithm:
        # TODO возможно нужна проверка на WU(если после W цифры)
        # TODO проверить на вторую входящую U(вроде сделал уже и работает)
        if re.fullmatch(r'[0-9]', symbol) or (re.fullmatch(r'U', symbol) and ('U' not in word)):
            word += symbol
        else:
            if re.fullmatch(pattern, word):
                commands.append(word)
                word = ''
            word += symbol

    if re.fullmatch(pattern, word):
        commands.append(word)
        word = ''

    if word:
        raise TypeError(f'Ошибка. Неверная команда, с вхождением на индексе:{len(algorithm)-len(word)+1}')
    return commands


def read_commands(commands, binary_code):
    i = 0
    binary_count = 0
    while commands[i] != 'Yf':
        if commands[i] == 'Ys':
            ys()
            i += 1
        elif re.fullmatch(r'Y\d+', commands[i]):
            y(commands[i])
            i += 1
        elif re.fullmatch(r'D\d+', commands[i]):
            d(commands[i])
            i += 1
        elif re.fullmatch(r'WU\d+', commands[i]):
            i = wu(commands, i)
        elif re.fullmatch(r'X\d+U\d+', commands[i]):
            if binary_code:
                try:
                    i = xu(commands, i, binary_code[binary_count])
                    binary_count += 1
                except IndexError:
                    print('Ошибка бинарного кода, программа не завершена.')
                    return
            else:
                i = xu(commands, i, '')
    yf()


def xu(commands, current_index, input_value):
    u_number = commands[current_index].split('U')[1]
    x_number = commands[current_index].split('U')[0].strip('X')
    if input_value:
        print(f'Пройдено X{x_number} = {input_value}')
        value = int(input_value)
    else:
        value = input(f'Введите значение X{x_number}: ')
        if not re.fullmatch(r'0|1', value):
            while not re.fullmatch(r'0|1', value):
                value = input(f'Ошибка. X может принимать значения 0 или 1.\nВведите значение X{x_number}: ')
    if int(value):
        return current_index + 1
    else:
        return commands.index(f'D{u_number}')


def wu(commands, current_index):
    u_number = commands[current_index].strip('WU')
    print(f'Пройдено WU{u_number}')
    return commands.index(f'D{u_number}')


def d(command):
    print(f'Пройдено D{command.strip("D")}')


def ys():
    print('Начало работы программы')


def yf():
    print('Программа успешно завершена')


def y(command):
    print(f'Пройдено Y{command.strip("Y")}')


if __name__ == '__main__':
    try:
        read_commands(is_valid_commands(parse_algorithm(is_valid_algorithm(input_algorithm))), input_binary_code())
    except TypeError as e:
        print(e)
        exit()


