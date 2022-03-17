from functions import text_preparation, number_word, average_median, top_grams, input_constants


def main():
    k, n = input_constants()
    text = text_preparation()
    number_of_words = number_word(text)

    for i in number_of_words:
        print(f"Number of {i} {str(number_of_words[i])}")
    median = average_median(text)[0]
    average = average_median(text)[1]
    print(f"Average number of words in a sentence {median}")
    print(f"Median number of words in a sentence {average}")

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
