from random import randint
from printer import term_colors as tc
from user import User
from graphviz import Source
from os import path as os_path, makedirs as os_makedirs
from utils import get_inverse


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
            f"Creating an ElGamal encryption system ({tc.BOLD.value}p{tc.RESET.value}=",
            end="",
        )
        self._is_valid_prime(p)

        print(
            f"{tc.BOLD.value}{tc.YELLOW.value}{p}{tc.RESET.value}, {tc.BOLD.value}g{tc.RESET.value}=",
            end="",
        )
        self._is_valid_generator(p, g)

        g = g % p
        print(f"{tc.BOLD.value}{tc.YELLOW.value}{g}{tc.RESET.value})...", end=" ")

        self.p = p
        self.g = g
        self.pks = {}
        self.users = []
        self.nb_users = 0
        self.message_queue = []

        print(f"{tc.GREEN.value}OK{tc.RESET.value}")
        if self.debug:
            print(f"- Set of messages: {tc.BOLD.value}(ℤ/{p}ℤ)×{tc.RESET.value}")
            print(
                f"- Set of encrypted messages: {tc.BOLD.value}(ℤ/{p}ℤ)×²{tc.RESET.value}"
            )
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
            print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(f"{tc.RED.value}Given number is negative!{tc.RESET.value}")
        if n == 0:
            print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(f"{tc.RED.value}Given number is null!{tc.RESET.value}")

        for i in range(2, n):
            if (n % i) == 0:
                print(f"{tc.RED.value}KO{tc.RESET.value}")
                raise Exception(
                    f"{tc.RED.value}Given number is not prime!{tc.RESET.value}"
                )

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
            print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given generator is negative!{tc.RESET.value}"
            )
        if g == 0:
            print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(f"{tc.RED.value}Given generator is null!{tc.RESET.value}")

        nb_seen = 0
        seen = [False] * p
        for i in range(1, p):
            curr = (g**i) % p
            if not seen[curr]:
                seen[curr] = True
                nb_seen += 1
            else:
                print(f"{tc.RED.value}KO{tc.RESET.value}")
                raise Exception(
                    f"{tc.RED.value}Given generator is not a generator of the multiplicative group {tc.BOLD.value}(ℤ/{p}ℤ)×{tc.RESET.value}!{tc.RESET.value}"
                )

        if nb_seen != p - 1:
            print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given generator is not a generator of the multiplicative group {tc.BOLD.value}(ℤ/{p}ℤ)×{tc.RESET.value}!{tc.RESET.value}"
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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
                raise Exception(
                    f"{tc.RED.value}Given name for user is empty!{tc.RESET.value}"
                )

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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given private key for user is negative!{tc.RESET.value}"
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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given public key for user is empty!{tc.RESET.value}"
            )

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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given message is greater than {tc.BOLD.value}p{tc.RESET.value}={tc.BOLD.value}{self.p}{tc.RESET.value}!{tc.RESET.value}"
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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(f"{tc.RED.value}Given message is empty!{tc.RESET.value}")

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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given sender and receiver are the same!{tc.RESET.value}"
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
                print(f"{tc.RED.value}KO{tc.RESET.value}")
            raise Exception(
                f"{tc.RED.value}Given name for user is not in user list!{tc.RESET.value}"
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
                f"Adding new user {tc.BOLD.value}{tc.YELLOW.value}{name if (name != None and name != '') else 'ERROR'}{tc.RESET.value}...",
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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")

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
                    print(f"{tc.GREEN.value}OK{tc.RESET.value}")
                return
        print(f'{tc.RED.value}Couldn\'t find user "{name}" to remove{tc.RESET.value}')

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
                    print(f"{tc.GREEN.value}OK{tc.RESET.value}")
                return user
        print(f'{tc.RED.value}Couldn\'t find user "{name}"{tc.RESET.value}')

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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f'Public key for user "{name}": {tc.BOLD.value}{tc.BLUE.value}{pk}{tc.RESET.value}'
            )
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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f'New private key for user "{name}": {tc.BOLD.value}{tc.RED.value}{new_sk}{tc.RESET.value}'
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
                f"Encrypting character {tc.BOLD.value}{tc.YELLOW.value}{char}{tc.RESET.value} from {src} to {dst}...",
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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f"Encrypted character: ({tc.BOLD.value}c1{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{c1}{tc.RESET.value}, {tc.BOLD.value}c2{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{c2}{tc.RESET.value})"
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
                f"Sending message {tc.BOLD.value}{tc.YELLOW.value}{m}{tc.RESET.value} from {src} to {dst}...",
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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f'Encrypted message: "{tc.BOLD.value}{tc.YELLOW.value}{chars}{tc.RESET.value}"'
            )

        # 3. Update users' messages & connections
        src_user.sent_messages.append(m)
        src_user.nb_sent_messages += 1
        src_user.connections.append(dst)

        # 4. Send message to receiver
        self.message_queue.insert(0, (dst, (src, chars)))

        # 5. Return encrypted message
        return (src, chars)

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
                f"Decrypting character ({tc.BOLD.value}c1{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{char[0]}{tc.RESET.value}, {tc.BOLD.value}c2{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{char[1]}{tc.RESET.value}) for {dst}...",
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
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f"Decrypted character: {tc.BOLD.value}{tc.YELLOW.value}{dec}{tc.RESET.value}"
            )

        # 2. Return decrypted character
        return dec

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
                f"Receiving message from {tc.BOLD.value}{tc.YELLOW.value}{encrypted[0]}{tc.RESET.value}..."
            )

        self._is_valid_username(dst)
        self._user_exists(dst)

        # 0. Get encrypted message
        chars, m = encrypted[1], ""

        # 1. Decrypt each char of the message
        for char in chars:
            m += chr(self.decrypt_char(dst, char, debug))

        if self.debug or debug:
            print(f"{tc.GREEN.value}OK{tc.RESET.value}")
            print(
                f"Decrypted message: {tc.BOLD.value}{tc.YELLOW.value}{m}{tc.RESET.value}"
            )

        # 2. Update destination user's messages stats
        dst_user = self.get_user(dst)
        dst_user.received_messages.append(m)
        dst_user.nb_received_messages += 1

        # 3. Delete message from queue
        self.message_queue.pop()

        # 4. Return decrypted message
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
            f"Number of connected users: {tc.BOLD.value}{tc.YELLOW.value}{self.nb_users}{tc.RESET.value}"
        )
        self.print_users()
        self.print_user_connections()

    def print_users(self) -> None:
        """
        Print the users of the encryption system.
        """
        for i in range(self.nb_users):
            curr_user = self.users[i]
            print(
                f"- User {i+1}: "
                + str(curr_user)
                + f", {tc.BOLD.value}pk{tc.RESET.value}={tc.BOLD.value}{tc.BLUE.value}{self.pks[curr_user.name]}{tc.RESET.value})"
            )
            self.users[i].print_inbox()
            print()

    def print_user_connections(self) -> None:
        """
        Print the connections between users.
        """
        print("Connections between users:")
        for user in self.users:
            if user.connections:
                print(
                    f"{tc.BOLD.value}{tc.YELLOW.value}{user.name}{tc.RESET.value} is connected to: {', '.join(user.connections)}"
                )
            else:
                print(
                    f"{tc.BOLD.value}{tc.YELLOW.value}{user.name}{tc.RESET.value} is not connected to any user."
                )

    def __str__(self) -> str:
        """
        Return a string representation of the encryption system.

        Returns:
        --------
        str
            A string representation of the encryption system.
        """
        return (
            f"ElGamal encryption system ({tc.BOLD.value}p{tc.RESET.value}={tc.BOLD.value}{tc.BLUE.value}{self.p}{tc.RESET.value}, {tc.BOLD.value}g{tc.RESET.value}={tc.BOLD.value}{tc.BLUE.value}{self.g}{tc.RESET.value})"
            + f" with {tc.BOLD.value}{tc.BLUE.value}{self.nb_users}{tc.RESET.value} users.\n"
            + f"Current message queue: {tc.BOLD.value}{tc.YELLOW.value}{self.message_queue}{tc.RESET.value}\n"
        )

    def to_dot(self) -> str:
        """
        Convert the encryption system to a dot format string.

        Returns:
        --------
        str
            A dot format string of the encryption system.
        """

        dot_string = "digraph CryptoSystem {\n"
        dot_string += "    node [shape=plaintext]\n"
        dot_string += '    labelloc="t";\n'
        dot_string += '    labeljust="c";\n'
        dot_string += (
            '    label="ElGamal, p='
            + str(self.p)
            + ", g="
            + str(self.g)
            + ", nb_users="
            + str(self.nb_users)
            + '";\n'
            "    fontsize=20;\n"
        )

        # Add users to the graph
        for user in self.users:
            user_pk = self.get_user_pk(user.name)
            user_info = f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0"><TR><TD>{user.name}</TD></TR><TR><TD><FONT COLOR="blue">pk={user_pk}</FONT></TD></TR><TR><TD><FONT COLOR="red">sk={user.sk}</FONT></TD></TR></TABLE>>'
            dot_string += f"    {user.name} [label={user_info}];\n"

        # Add connections between users
        connected = set()
        for user in self.users:
            for connection in user.connections:
                if connection in connected:
                    continue
                dot_string += (
                    f"    {user.name} -> {connection};\n"  # Use -> for directed edges
                )
                connected.add((user.name, connection))

        dot_string += "}\n"
        return dot_string

    def export_graph(
        self, filename="elgamal_graph", folder="graphs_elgamal", same=False, debug=False
    ) -> None:
        """
        Export a dot format string into a PNG file.

        Parameters:
        -----------
        filename : str, optional
            The name of the PNG file, by default "elgamal_graph"
        folder : str, optional
            The folder to save the PNG file, by default "graphs_elgamal"
        same : bool, optional
            A boolean to save the PNG file with the same name, by default False
        debug : bool, optional
            A boolean to print debug information, by default False

        Raises:
        -------
        Exception
            If the folder doesn't exist.
        """

        if self.debug or debug:
            print(f"Exporting {tc.BOLD.value}ElGamal{tc.RESET.value} graph to PNG...")

        dot_graph = self.to_dot()
        if same:
            filepath = os_path.join(folder, filename)
        else:
            if not os_path.exists(folder):
                os_makedirs(folder)

            counter = 1
            while True:
                filepath = os_path.join(folder, f"{filename}_{counter}")
                if not os_path.exists(filepath + ".png"):
                    break
                counter += 1

        source = Source(dot_graph, filename=filepath, format="png")
        source.render(filename=filepath, view=False, cleanup=True)

        if self.debug or debug:
            print(
                f"Graph exported to {tc.BOLD.value}{tc.YELLOW.value}{filepath}.png{tc.RESET.value}"
            )
