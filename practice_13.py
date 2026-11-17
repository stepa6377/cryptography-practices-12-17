def point_on_curve(point, prime, coefficient_a, coefficient_b):
    if point is None:
        return True
    x, y = point
    return (y * y - x ** 3 - coefficient_a * x - coefficient_b) % prime == 0


def curve_points(prime, coefficient_a, coefficient_b):
    points = []
    for x in range(prime):
        for y in range(prime):
            if point_on_curve((x, y), prime, coefficient_a, coefficient_b):
                points.append((x, y))
    points.append(None)
    return points


def add_points(first, second, prime, coefficient_a):
    if first is None:
        return second
    if second is None:
        return first
    x1, y1 = first
    x2, y2 = second
    if x1 == x2 and (y1 + y2) % prime == 0:
        return None
    if first == second:
        numerator = 3 * x1 * x1 + coefficient_a
        denominator = 2 * y1
    else:
        numerator = y2 - y1
        denominator = x2 - x1
    slope = numerator * pow(denominator, -1, prime) % prime
    x3 = (slope * slope - x1 - x2) % prime
    y3 = (slope * (x1 - x3) - y1) % prime
    return x3, y3


def multiply_point(number, point, prime, coefficient_a):
    if number < 0:
        raise ValueError("Множитель не должен быть отрицательным.")
    result = None
    for step in range(number):
        result = add_points(result, point, prime, coefficient_a)
    return result


def encrypt_message(
    message, public_key, base_point, nonce, prime, coefficient_a
):
    if not 0 <= message < prime:
        raise ValueError("Сообщение должно быть от 0 до p - 1.")
    first = multiply_point(nonce, base_point, prime, coefficient_a)
    shared_point = multiply_point(nonce, public_key, prime, coefficient_a)
    if first is None or shared_point is None or shared_point[0] == 0:
        raise ValueError("Выберите другое k: нужна ненулевая абсцисса.")
    second = message * shared_point[0] % prime
    return first, second, shared_point


def decrypt_message(first, second, private_key, prime, coefficient_a):
    shared_point = multiply_point(private_key, first, prime, coefficient_a)
    if shared_point is None or shared_point[0] == 0:
        raise ValueError("Невозможно обратить секретную абсциссу.")
    message = second * pow(shared_point[0], -1, prime) % prime
    return message, shared_point


def main():
    prime = 7
    coefficient_a = 2
    coefficient_b = 6
    base_point = (2, 2)
    print("Практика 13. Кривая y^2 = x^3 + 2x + 6 (mod 7)")
    print("None обозначает бесконечно удалённую точку O.")
    points = curve_points(prime, coefficient_a, coefficient_b)
    print("Точки кривой:", points)
    print("Количество точек с учётом O:", len(points))

    print("\nЗадание 1. Композиции точек")
    doubled = add_points(base_point, base_point, prime, coefficient_a)
    tripled = add_points(doubled, base_point, prime, coefficient_a)
    total = add_points(base_point, (3, 2), prime, coefficient_a)
    print("[2](2, 2) =", doubled)
    print("[3](2, 2) =", tripled)
    print("(2, 2) + (3, 2) =", total)

    print("\nЗадание 2. Шифр Эль-Гамаля на эллиптической кривой")
    order = 11
    private_key = 5
    nonce = 3
    message = 5
    public_key = multiply_point(private_key, base_point, prime, coefficient_a)
    first, second, shared_point = encrypt_message(
        message, public_key, base_point, nonce, prime, coefficient_a
    )
    restored_message, restored_point = decrypt_message(
        first, second, private_key, prime, coefficient_a
    )
    print("G =", base_point, "q =", order, "c =", private_key, "k =", nonce)
    print("[q]G =", multiply_point(order, base_point, prime, coefficient_a))
    print("Открытый ключ D = [c]G =", public_key)
    print("R = [k]G =", first)
    print("P = [k]D =", shared_point)
    print("e = m * x(P) mod p =", second)
    print("Шифротекст (R, e) =", (first, second))
    print("Q = [c]R =", restored_point)
    print("Расшифрованное сообщение:", restored_message)
    print("Сообщение восстановлено:", restored_message == message)


if __name__ == "__main__":
    main()
