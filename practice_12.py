from math import gcd


ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def surname_numbers(surname):
    surname = surname.strip().upper()
    if not surname:
        raise ValueError("Фамилия не должна быть пустой.")

    numbers = []
    for letter in surname:
        if letter == "-" or letter == " ":
            continue
        if letter not in ALPHABET:
            raise ValueError("Введите фамилию русскими буквами.")
        numbers.append(ALPHABET.index(letter) + 1)

    if not numbers:
        raise ValueError("В фамилии должны быть буквы.")
    return numbers


def message_hash(numbers, prime):
    hash_value = 0
    steps = []
    for number in numbers:
        hash_value = (hash_value + number) ** 2 % prime
        steps.append(hash_value)
    return hash_value, steps


def sign_elgamal(hash_value, prime, generator, private_key, nonce):
    if not 1 <= private_key <= prime - 2:
        raise ValueError("Недопустимый секретный ключ.")
    if not 1 < nonce < prime - 1 or gcd(nonce, prime - 1) != 1:
        raise ValueError("Число k должно быть взаимно простым с p - 1.")
    first = pow(generator, nonce, prime)
    inverse_nonce = pow(nonce, -1, prime - 1)
    second = (hash_value - private_key * first) * inverse_nonce % (prime - 1)
    if second == 0:
        raise ValueError("Нулевая часть подписи: выберите другое k.")
    return first, second


def verify_elgamal(hash_value, first, second, prime, generator, public_key):
    if not 0 < first < prime or not 0 <= second < prime - 1:
        return False, None, None
    left = pow(generator, hash_value, prime)
    right = pow(public_key, first, prime) * pow(first, second, prime) % prime
    return left == right, left, right


def sign_gost(hash_value, prime, order, generator, private_key, nonce):
    if not 0 < private_key < order or not 0 < nonce < order:
        raise ValueError("Секретный ключ и k должны быть от 1 до q - 1.")
    reduced_hash = hash_value % order
    if reduced_hash == 0:
        reduced_hash = 1
    first = pow(generator, nonce, prime) % order
    second = (private_key * first + nonce * reduced_hash) % order
    if first == 0 or second == 0:
        raise ValueError("Нулевая часть подписи: выберите другое k.")
    return first, second


def verify_gost(
    hash_value, first, second, prime, order, generator, public_key
):
    if not 0 < first < order or not 0 < second < order:
        return False, None, None, None, None
    reduced_hash = hash_value % order
    if reduced_hash == 0:
        reduced_hash = 1
    inverse_hash = pow(reduced_hash, -1, order)
    first_power = second * inverse_hash % order
    second_power = -first * inverse_hash % order
    result = pow(generator, first_power, prime)
    result = result * pow(public_key, second_power, prime) % prime % order
    return result == first, inverse_hash, first_power, second_power, result


def main():
    print("Практика 12. Электронные подписи")
    while True:
        surname = input("Введите фамилию русскими буквами: ")
        try:
            numbers = surname_numbers(surname)
            break
        except ValueError as error:
            print(error)

    print("Коды букв (А = 1, Ё = 7, Я = 33):", numbers)
    print("Начальное значение хеша H0 = 0.")

    print("\nЗадание 1. Подпись Эль-Гамаля")
    prime = 47
    generator = 5
    private_key = 9
    public_key = pow(generator, private_key, prime)
    hash_value, steps = message_hash(numbers, prime)
    for nonce in range(7, prime - 1):
        try:
            first, second = sign_elgamal(
                hash_value, prime, generator, private_key, nonce
            )
            break
        except ValueError:
            continue
    valid, left, right = verify_elgamal(
        hash_value, first, second, prime, generator, public_key
    )
    print("p =", prime, "g =", generator, "x =", private_key, "k =", nonce)
    print("Открытый ключ Y =", public_key)
    print("Значения хеша после каждой буквы:", steps)
    print("h(M) =", hash_value, "Подпись (r, s) =", (first, second))
    print("g^h mod p =", left, "Y^r * r^s mod p =", right)
    print("Подпись верна:", valid)

    print("\nЗадание 2. Проверка заданных подписей Эль-Гамаля")
    messages = [
        (22, 15, 20, 3), (22, 15, 10, 5), (22, 15, 19, 3),
        (9, 5, 19, 17), (9, 7, 17, 8), (9, 6, 17, 8),
    ]
    for public_key, hash_value, first, second in messages:
        valid, left, right = verify_elgamal(
            hash_value, first, second, 23, 5, public_key
        )
        print("Y =", public_key, "(M, r, s) =", (hash_value, first, second))
        print("g^M mod p =", left, "Y^r * r^s mod p =", right, "Верна:", valid)

    print("\nЗадание 3. Подпись ГОСТ Р 34.10-94")
    prime = 67
    order = 11
    generator = 25
    private_key = 5
    public_key = pow(generator, private_key, prime)
    hash_value, steps = message_hash(numbers, prime)
    for nonce in range(1, order):
        try:
            first, second = sign_gost(
                hash_value, prime, order, generator, private_key, nonce
            )
            break
        except ValueError:
            continue
    valid, inverse_hash, first_power, second_power, result = verify_gost(
        hash_value, first, second, prime, order, generator, public_key
    )
    print("p =", prime, "q =", order, "a =", generator)
    print("x =", private_key, "Y =", public_key, "k =", nonce)
    print("Значения хеша после каждой буквы:", steps)
    print("h(M) =", hash_value, "Подпись (r, s) =", (first, second))
    print("v =", inverse_hash, "z1 =", first_power, "z2 =", second_power)
    print("u =", result, "r =", first, "Подпись верна:", valid)

    print("\nЗадание 4. Проверка заданных подписей ГОСТ Р 34.10-94")
    messages = [
        (22, 6, 9, 5), (22, 8, 8, 3), (22, 7, 4, 1),
        (64, 10, 7, 3), (64, 7, 7, 10), (64, 8, 7, 5),
    ]
    for public_key, hash_value, first, second in messages:
        valid, inverse_hash, first_power, second_power, result = verify_gost(
            hash_value, first, second, 67, 11, 25, public_key
        )
        print("Y =", public_key, "(M, r, s) =", (hash_value, first, second))
        print("v =", inverse_hash, "z1 =", first_power, "z2 =", second_power)
        print("u =", result, "r =", first, "Верна:", valid)


if __name__ == "__main__":
    main()
