from secrets import randbelow


def split_secret(secret, prime):
    if not 0 <= secret < prime:
        raise ValueError("Секрет должен быть от 0 до p - 1.")
    first_coefficient = randbelow(prime)
    second_coefficient = randbelow(prime)
    shares = []
    for user_number in range(1, 4):
        value = secret + first_coefficient * user_number
        value += second_coefficient * user_number ** 2
        shares.append((user_number, value % prime))
    return shares


def restore_secret(shares, prime):
    if len(shares) != 3:
        raise ValueError("Для схемы 3 из 3 нужны доли всех трёх участников.")
    user_numbers = []
    for user_number, value in shares:
        if not 0 < user_number < prime or not 0 <= value < prime:
            raise ValueError("Недопустимая доля секрета.")
        if user_number in user_numbers:
            raise ValueError("Нельзя использовать одну долю дважды.")
        user_numbers.append(user_number)

    secret = 0
    for index in range(len(shares)):
        user_number, value = shares[index]
        numerator = 1
        denominator = 1
        for other_index in range(len(shares)):
            if other_index != index:
                other_number = shares[other_index][0]
                numerator = numerator * (-other_number) % prime
                denominator *= user_number - other_number
                denominator %= prime
        coefficient = numerator * pow(denominator, -1, prime) % prime
        secret = (secret + value * coefficient) % prime
    return secret


def main():
    print("Практика 17. Схема Шамира 3 из 3")
    prime = 257
    secret = 123
    print("Простое число p =", prime, "Секрет S =", secret)
    print("Создаём f(x) = S + a1*x + a2*x^2 mod p.")
    print("Коэффициенты a1 и a2 случайны и не передаются пользователям.")
    shares = split_secret(secret, prime)
    for user_number, value in shares:
        print("Пользователь", user_number, "Доля:", (user_number, value))
    restored_secret = restore_secret(shares, prime)
    print("\nВосстановление интерполяцией Лагранжа при x = 0.")
    print("Для x = 1, 2, 3: S = (3*y1 - 3*y2 + y3) mod p.")
    print("S =", (3 * shares[0][1] - 3 * shares[1][1] + shares[2][1]) % prime)
    print("Восстановленный секрет:", restored_secret)
    print("Секрет восстановлен:", restored_secret == secret)
    print("\nПопытка восстановления по двум долям:")
    try:
        restore_secret(shares[:2], prime)
    except ValueError as error:
        print(error)
    print("Через две доли проходят полиномы с любым значением S из поля.")


if __name__ == "__main__":
    main()
