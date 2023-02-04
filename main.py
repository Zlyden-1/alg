import re

with open('resources/LSA.txt', 'r') as file:
    algorithm = file.read()


def is_valid(algorithm):
    if not re.fullmatch(r'[XYWUDsf0-9]*', algorithm):
        return False
    return True


def parse_algorithm(algorithm):
    commands = []
    pattern = re.Pattern(r'Yf|Ys|Y[0-9]*|X[0-9]*U[0-9]*|WU[0-9]*|D[0-9]*')
    word = ''
    for symbol in algorithm:
        # TODO проверить на вторую входящую U
        if re.fullmatch(r'[0-9]', symbol) or (re.fullmatch(r'U', symbol) and ('U' not in word)):
            word += symbol
        else:
            if re.fullmatch(pattern, word):
                commands.append(word)
                word = ''
            word += symbol
    if word:
        raise TypeError(word)


def ys():
    print('Начало работы программы')


def yf():
    print('Программа успешно завершена')


def y(n):
    print(f'Пройдено y{n}')

# def xu(n):

# if __name__ == '__main__':
#     patterns = r'Yf|Ys|Y[0-9]*|X[0-9]*U[0-9]*|WU[0-9]*|D[0-9]*'
#     print(re.fullmatch(patterns, 'Yf'))
