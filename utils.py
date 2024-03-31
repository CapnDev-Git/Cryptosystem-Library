def find_generator(p: int) -> int:
    """
    Find a generator of the cyclic group Z/pZ, where p is a prime number given as input.

    Attributes
    ----------
    p : int
        A prime number.

    Returns
    -------
    int
        A generator of the group Z/pZ.
    """

    # Check if the input is a prime number
    for i in range(2, p):
        # Initialize a list to keep track of the elements we have seen
        seen = [False] * p
        nb_seen = 0

        # Compute the powers of i modulo p
        for j in range(1, p):
            curr = (i**j) % p

            # If we have not seen the element yet, we increment the counter
            if not seen[curr]:
                seen[curr] = True
                nb_seen += 1
            else:
                break

        # Check if we have seen all the elements of the group (except 0)
        if nb_seen == p - 1:
            # If we have seen all the elements of the group, then i is a generator
            return i

    # If we have not found a generator, we return -1
    return -1


def find_prime_above(n: int) -> int:
    """
    Find the first prime number greater than n.

    Attributes
    ----------
    n : int
        An integer.

    Returns
    -------
    int
        The first prime number greater than n.
    """

    # Start from n and look for the first prime number
    for i in range(n, 2 * n):
        # Check if i is a prime number
        for j in range(2, i):
            # If i is divisible by j, then i is not a prime number
            if (i % j) == 0:
                break
        else:
            # If i is not divisible by any number, then i is a prime number
            return i

    # No prime number found
    return -1


def get_inverse(n: int, p: int) -> int:
    """
    Compute the inverse of n modulo p.

    Attributes
    ----------
    n : int
        An integer.
    p : int
        An integer.

    Returns
    -------
    int
        The inverse of n modulo p.
    """

    # Consequence of Little Fermat's theorem: a^(p-1) = 1 mod p
    return pow(n, p - 2, p)
