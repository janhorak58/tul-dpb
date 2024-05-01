# task_cv03.py


"""
script pro cv03 DPB kurz
"""

import re

def factorize(number):
    """
    Rozkládá vstupní číslo na prvočísla a vrací vzestupně setříděný seznam.
    """
    factors = []
    divisor = 2

    while divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            number = number // divisor
        else:
            divisor += 1

    return factors


def queen(n, m, x, y):
    """
    Vykresluje hrací plochu nxm, umisťuje dámu na zadané souřadnice
    a označuje pole ohrožovaná dámou znakem '*'.
    """
    board = [[" " for _ in range(m)] for _ in range(n)]

    # Ohrožovaná pole označena '*' ostatní '.'
    for i in range(n):
        for j in range(m):
            if i == x or j == y or abs(i - x) == abs(j - y):
                board[i][j] = "*"
            else:
                board[i][j] = "."

    # Umístění dámy na zadané souřadnice
    board[x][y] = "D"

    # Výpis hrací plochy
    for row in board:
        print(" ".join(row))


def censor_number(max_num, censored_num):
    """
    Vypisuje posloupnost od 1 do max_num, kde čísla obsahující censored_num jsou nahrazena '*'.
    """
    for i in range(1, max_num + 1):
        if str(censored_num) in str(i):
            print("*")
        else:
            print(i)


def text_analysis(file_path):
    """
    Analýza textu: počet výskytů jednotlivých písmen a slov v textovém souboru.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().lower()

    # Analýza písmen
    letters_count = {}
    for char in text:
        if char.isalpha():
            letters_count[char] = letters_count.get(char, 0) + 1

    # Analýza slov
    words_count = {}
    words = re.findall(r"\b\w+\b", text)
    for word in words:
        words_count[word] = words_count.get(word, 0) + 1

    return letters_count, words_count


def get_words(N, M, analysis_results):
    """
    Vrací N slov o minimální délce M s nejvyšším výskytem včetně počtu.
    """
    words_sorted_by_count = sorted(
        analysis_results[1].items(), key=lambda x: x[1], reverse=True
    )

    filtered_words = [
        (word, count) for word, count in words_sorted_by_count if len(word) >= M
    ][:N]

    return filtered_words


def cypher(input_file_path, output_file_path, key):
    """
    Šifruje textový soubor pomoci Vigenère šifry a výsledek ukládá do jiného souboru.
    """
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        text = input_file.read().lower()

    encrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord("a")
            encrypted_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            encrypted_text += encrypted_char
            key_index += 1
        else:
            encrypted_text += char

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(encrypted_text)


def decypher(input_file_path, output_file_path, key):
    """
    Dešifruje textový soubor zašifrovaný Vigenère šifrou a výsledek ukládá do jiného souboru.
    """
    with open(input_file_path, "r", encoding="utf-8") as input_file:
        encrypted_text = input_file.read().lower()

    decrypted_text = ""
    key_index = 0
    for char in encrypted_text:
        if char.isalpha():
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord("a")
            decrypted_char = chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            decrypted_text += decrypted_char
            key_index += 1
        else:
            decrypted_text += char
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(decrypted_text)


# Příklady použití funkcí:
if __name__ == "__main__":
    # Testování factorize
    print("Faktorizace 90:", factorize(12))

    # Testování queen
    # print("\nDáma:")
    # queen(8, 10, 4, 3)

    # Testování censor_number
    # print("\nCensoring numbers:")
    # censor_number(13, 2)

    # Testování text_analysis
    # analysis_results = text_analysis('book.txt')
    # print("\nAnalyza ulozena v souboru analyza.txt")
    # with open("analyza.txt", "w") as file:
    #     file.write("Pismena: " + str(analysis_results[0]) + "\nSlova: " + str(analysis_results[1]))

    # # Testování get_words
    # N = 5
    # M = 4
    # top_words = get_words(N, M, analysis_results)
    # print("\n", N, "slov s nejvetsi cetnosti a s minimalni delkou", M, ":")
    # for word, count in top_words:
    #     print(f"{word}: {count}")

    # Testování cypher
    # key = "VEIUSVNI"
    # cypher("cifra_in.txt", "cifra_out.txt", key)
    # decypher("cifra_out.txt", "desifra_out.txt", key)

    pass
