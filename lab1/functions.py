from variables import N, K, PUNCTUATION_MARKS, END_MARKS, MR_CONST, MRS_CONST


def input_constants():
    choice = '42'

    while choice != 'Y' and choice != 'N':
        choice = input("Do you want to enter N and K, enter 'Y/N'\n")

    if choice == 'Y':
        k = int(input('Enter K:\n'))
        n = int(input('Enter N:\n'))
    else:
        k = K
        n = N

    return k, n


def input_text():
    text = input("Enter text\n")

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
        if text[i:i + 3] == MR_CONST:
            text = text[0:i + 2] + ' ' + text[i + 3:]

    for i in range(len(text) - 5):
        if text[i:i + 4] == MRS_CONST:
            text = text[0:i + 3] + ' ' + text[i + 4:]

    return text


def get_number_word_sentence(text):
    list_point = []

    for i in range(len(text)):
        if text[i] == '.':
            list_point.append(i)

    number_of_word_in_sentences = []

    for i in range(len(list_point) - 1):
        number_of_word_in_sentences.append(text.count(' ', list_point[i], list_point[i + 1]) - 1)

    return number_of_word_in_sentences


def get_median(text):
    number_of_word_in_sentences = get_number_word_sentence(text)

    median = sorted(number_of_word_in_sentences)[len(number_of_word_in_sentences) // 2]

    return median


def get_average(text):
    number_of_word_in_sentences = get_number_word_sentence(text)

    average = sum(number_of_word_in_sentences) / len(number_of_word_in_sentences)

    return average


def number_word(text):
    for i in ['.']:
        text = text.replace(i, '')

    words = text.split()
    word_dict = {}

    for i in range(len(words)):
        word_dict[words[i]] = words.count(words[i])

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
