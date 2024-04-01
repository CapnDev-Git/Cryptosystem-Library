import random
from cryptosystems import ElGamal
from utils import generate_usernames
from printer import term_colors as tc
from attacker import Attacker


def send_generated_messages(eg: ElGamal, nb_users: int, nb_messages: int, debug=False):
    """
    Generate and send nb_messages messages randomly.

    Parameters:
    -----------
    nb_users : int
        The number of users.
    nb_messages : int
        The number of messages to send.
    usernames : list
        A list of user names.
    eg : ElGamal
        An ElGamal object.
    """

    usernames = generate_usernames(nb_users)
    for username in usernames:
        eg.add_user(username, debug=debug)
    print()

    for _ in range(nb_messages):
        sender = random.choice(usernames)
        receiver = random.choice(usernames)
        while receiver == sender:
            receiver = random.choice(usernames)
        message = f"{sender} -> {receiver}"

        if debug:
            print(
                f'Sending message from {tc.BOLD.value}{tc.BLUE.value}{sender}{tc.RESET.value} to {tc.BOLD.value}{tc.RED.value}{receiver}{tc.RESET.value}: "{tc.BOLD.value}{tc.YELLOW.value}{message}{tc.RESET.value}"...',
                end=" ",
            )

        encr_message = eg.send_message(sender, receiver, message, debug=debug)
        eg.receive_message(receiver, encr_message, debug=debug)

        if debug:
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")


def main():
    # Create an ElGamal object with p = 257 and g = 3
    eg = ElGamal(257, 3, debug=False)  # min 257

    # Create an attacker object
    attacker = Attacker("Attacker", eg)

    # Send 25 messages to 20 users
    send_generated_messages(eg, 20, 25)

    # Actualize the users in the attacker object
    attacker.actualize_users()
    print(attacker)

    # Export a dot format string into a PNG file
    eg.export_graph(folder="output", same=True)


if __name__ == "__main__":
    main()
