from functions import text_preparation, number_word, get_average, get_median, top_grams, input_constants


def main():
    k, n = input_constants()
    text = text_preparation()
    number_of_words = number_word(text)

    for i in number_of_words:
        print(f"Number of {i} {str(number_of_words[i])}")

    print(f"Average number of words in a sentence {get_average(text)}")
    print(f"Median number of words in a sentence {get_median(text)}")

    top_of_grams = top_grams(text, n)
    if len(top_of_grams[0]) >= k:
        print(f"Top {k}")

        for i in range(k):
            print(f"{top_of_grams[0][i]} {top_of_grams[1][i]}")
    else:
        print(f"Top {len(top_of_grams[0])}")

        for i in range(len(top_of_grams[0])):
            print(f"{top_of_grams[0][i]} {top_of_grams[1][i]}")


if __name__ == '__main__':
    main()
