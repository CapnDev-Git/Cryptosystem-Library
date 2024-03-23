from printer import term_colors as tc

class User:
    """
    Class to define a user in the ElGamal encryption system.

    Attributes:
    -----------
    name : str
        The name of the user.
    sk : int
        The private key of the user.
    received_messages : list
        A list to store received messages.
    nb_received_messages : int
        The number of received messages.
    sent_messages : list
        A list to store sent messages.
    nb_sent_messages : int
        The number of sent messages.

    Methods:
    --------
    __init__(name: str, sk: int) -> None
        Initialize a user with a name and a private key.
    __str__() -> str
        Return a string representation of the user.
    print_inbox() -> None
        Print the received and sent messages of the user.
    """
    
    def __init__(self, name: str, sk: int) -> None:
        """
        Initialize a user with a name and a private key.

        Parameters:
        -----------
        name : str
            The name of the user.
        sk : int
            The private key of the user.
        """
        self.name = name
        self.sk = sk
        self.received_messages = []
        self.nb_received_messages = 0
        self.sent_messages = []
        self.nb_sent_messages = 0

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
        --------
        str
            A string representation of the user.
        """
        return (
            f'"{self.name}" ({tc.BOLD}sk{tc.RESET}={tc.BOLD}{tc.RED}{self.sk}{tc.RESET}'
        )

    def print_inbox(self) -> None:
        """
        Print the received and sent messages of the user.
        """
        if self.nb_received_messages == 0 and self.nb_sent_messages == 0:
            print(f"{self.name} has no messages.")
            return

        if self.nb_received_messages == 0:
            print(f"{self.name} has no received messages.")
        elif self.nb_received_messages == 1:
            print(
                f"{self.name} has received {tc.BOLD}{tc.YELLOW}{self.nb_received_messages}{tc.RESET} message:"
            )
        else:
            print(
                f"{self.name} has received {tc.BOLD}{tc.YELLOW}{self.nb_received_messages}{tc.RESET} messages:"
            )
        for i in range(self.nb_received_messages):
            print(f'- "{self.received_messages[i]}"')

        if self.nb_sent_messages == 0:
            print(f"{self.name} has no sent messages.")
        elif self.nb_sent_messages == 1:
            print(
                f"{self.name} has sent {tc.BOLD}{tc.YELLOW}{self.nb_sent_messages}{tc.RESET} message:"
            )
        else:
            print(
                f"{self.name} has sent {tc.BOLD}{tc.YELLOW}{self.nb_sent_messages}{tc.RESET} messages:"
            )
        for i in range(self.nb_sent_messages):
            print(f'- "{self.sent_messages[i]}"')
