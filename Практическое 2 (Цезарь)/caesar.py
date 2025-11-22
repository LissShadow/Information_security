import colorama
from colorama import Fore, Style
colorama.init()
# Основной латинский алфавит 
LATIN_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

def caesar_encrypt(text, key):
    result = ''
    for char in text.lower():
        if char in LATIN_ALPHABET:
            idx = LATIN_ALPHABET.index(char)
            result += LATIN_ALPHABET[(idx + key) % len(LATIN_ALPHABET)]
        else:
            result += char
    return result

def caesar_decrypt(text, key):
    return caesar_encrypt(text, -key)

def known_plaintext_attack(plaintext, ciphertext):
    for p, c in zip(plaintext.lower(), ciphertext.lower()):
        if p in LATIN_ALPHABET and c in LATIN_ALPHABET:
            key = (LATIN_ALPHABET.index(c) - LATIN_ALPHABET.index(p)) % len(LATIN_ALPHABET)
            return key
    return None

def ciphertext_only_attack(ciphertext):
    return [(key, caesar_decrypt(ciphertext, key)) for key in range(len(LATIN_ALPHABET))]

def dictionary_attack(ciphertext, dictionary):
    for key in range(len(LATIN_ALPHABET)):
        decrypted = caesar_decrypt(ciphertext, key)
        words = decrypted.split()
        matches = sum(1 for word in words if word in dictionary)
        if matches > 0:
            return key, decrypted
    return None, None

def main():
    # Пример простого словаря распространённых английских слов
    choice = ""
    while(choice != "0"):
        dictionary = {"it", "he", "she", "me", "cat", "dog", "when", "apple", "bird", "stop", "love", "sun", "cloud", "mind", "soul", "thry", "be", "in", "on", "from", "at", "light", "where"}
        print("1. Зашифровать текст")
        print("2. Расшифровать текст")
        print("3. Атака по открытому тексту (определение ключа)")
        print("4. Атака по шифрованному тексту (вывод всех вариантов)")
        print("5. Атака с помощью словаря")
        print("0. Закрыть программу")
        choice = input("Введите номер желаемого действия: ")

        if choice == "1":
            text = input("Введите текст: ")
            key = int(input(f"Введите ключ (0-{len(LATIN_ALPHABET)-1}): "))
            print(Fore.GREEN +"Зашифрованный текст:", caesar_encrypt(text, key) + Style.RESET_ALL)

        elif choice == "2":
            text = input("Введите зашифрованный текст: ")
            key = int(input(f"Введите ключ (0-{len(LATIN_ALPHABET)-1}): "))
            print(Fore.GREEN +"Расшифрованный текст:", caesar_decrypt(text, key)+ Style.RESET_ALL)

        elif choice == "3":
            plaintext = input("Введите открытый текст: ")
            ciphertext = input("Введите зашифрованный текст: ")
            key = known_plaintext_attack(plaintext, ciphertext)
            if key is not None:
                print(Fore.GREEN + f"Обнаруженный ключ: {key}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Ключ не найден." + Style.RESET_ALL)

        elif choice == "4":
            ciphertext = input("Введите зашифрованный текст: ")
            for key, variant in ciphertext_only_attack(ciphertext):
                print(Fore.GREEN + f"Ключ {key}: {variant}" + Style.RESET_ALL)

        elif choice == "5":
            ciphertext = input("Введите зашифрованный текст: ")
            key, variant = dictionary_attack(ciphertext, dictionary)
            if key is not None:
                print(Fore.GREEN + f"Обнаруженный ключ: {key}, расшифровка: {variant}" + Style.RESET_ALL)
            else:
                print(Fore.RED + "Подходящий ключ не найден." + Style.RESET_ALL)  
if __name__ == "__main__":
    main()
