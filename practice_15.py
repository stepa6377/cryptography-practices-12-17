from math import gcd


def receive_banknote(
    number, blinding_factor, modulus, public_exponent, private_exponent
):
    if not 0 < number < modulus:
        raise ValueError("Номер банкноты должен быть от 1 до N - 1.")
    if not 1 < blinding_factor < modulus or gcd(blinding_factor, modulus) != 1:
        raise ValueError("Множитель ослепления должен быть взаимно прост с N.")
    blinded_number = number * pow(blinding_factor, public_exponent, modulus)
    blinded_number %= modulus
    blinded_signature = pow(blinded_number, private_exponent, modulus)
    signature = blinded_signature * pow(blinding_factor, -1, modulus) % modulus
    return signature, blinded_number, blinded_signature


def verify_banknote(number, signature, modulus, public_exponent):
    if not 0 < number < modulus or not 0 <= signature < modulus:
        return False
    return pow(signature, public_exponent, modulus) == number


def main():
    print("Практика 15. Слепая подпись RSA")
    print("\nЗадание 1. Ключи банка")
    first_prime = 17
    second_prime = 11
    modulus = first_prime * second_prime
    totient = (first_prime - 1) * (second_prime - 1)
    public_exponent = 7
    private_exponent = pow(public_exponent, -1, totient)
    print("P =", first_prime, "Q =", second_prime)
    print("N = P * Q =", modulus, "phi(N) =", totient)
    print("Открытый ключ (N, e) =", (modulus, public_exponent))
    print("Секретный ключ (N, d) =", (modulus, private_exponent))
    print("e * d mod phi(N) =", public_exponent * private_exponent % totient)

    print("\nЗадание 2. Две банкноты одинакового номинала")
    print("n1 = 11 и n2 = 22 считаем номерами банкнот.")
    print("Схема: покупатель -> банк: t = n * b^e mod N")
    print("Банк -> покупатель: u = t^d mod N")
    print("Покупатель снимает ослепление: s = u * b^(-1) mod N")
    print("Проверка банкноты: s^e mod N = n")
    banknotes = []
    for number, blinding_factor in [(11, 2), (22, 3)]:
        signature, blinded_number, blinded_signature = receive_banknote(
            number, blinding_factor, modulus, public_exponent, private_exponent
        )
        banknotes.append((number, signature))
        valid = verify_banknote(number, signature, modulus, public_exponent)
        print("\nНомер n =", number, "множитель b =", blinding_factor)
        print("Покупатель -> банк, t =", blinded_number)
        print("Банк -> покупатель, u =", blinded_signature)
        print("Банкнота (n, s) =", (number, signature))
        print("s^e mod N =", pow(signature, public_exponent, modulus))
        print("Банкнота верна:", valid)

    print("\nЗадание 3. Получение третьей банкноты")
    first_number, first_signature = banknotes[0]
    second_number, second_signature = banknotes[1]
    forged_number = first_number * second_number % modulus
    forged_signature = first_signature * second_signature % modulus
    valid = verify_banknote(
        forged_number, forged_signature, modulus, public_exponent
    )
    print("n3 = n1 * n2 mod N =", forged_number)
    print("s3 = s1 * s2 mod N =", forged_signature)
    print("Третья банкнота (n3, s3) =", (forged_number, forged_signature))
    print("s3^e mod N =", pow(forged_signature, public_exponent, modulus))
    print("Третья банкнота проходит проверку:", valid)
    print("Доказательство: (s1 * s2)^e = s1^e * s2^e = n1 * n2 (mod N).")


if __name__ == "__main__":
    main()
