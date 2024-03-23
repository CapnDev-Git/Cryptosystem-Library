from random import randint
from printer import term_colors as tc
from helpers import get_inverse
from user import User

class ElGamal:
    """
    Class to define an ElGamal encryption system.

    Attributes:
    -----------
    p : int
        The prime number for the encryption system.
    g : int
        The generator for the encryption system.
    pks : dict
        A dictionary to store the public keys of the users.
    users : list
        A list to store the users.
    nb_users : int
        The number of users in the encryption system.
    debug : bool
        A boolean to print debug information.

    Methods:
    --------
    _is_valid_prime(n: int) -> None
        Check if a number is prime.
    _is_valid_generator(p: int, g: int) -> None
        Check if a number is a generator of the multiplicative group.
    _is_valid_username(name: str) -> None
        Check if a username is valid.
    _is_valid_sk(sk: int) -> None
        Check if a private key is valid.
    _is_valid_pk(pk: int) -> None
        Check if a public key is valid.
    _is_valid_char(char: str) -> None
        Check if a character is valid.
    _is_valid_message(m: str) -> None
        Check if a message is valid.
    _is_valid_dst(src: str, dst: str) -> None
        Check if a sender and receiver are different.
    _user_exists(name: str) -> None
        Check if a user exists.
    add_user(name: str, debug: bool = False) -> None
        Add a user to the encryption system.
    remove_user(name: str, debug: bool = False) -> None
        Remove a user from the encryption system.
    get_user(name: str, debug: bool = False) -> User
        Get a user from the encryption system.
    get_user_pk(name: str, debug: bool = False) -> int
        Get the public key of a user.
    get_new_sk(name: str, debug: bool = False) -> int
        Generate a new private key for a user.
    encrypt_char(src: str, dst: str, char: str, debug: bool = False) -> tuple
        Encrypt a character from a sender to a receiver.
    send_message(src: str, dst: str, m: str, debug: bool = False) -> list
        Send a message from a sender to a receiver.
    decrypt_char(dst: str, char: tuple, debug: bool = False) -> int
        Decrypt a character for a receiver.
    receive_message(dst: str, encrypted: list, debug: bool = False) -> str
        Receive a message for a receiver.
    print_status() -> None
        Print the status of the encryption system.
    print_users() -> None
        Print the users of the encryption system.
    __str__() -> str
        Return a string representation of the encryption system.
    """

    def __init__(self, p: int, g: int, debug: bool = True) -> None:
        """
        Initialize ElGamal encryption system with prime number p and generator g.

        Parameters:
        -----------
        p : int
            The prime number for the encryption system.
        g : int
            The generator for the encryption system.
        debug : bool, optional
            A boolean to print debug information, by default True
        """
        self.debug = debug

        print(
            f"Creating an ElGamal encryption system ({tc.BOLD}p{tc.RESET}=",
            end="",
        )
        self._is_valid_prime(p)

        print(
            f"{tc.BOLD}{tc.YELLOW}{p}{tc.RESET}, {tc.BOLD}g{tc.RESET}=",
            end="",
        )
        self._is_valid_generator(p, g)

        g = g % p
        print(f"{tc.BOLD}{tc.YELLOW}{g}{tc.RESET})...", end=" ")

        self.p = p
        self.g = g
        self.pks = {}
        self.users = []
        self.nb_users = 0

        print(f"{tc.GREEN}OK{tc.RESET}")
        if self.debug:
            print(f"- Set of messages: {tc.BOLD}(ℤ/{p}ℤ)×{tc.RESET}")
            print(f"- Set of encrypted messages: {tc.BOLD}(ℤ/{p}ℤ)×²{tc.RESET}")
        self.print_status()

    ## Private methods (validity checks)

    def _is_valid_prime(self, n: int) -> None:
        """
        Check if a number is prime.

        Parameters:
        -----------
        n : int
            The number to check.
        """
        if n < 0:
            print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given number is negative!{tc.RESET}")
        if n == 0:
            print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given number is null!{tc.RESET}")

        for i in range(2, n):
            if (n % i) == 0:
                print(f"{tc.RED}KO{tc.RESET}")
                raise Exception(f"{tc.RED}Given number is not prime!{tc.RESET}")

    def _is_valid_generator(self, p: int, g: int) -> None:
        """
        Check if a number is a generator of the multiplicative group.

        Parameters:
        -----------
        p : int
            The prime number.
        g : int
            The number to check as a generator.
        """
        if g < 0:
            print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given generator is negative!{tc.RESET}")
        if g == 0:
            print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given generator is null!{tc.RESET}")

        nb_seen = 0
        seen = [False] * p
        for i in range(1, p):
            curr = (g**i) % p
            if not seen[curr]:
                seen[curr] = True
                nb_seen += 1
            else:
                print(f"{tc.RED}KO{tc.RESET}")
                raise Exception(
                    f"{tc.RED}Given generator is not a generator of the multiplicative group {tc.BOLD}(ℤ/{p}ℤ)×{tc.RESET}!{tc.RESET}"
                )

        if nb_seen != p - 1:
            print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(
                f"{tc.RED}Given generator is not a generator of the multiplicative group {tc.BOLD}(ℤ/{p}ℤ)×{tc.RESET}!{tc.RESET}"
            )

    def _is_valid_username(self, name: str) -> None:
        """
        Check if a username is valid.

        Parameters:
        -----------
        name : str
            The username to check.
        """
        if name == None or name == "":
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
                raise Exception(f"{tc.RED}Given name for user is empty!{tc.RESET}")

    def _is_valid_sk(self, sk: int) -> None:
        """
        Check if a private key is valid.

        Parameters:
        -----------
        sk : int
            The private key to check.
        """
        if sk < 0:
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(
                f"{tc.RED}Given private key for user is negative!{tc.RESET}"
            )

    def _is_valid_pk(self, pk: int) -> None:
        """
        Check if a public key is valid.

        Parameters:
        -----------
        pk : int
            The public key to check.
        """
        if pk == None:
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given public key for user is empty!{tc.RESET}")

    def _is_valid_char(self, char: str) -> None:
        """
        Check if a character is valid.

        Parameters:
        -----------
        char : str
            The character to check.
        """
        if ord(char) > self.p:
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(
                f"{tc.RED}Given message is greater than {tc.BOLD}p{tc.RESET}={tc.BOLD}{self.p}{tc.RESET}!{tc.RESET}"
            )

    def _is_valid_message(self, m: str) -> None:
        """
        Check if a message is valid.

        Parameters:
        -----------
        m : str
            The message to check.
        """
        if m == None or m == "":
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(f"{tc.RED}Given message is empty!{tc.RESET}")

    def _is_valid_dst(self, src: str, dst: str) -> None:
        """
        Check if a sender and receiver are different.

        Parameters:
        -----------
        src : str
            The sender's name.
        dst : str
            The receiver's name.
        """
        if src == dst:
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(
                f"{tc.RED}Given sender and receiver are the same!{tc.RESET}"
            )

    def _user_exists(self, name: str) -> None:
        """
        Check if a user exists.

        Parameters:
        -----------
        name : str
            The name of the user.
        """
        if name not in self.pks:
            if self.debug:
                print(f"{tc.RED}KO{tc.RESET}")
            raise Exception(
                f"{tc.RED}Given name for user is not in user list!{tc.RESET}"
            )

    ## User methods

    def add_user(self, name: str, debug: bool = False) -> None:
        """
        Add a user to the encryption system.

        Parameters:
        -----------
        name : str
            The name of the user to add.
        debug : bool, optional
            A boolean to print debug information, by default False
        """
        if self.debug or debug:
            print(
                f"Adding new user \"{name if (name != None and name != '') else 'ERROR'}\"...",
                end=" ",
            )

        self._is_valid_username(name)

        sk = randint(1, self.p - 1)  # TODO fix random generation
        self._is_valid_sk(sk)

        pk = (self.g**sk) % self.p
        self.pks[name] = pk

        new_user = User(name, sk)
        self.users.append(new_user)
        self.nb_users += 1

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")

    def remove_user(self, name: str, debug: bool = False) -> None:
        """
        Remove a user from the encryption system.

        Parameters:
        -----------
        name : str
            The name of the user to remove.
        debug : bool, optional
            A boolean to print debug information, by default False
        """
        if self.debug or debug:
            print(f'Removing user "{name}"...', end=" ")

        self._is_valid_username(name)
        self._user_exists(name)

        for user in self.users:
            if user.name == name:
                self.users.remove(user)
                self.nb_users -= 1

                if self.debug or debug:
                    print(f"{tc.GREEN}OK{tc.RESET}")
                return
        print(f'{tc.RED}Couldn\'t find user "{name}" to remove{tc.RESET}')

    def get_user(self, name: str, debug: bool = False) -> User:
        """
        Get a user from the encryption system.

        Parameters:
        -----------
        name : str
            The name of the user to get.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        User
            The user object.
        """
        if self.debug or debug:
            print(f'Getting user "{name}"...', end=" ")

        self._is_valid_username(name)
        self._user_exists(name)

        for user in self.users:
            if user.name == name:
                if self.debug or debug:
                    print(f"{tc.GREEN}OK{tc.RESET}")
                return user
        print(f'{tc.RED}Couldn\'t find user "{name}"{tc.RESET}')

    def get_user_pk(self, name: str, debug: bool = False) -> int:
        """
        Get the public key of a user.

        Parameters:
        -----------
        name : str
            The name of the user.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        int
            The public key of the user.
        """
        if self.debug or debug:
            print(f'Getting public key of user "{name}"...', end=" ")

        self._is_valid_username(name)
        self._user_exists(name)

        pk = self.pks.get(name)
        self._is_valid_pk(pk)

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(f'Public key for user "{name}": {tc.BOLD}{tc.BLUE}{pk}{tc.RESET}')
        return pk

    def get_new_sk(self, name: str, debug: bool = False) -> int:
        """
        Generate a new private key for a user.

        Parameters:
        -----------
        name : str
            The name of the user.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        int
            The new private key for the user.
        """
        if self.debug or debug:
            print(f'Generating new private key for user "{name}"...', end=" ")

        self._is_valid_username(name)
        self._user_exists(name)

        new_sk = randint(1, self.p - 1)  # TODO fix random generation
        for user in self.users:
            if user.name == name:
                user.sk = new_sk
                break

        # Update public key!
        self.pks[name] = (self.g**new_sk) % self.p

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(
                f'New private key for user "{name}": {tc.BOLD}{tc.RED}{new_sk}{tc.RESET}'
            )
        return new_sk

    ## Message methods

    def encrypt_char(self, src: str, dst: str, char: str, debug: bool = False) -> tuple:
        """
        Encrypt a character from a sender to a receiver.

        Parameters:
        -----------
        src : str
            The sender's name.
        dst : str
            The receiver's name.
        char : str
            The character to encrypt.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        tuple
            The encrypted character.
        """
        if self.debug or debug:
            print(
                f"Encrypting character {tc.BOLD}{tc.YELLOW}{char}{tc.RESET} from {src} to {dst}...",
                end=" ",
            )

        self._is_valid_char(char)

        # 0. Get sender user
        src_user = self.get_user(src)

        # 1. Choose new secret key for sender
        self.get_new_sk(src)  # Also updates public key accordingly
        c1 = self.get_user_pk(src)  # c1 = g^sk

        # 2. Encrypt message with receiver's public key
        dst_pk = self.get_user_pk(dst)
        c2 = (ord(char) * (dst_pk**src_user.sk)) % self.p

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(
                f"Encrypted character: ({tc.BOLD}c1{tc.RESET}={tc.BOLD}{tc.YELLOW}{c1}{tc.RESET}, {tc.BOLD}c2{tc.RESET}={tc.BOLD}{tc.YELLOW}{c2}{tc.RESET})"
            )

        return (c1, c2)

    def send_message(self, src: str, dst: str, m: str, debug: bool = False) -> list:
        """
        Send a message from a sender to a receiver.

        Parameters:
        -----------
        src : str
            The sender's name.
        dst : str
            The receiver's name.
        m : str
            The message to send.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        list
            The encrypted message.
        """
        if self.debug or debug:
            print(
                f"Sending message {tc.BOLD}{tc.YELLOW}{m}{tc.RESET} from {src} to {dst}...",
                end=" ",
            )

        self._is_valid_message(m)
        self._is_valid_username(src)
        self._user_exists(src)
        self._is_valid_username(dst)
        self._user_exists(dst)
        self._is_valid_dst(src, dst)

        # 0. Get sender & receiver users
        src_user = self.get_user(src)

        # Loop through each char of the message
        chars = []
        for char in m:
            chars.append(self.encrypt_char(src, dst, char, debug))

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(f"Encrypted message: {tc.BOLD}{tc.YELLOW}{chars}{tc.RESET}")

        # 3. Update users' messages
        src_user.sent_messages.append(m)
        src_user.nb_sent_messages += 1

        # 4. Send message to receiver
        return chars

    def decrypt_char(self, dst: str, char: tuple, debug: bool = False) -> int:
        """
        Decrypt a character for a receiver.

        Parameters:
        -----------
        dst : str
            The receiver's name.
        char : tuple
            The encrypted character.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        int
            The decrypted character.
        """
        if self.debug or debug:
            print(
                f"Decrypting character ({tc.BOLD}c1{tc.RESET}={tc.BOLD}{tc.YELLOW}{char[0]}{tc.RESET}, {tc.BOLD}c2{tc.RESET}={tc.BOLD}{tc.YELLOW}{char[1]}{tc.RESET}) for {dst}...",
                end=" ",
            )

        c1 = char[0]
        c2 = char[1]

        # 0. Get receiver user
        dst_user = self.get_user(dst)

        # 1. Decrypt message
        c1_inv = get_inverse(c1**dst_user.sk, self.p)  # c1^-sk
        dec = (c1_inv * c2) % self.p  # m = c2 * c1^-sk

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(f"Decrypted character: {tc.BOLD}{tc.YELLOW}{dec}{tc.RESET}")

        return dec  # Return decrypted char

    def receive_message(self, dst: str, encrypted: list, debug: bool = False) -> str:
        """
        Receive a message for a receiver.

        Parameters:
        -----------
        dst : str
            The receiver's name.
        encrypted : list
            The encrypted message.
        debug : bool, optional
            A boolean to print debug information, by default False

        Returns:
        --------
        str
            The decrypted message.
        """
        if self.debug or debug:
            print(
                f"Receiving message ({tc.BOLD}c1{tc.RESET}={tc.BOLD}{tc.YELLOW}{encrypted[0]}{tc.RESET}, {tc.BOLD}c2{tc.RESET}={tc.BOLD}{tc.YELLOW}{encrypted[1]}{tc.RESET}) for {dst}...",
                end=" ",
            )

        chars = encrypted

        self._is_valid_username(dst)
        self._user_exists(dst)

        m = ""
        for char in chars:
            m += chr(self.decrypt_char(dst, char, debug))

        if self.debug or debug:
            print(f"{tc.GREEN}OK{tc.RESET}")
            print(f"Decrypted message: {tc.BOLD}{tc.YELLOW}{m}{tc.RESET}")

        # 3. Update users' messages
        dst_user = self.get_user(dst)
        dst_user.received_messages.append(m)
        dst_user.nb_received_messages += 1

        # 4. Send message to receiver
        return m

    ## Print methods

    def print_status(self) -> None:
        """
        Print the status of the encryption system.
        """
        if self.nb_users == 0:
            print("No users logged in.")
            return

        print(
            f"Number of connected users: {tc.BOLD}{tc.YELLOW}{self.nb_users}{tc.RESET}"
        )
        self.print_users()

    def print_users(self) -> None:
        """
        Print the users of the encryption system.
        """
        for i in range(self.nb_users):
            curr_user = self.users[i]
            print(
                f"- User {i+1}: "
                + str(curr_user)
                + f", {tc.BOLD}pk{tc.RESET}={tc.BOLD}{tc.BLUE}{self.pks[curr_user.name]}{tc.RESET})"
            )
            self.users[i].print_inbox()
            print()

    def __str__(self) -> str:
        """
        Return a string representation of the encryption system.

        Returns:
        --------
        str
            A string representation of the encryption system.
        """
        return (
            f"ElGamal encryption system ({tc.BOLD}p{tc.RESET}={tc.BOLD}{tc.BLUE}{self.p}{tc.RESET}, {tc.BOLD}g{tc.RESET}={tc.BOLD}{tc.BLUE}{self.g}{tc.RESET})"
            + f" with {tc.BOLD}{tc.BLUE}{self.nb_users}{tc.RESET} users"
        )
