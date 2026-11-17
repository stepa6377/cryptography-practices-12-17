from math import gcd
from random import SystemRandom

from practice_12 import ALPHABET, surname_numbers


def make_public_key(secret_key, modulus, multiplier):
    previous_sum = 0
    for weight in secret_key:
        if weight <= previous_sum:
            raise ValueError("Нужна сверхвозрастающая последовательность.")
        previous_sum += weight
    if modulus <= previous_sum:
        raise ValueError("Модуль должен быть больше суммы секретных весов.")
    if gcd(multiplier, modulus) != 1:
        raise ValueError("Множитель должен быть взаимно простым с модулем.")
    public_key = []
    for weight in secret_key:
        public_key.append(weight * multiplier % modulus)
    return public_key


def encrypt_numbers(numbers, public_key):
    encrypted = []
    for number in numbers:
        if not 0 <= number < 2 ** len(public_key):
            raise ValueError("Код буквы не помещается в блок.")
        bits = format(number, f"0{len(public_key)}b")
        total = 0
        for index in range(len(public_key)):
            total += int(bits[index]) * public_key[index]
        encrypted.append(total)
    return encrypted


def decrypt_numbers(encrypted, secret_key, modulus, multiplier):
    inverse_multiplier = pow(multiplier, -1, modulus)
    numbers = []
    transformed = []
    for total in encrypted:
        remainder = total * inverse_multiplier % modulus
        transformed.append(remainder)
        bits = [0] * len(secret_key)
        for index in range(len(secret_key) - 1, -1, -1):
            if secret_key[index] <= remainder:
                bits[index] = 1
                remainder -= secret_key[index]
        if remainder != 0:
            raise ValueError("Шифротекст не соответствует секретному рюкзаку.")
        number = 0
        for bit in bits:
            number = number * 2 + bit
        numbers.append(number)
    return numbers, transformed


def deal_keys(initial_keys, prime, encryption_keys, random_source):
    if len(initial_keys) != 3 or len(set(initial_keys)) != 3:
        raise ValueError("Нужны три разных ключа для раздачи.")
    if len(encryption_keys) != 3:
        raise ValueError("Нужны три участника.")
    for key in initial_keys:
        if not 1 < key < prime:
            raise ValueError("Раздаваемые ключи должны быть от 2 до p - 1.")
    decryption_keys = []
    for encryption_key in encryption_keys:
        if gcd(encryption_key, prime - 1) != 1:
            raise ValueError("Показатель должен быть взаимно прост с p - 1.")
        decryption_keys.append(pow(encryption_key, -1, prime - 1))

    participants = ["А", "Б", "В"]
    deck = initial_keys.copy()
    print("Общая исходная колода ключей:", deck)
    for participant_index in range(3):
        encrypted_deck = []
        for key in deck:
            encrypted_key = pow(key, encryption_keys[participant_index], prime)
            encrypted_deck.append(encrypted_key)
        random_source.shuffle(encrypted_deck)
        deck = encrypted_deck
        print("Шифрование и перемешивание:", participants[participant_index])
        print("Колода:", deck)

    received_keys = []
    for recipient_index in range(3):
        key = deck[recipient_index]
        recipient = participants[recipient_index]
        print("\nВыбранный зашифрованный ключ для", recipient, "=", key)
        for participant_index in range(3):
            if participant_index != recipient_index:
                key = pow(key, decryption_keys[participant_index], prime)
                participant = participants[participant_index]
                print("Участник", participant, "снимает свой слой:", key)
        print("Передача участнику", recipient, "числа", key)
        key = pow(key, decryption_keys[recipient_index], prime)
        received_keys.append(key)
        print("Получатель снимает последний слой у себя. Его ключ:", key)
    return received_keys


def main():
    print("Практика 16")
    print("\nЗадание 1. Сверхвозрастающий рюкзак")
    while True:
        surname = input("Введите фамилию русскими буквами: ")
        try:
            numbers = surname_numbers(surname)
            break
        except ValueError as error:
            print(error)

    secret_key = [2, 3, 6, 13, 25, 51]
    modulus = 101
    multiplier = 31
    public_key = make_public_key(secret_key, modulus, multiplier)
    encrypted = encrypt_numbers(numbers, public_key)
    restored_numbers, transformed = decrypt_numbers(
        encrypted, secret_key, modulus, multiplier
    )
    restored_surname = ""
    for number in restored_numbers:
        restored_surname += ALPHABET[number - 1]

    print("Секретный ключ:", secret_key, "Сумма:", sum(secret_key))
    print("Модуль:", modulus, "Множитель:", multiplier)
    print("Обратный множитель:", pow(multiplier, -1, modulus))
    print("Открытый ключ:", public_key)
    print("Коды букв (А = 1, Ё = 7, Я = 33):", numbers)
    for index in range(len(numbers)):
        bits = format(numbers[index], "06b")
        print("Код", numbers[index], "Биты", bits, "Шифр", encrypted[index])
    print("Шифротекст:", encrypted)
    print("Суммы после снятия множителя:", transformed)
    print("Расшифрованные коды:", restored_numbers)
    print("Восстановленная фамилия:", restored_surname)
    print("Коды восстановлены:", numbers == restored_numbers)

    print("\nЗадание 2. Ментальный покер для трёх абонентов")
    prime = 101
    initial_keys = [12, 34, 56]
    encryption_keys = [3, 7, 9]
    print("p =", prime)
    print("Показатели шифрования А, Б, В (учебный вывод):", encryption_keys)
    print("Для каждого участника d = c^(-1) mod (p - 1).")
    for index in range(3):
        encryption_key = encryption_keys[index]
        decryption_key = pow(encryption_key, -1, prime - 1)
        print("Участник", index + 1)
        print("c =", encryption_key, "d =", decryption_key)
    received_keys = deal_keys(
        initial_keys, prime, encryption_keys, SystemRandom()
    )
    print("\nИтоговая раздача А, Б, В (учебный вывод):", received_keys)
    valid = sorted(initial_keys) == sorted(received_keys)
    print("Все ключи розданы без повторений:", valid)


if __name__ == "__main__":
    main()
