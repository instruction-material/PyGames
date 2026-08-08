def diffie_hellman_brute_force_search(
    alpha_val, prime_mod_val, intercepted_a, intercepted_b
):
    secret_x = secret_y = -1

    for exponent_guess in range(1, prime_mod_val):
        calculated_val = pow(alpha_val, exponent_guess, prime_mod_val)

        if calculated_val == intercepted_a:
            secret_x = exponent_guess
        if calculated_val == intercepted_b:
            secret_y = exponent_guess

        if secret_x != -1 and secret_y != -1:
            break

    shared_key = (
        -1 if secret_x == -1 else pow(intercepted_b, secret_x, prime_mod_val)
    )

    return secret_x, secret_y, shared_key


print(
    f"Recovered secrets and key: {diffie_hellman_brute_force_search(6, 13, 9, 2)}"
)
