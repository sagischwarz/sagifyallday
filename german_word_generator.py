import random
import argparse
import datetime


def can_form_word(word, characters, first_char):
    if first_char not in word:
        return False

    if len(word) < 4:
        return False

    for char in word:
        if char not in characters:
            return False

    return True


def uses_all_characters(word, characters):
    return all(char in word for char in characters)


def get_german_words(file_path="german_words.txt"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [
                word.strip().lower()
                for word in file
                if word.strip() and all(c.isalpha() for c in word.strip())
            ]
    except FileNotFoundError:
        print(f"Error: Word list file '{file_path}' not found.")
        print("Please create a text file with German words (one word per line).")
        return []


def find_character_set(
    word_file="german_words.txt", max_attempts=10000, needs_all_chars=True
):
    german_words = get_german_words(word_file)

    attempts = 0

    while attempts < max_attempts:
        attempts += 1

        german_chars = "abcdefghijklmnopqrstuvwxyzäöüß"

        char_set = random.sample(german_chars, 7)

        valid_words = []
        has_word_with_all_chars = not needs_all_chars

        for word in german_words:
            if can_form_word(word, char_set, char_set[0]):
                valid_words.append(word)
                if uses_all_characters(word, char_set):
                    has_word_with_all_chars = True

                if len(valid_words) >= 15 and has_word_with_all_chars:
                    return char_set, valid_words

    return None, []


def main():
    parser = argparse.ArgumentParser(
        description="Generate sets of 7 characters that can form German words"
    )
    parser.add_argument(
        "--words",
        "-w",
        type=str,
        default="woerter_de.txt",
        help="Path to the text file containing German words (default: german_words.txt)",
    )
    parser.add_argument(
        "--count",
        "-c",
        type=int,
        default=1,
        help="Number of character sets to generate (default: 1)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show verbose output including found words",
    )
    parser.add_argument(
        "--yearly",
        "-y",
        action="store_true",
        help="Generate one character set for each day of the current year",
    )
    parser.add_argument(
        "--month",
        "-m",
        type=int,
        choices=range(1, 13),
        help="Generate character sets for a specific month (1-12). Works only with --yearly",
    )
    args = parser.parse_args()

    german_words = get_german_words(args.words)
    if not german_words:
        return

    if args.yearly:
        current_year = datetime.datetime.now().year

        if args.month:
            start_date = datetime.date(current_year, args.month, 1)
            if args.month == 12:
                next_month_year = current_year + 1
                next_month = 1
            else:
                next_month_year = current_year
                next_month = args.month + 1
            end_date = datetime.date(
                next_month_year, next_month, 1
            ) - datetime.timedelta(days=1)
        else:
            start_date = datetime.date(current_year, 1, 1)
            end_date = datetime.date(current_year, 12, 31)

        current_date = start_date

        while current_date <= end_date:
            random.seed(f"{current_date.isoformat()}-seed")

            char_set, valid_words = find_character_set(word_file=args.words)

            if char_set:
                print(f"{current_date.isoformat()}:{''.join(char_set).upper()}")

                if args.verbose:
                    print(f"  First character (required): {char_set[0]}")
                    print(f"  Other characters (optional): {''.join(char_set[1:])}")
                    all_char_words = [
                        word
                        for word in valid_words
                        if uses_all_characters(word, char_set)
                    ]
                    print(
                        f"  Found {len(valid_words)} German words (minimum 4 characters), {len(all_char_words)} using all 7 letters"
                    )
            else:
                print(f"Could not find character set for {current_date.isoformat()}")

            current_date += datetime.timedelta(days=1)

            random.seed()
    else:
        for i in range(args.count):
            char_set, valid_words = find_character_set(word_file=args.words)

            if char_set:
                print("".join(char_set).upper())

                if args.verbose:
                    print(f"  First character (required): {char_set[0]}")
                    print(f"  Other characters (optional): {''.join(char_set[1:])}")
                    print(
                        f"  Found {len(valid_words)} German words (minimum 4 characters):"
                    )
                    for j, word in enumerate(valid_words, 1):
                        uses_all = "✓" if uses_all_characters(word, char_set) else " "
                        print(f"  {j}. {word} {uses_all}")
            else:
                print(f"Could not find character set #{i + 1}")
                break


if __name__ == "__main__":
    main()
