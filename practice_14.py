from practice_13 import add_points, curve_points, multiply_point


def sign_message(
    hash_value, private_key, nonce, base_point, prime, order, coefficient_a
):
    if not 0 < private_key < order or not 0 < nonce < order:
        raise ValueError("Секретный ключ и k должны быть от 1 до q - 1.")
    reduced_hash = hash_value % order
    if reduced_hash == 0:
        reduced_hash = 1
    point = multiply_point(nonce, base_point, prime, coefficient_a)
    if point is None:
        raise ValueError("Выберите другое k.")
    first = point[0] % order
    second = (first * private_key + nonce * reduced_hash) % order
    if first == 0 or second == 0:
        raise ValueError("Нулевая часть подписи: выберите другое k.")
    return first, second, point


def verify_signature(
    hash_value, first, second, public_key,
    base_point, prime, order, coefficient_a
):
    if not 0 < first < order or not 0 < second < order:
        return False, None, None, None, None
    reduced_hash = hash_value % order
    if reduced_hash == 0:
        reduced_hash = 1
    inverse_hash = pow(reduced_hash, -1, order)
    first_number = second * inverse_hash % order
    second_number = -first * inverse_hash % order
    first_point = multiply_point(
        first_number, base_point, prime, coefficient_a
    )
    second_point = multiply_point(
        second_number, public_key, prime, coefficient_a
    )
    point = add_points(first_point, second_point, prime, coefficient_a)
    if point is None:
        return False, inverse_hash, first_number, second_number, point
    valid = point[0] % order == first
    return valid, inverse_hash, first_number, second_number, point


def main():
    print("Практика 14")
    print("\nЗадание 1. Количество точек E11(2, 5)")
    points = curve_points(11, 2, 5)
    print("None обозначает бесконечно удалённую точку O.")
    print("Точки кривой:", points)
    print("Количество конечных точек:", len(points) - 1)
    print("Всего точек с учётом O:", len(points))

    print("\nЗадание 2. Подпись ГОСТ Р 34.10-2001")
    prime = 7
    order = 11
    coefficient_a = 2
    base_point = (2, 2)
    private_key = 5
    nonce = 3
    hash_value = 9
    public_key = multiply_point(private_key, base_point, prime, coefficient_a)
    first, second, point = sign_message(
        hash_value, private_key, nonce, base_point, prime, order, coefficient_a
    )
    verification = verify_signature(
        hash_value, first, second, public_key,
        base_point, prime, order, coefficient_a
    )
    valid, inverse_hash, first_number, second_number, point = verification
    print("E7(2, 6), G =", base_point, "q =", order)
    print("m = h(M) =", hash_value, "d =", private_key, "k =", nonce)
    print("Q = [d]G =", public_key, "C = [k]G =", point)
    print("Подпись (r, s) =", (first, second))
    print("v =", inverse_hash, "z1 =", first_number, "z2 =", second_number)
    print("[z1]G + [z2]Q =", point)
    print("R = x(C) mod q =", point[0] % order, "r =", first)
    print("Подпись верна:", valid)


if __name__ == "__main__":
    main()
