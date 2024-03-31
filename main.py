from cryptosystems import ElGamal
from attacker import Attacker, AttackType, CryptosystemType


def main():
    src = "Alice"
    dst = "Bob"
    atk = "Eve"
    msg = f"Hello, {dst}! This is a test message from {src}."

    # Create an ElGamal object with p = 257 and g = 3
    eg = ElGamal(257, 3, False)
    print()

    # Add users Alice, Bob, and Eve
    eg.add_user(src, True)
    eg.add_user(dst, True)
    print()

    attacker = Attacker(atk, eg)
    print(attacker)

    # Send message
    m1 = eg.send_message(src, dst, msg)

    # use queue system to 'receive' message

    # Intercept message
    secret_keys = attacker.intercept_message(AttackType.BRUTE_FORCE, debug=True)
    print()

    # # Receive messages
    # eg.receive_message(dst, m1)
    # print()

    # Print the status of the ElGamal object
    print(attacker)
    eg.print_status()
    print()


if __name__ == "__main__":
    main()
