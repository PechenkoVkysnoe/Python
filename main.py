import constants
from constants import *


def main():
    t = 42
    while t != 'Y' and t != 'N':
        print("Do you want to enter N and K, enter 'Y/N'")
        t = input()
    if t == 'Y':
        print('Enter K: ')
        constants.k = int(input())
        print('Enter N: ')
        constants.n = int(input())
    s = input()
    for i in [';', ':', ',', '"', "'", '_', '@', '(', ')', '*', '&', '–']:
        s = s.replace(i, '')
    for i in ['!', '?', '...', '?!', '!?']:
        s = s.replace(i, '.')

    for i in range(len(s) - 2):
        if s[i] == '.' and not s[i + 2].isupper():
            s = s[0:i] + ' ' + s[i + 1:]
    for i in range(len(s) - 4):
        if (s[i] == 'm' or s[i] == 'M') and s[i + 1] == 'r' and s[i + 2] == '.':
            s = s[0:i + 2] + ' ' + s[i + 3:]
    for i in range(len(s) - 5):
        if (s[i] == 'm' or s[i] == 'M') and s[i + 1] == 'r' and s[i + 2] == 's' and s[i + 3] == '.':
            s = s[0:i + 3] + ' ' + s[i + 4:]

    s = s.lower()
    s = s.replace('.', ' . ')
    s = ' '.join(s.split())
    s = '. ' + s + ' '

    list_point = []
    list_space = []

    for i in range(len(s)):
        if s[i] == '.':
            list_point.append(i)
    list_word_sentense = []
    for i in range(len(list_point) - 1):
        list_word_sentense.append(s.count(' ', list_point[i], list_point[i + 1]) - 1)
    print("Average number of words in a sentence " + str(sum(list_word_sentense) / len(list_word_sentense)))
    print("Median number of words in a sentence " + str(sorted(list_word_sentense)[len(list_word_sentense) // 2]))

    for i in ['.']:
        s = s.replace(i, '')
    s = ' '.join(s.split())
    s = ' ' + s + ' '
    word_dict = {}
    for i in range(len(s)):
        if s[i] == ' ':
            list_space.append(i)
    for i in range(len(list_space) - 1):
        if s[list_space[i] + 1:list_space[i + 1]] in word_dict:
            word_dict[s[list_space[i] + 1:list_space[i + 1]]] += 1
        else:
            word_dict[s[list_space[i] + 1:list_space[i + 1]]] = 1
    for i in word_dict:
        print("Number of " + i + " " + str(word_dict[i]))

    list_word = s.split(' ')
    gramms = {}
    for elem in list_word:
        if len(elem) >= constants.n:
            for i in range(len(elem) - constants.n + 1):
                if elem[i:i + constants.n] in gramms:
                    gramms[elem[i:i + constants.n]] += 1
                else:
                    gramms[elem[i:i + constants.n]] = 1
    gramms = sorted(gramms, key=gramms.get, reverse=True)
    if len(gramms) >= constants.k:
        print('Top ', constants.k)
        print(*gramms[:10], sep='\n')
    else:
        print('Top ', len(gramms))
        print(*gramms, sep='\n')


if __name__ == '__main__':
    main()
