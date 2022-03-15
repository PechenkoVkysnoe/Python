import constants


def inlet():
    t = 42
    while t != 'Y' and t != 'N':
        print("Do you want to enter N and K, enter 'Y/N'")
        t = input()
    if t == 'Y':
        print('Enter K: ')
        constants.k = int(input())
        print('Enter N: ')
        constants.n = int(input())
    print("Enter text")
    text = input()
    return text


def punctuation_marks(text):
    for i in [';', ':', ',', '"', "'", '_', '@', '(', ')', '*', '&', '–']:
        text = text.replace(i, '')
    for i in ['!', '?', '...', '?!', '!?']:
        text = text.replace(i, '.')
    return text


def abbreviation(text):
    for i in range(len(text) - 2):
        if text[i] == '.' and not text[i + 2].isupper():
            text = text[0:i] + ' ' + text[i + 1:]
    for i in range(len(text) - 4):
        if (text[i] == 'm' or text[i] == 'M') and text[i + 1] == 'r' and text[i + 2] == '.':
            text = text[0:i + 2] + ' ' + text[i + 3:]
    for i in range(len(text) - 5):
        if (text[i] == 'm' or text[i] == 'M') and text[i + 1] == 'r' and text[i + 2] == 's' and text[i + 3] == '.':
            text = text[0:i + 3] + ' ' + text[i + 4:]
    return text


def average_median(text):
    list_point = []
    for i in range(len(text)):
        if text[i] == '.':
            list_point.append(i)
    list_word_sentense = []
    for i in range(len(list_point) - 1):
        list_word_sentense.append(text.count(' ', list_point[i], list_point[i + 1]) - 1)
    average = sum(list_word_sentense) / len(list_word_sentense)
    median = sorted(list_word_sentense)[len(list_word_sentense) // 2]
    return average, median


def number_word(text):
    list_space = []
    for i in ['.']:
        text = text.replace(i, '')
    text = ' '.join(text.split())
    text = ' ' + text + ' '
    word_dict = {}
    for i in range(len(text)):
        if text[i] == ' ':
            list_space.append(i)
    for i in range(len(list_space) - 1):
        if text[list_space[i] + 1:list_space[i + 1]] in word_dict:
            word_dict[text[list_space[i] + 1:list_space[i + 1]]] += 1
        else:
            word_dict[text[list_space[i] + 1:list_space[i + 1]]] = 1
    return word_dict


def text_preparation():
    text = abbreviation(punctuation_marks(inlet()))
    text = text.lower()
    text = text.replace('.', ' . ')
    text = ' '.join(text.split())
    text = '. ' + text + ' '
    return text


def top_gramms(text):
    list_word = text.split(' ')
    gramms = {}
    for elem in list_word:
        if len(elem) >= constants.n:
            for i in range(len(elem) - constants.n + 1):
                if elem[i:i + constants.n] in gramms:
                    gramms[elem[i:i + constants.n]] += 1
                else:
                    gramms[elem[i:i + constants.n]] = 1
    list_gramms = sorted(gramms, key=gramms.get, reverse=True)
    number = []
    for i in range(len(list_gramms)):
        number.append(gramms[list_gramms[i]])
    return list_gramms, number
