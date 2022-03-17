from variables import N, K, PUNCTUATION_MARKS, END_MARKS


def input_constants():
    t = 42

    while t != 'Y' and t != 'N':
        print("Do you want to enter N and K, enter 'Y/N'")
        t = input()

    if t == 'Y':
        print('Enter K: ')
        k = int(input())
        print('Enter N: ')
        n = int(input())
    else:
        k = K
        n = N

    return k, n


def input_text():
    print("Enter text")
    text = input()

    return text


def punctuation_marks(text):
    for i in PUNCTUATION_MARKS:
        text = text.replace(i, '')

    for i in END_MARKS:
        text = text.replace(i, '.')

    return text


def abbreviation(text):
    for i in range(len(text) - 2):
        if text[i] == '.' and not text[i + 2].isupper():
            text = text[0:i] + ' ' + text[i + 1:]

    for i in range(len(text) - 4):
        if text[i:i + 3] == ('mr.' or 'Mr.'):
            text = text[0:i + 2] + ' ' + text[i + 3:]

    for i in range(len(text) - 5):
        if text[i:i + 4] == ('mrs.' or 'Mrs.'):
            text = text[0:i + 3] + ' ' + text[i + 4:]

    return text


def average_median(text):
    list_point = []

    for i in range(len(text)):
        if text[i] == '.':
            list_point.append(i)

    list_word_sentence = []

    for i in range(len(list_point) - 1):
        list_word_sentence.append(text.count(' ', list_point[i], list_point[i + 1]) - 1)

    average = sum(list_word_sentence) / len(list_word_sentence)
    median = sorted(list_word_sentence)[len(list_word_sentence) // 2]

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
    text = abbreviation(punctuation_marks(input_text())).lower()
    text = text.replace('.', ' . ')
    text = ' '.join(text.split())
    text = '. ' + text + ' '

    return text


def top_grams(text, n):
    text = text.replace('.', ' ')
    list_word = text.split(' ')
    grams = {}

    for elem in list_word:
        if len(elem) >= n:
            for i in range(len(elem) - n + 1):
                if elem[i:i + n] in grams:
                    grams[elem[i:i + n]] += 1
                else:
                    grams[elem[i:i + n]] = 1

    list_grams = sorted(grams, key=grams.get, reverse=True)
    number = []

    for i in range(len(list_grams)):
        number.append(grams[list_grams[i]])

    return list_grams, number
