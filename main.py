from fun import *


def main():
    text = text_preparation()
    number_of_words = number_word(text)

    for i in number_of_words:
        print("Number of " + i + " " + str(number_of_words[i]))

    print("Average number of words in a sentence " + str(average_median(text)[0]))
    print("Median number of words in a sentence " + str(average_median(text)[1]))

    top_of_gramms = top_gramms(text)
    if len(top_of_gramms[0]) >= constants.k:
        print('Top ', constants.k)
        for i in range(constants.k):
            print("{} {}".format(top_of_gramms[0][i], top_of_gramms[1][i]))
    else:
        print('Top ', len(top_of_gramms[0]))
        for i in range(len(top_of_gramms)):
            print("{} {}".format(top_of_gramms[0][i], top_of_gramms[1][i]))


if __name__ == '__main__':
    main()
