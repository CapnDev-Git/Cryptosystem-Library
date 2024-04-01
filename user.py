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
        self.connections = []

    def __str__(self) -> str:
        """
        Return a string representation of the user.

        Returns:
        --------
        str
            A string representation of the user.
        """
        return f"{tc.BOLD.value}{tc.YELLOW.value}{self.name}{tc.RESET.value} ({tc.BOLD.value}sk{tc.RESET.value}={tc.BOLD.value}{tc.RED.value}{self.sk}{tc.RESET.value}"

    def print_inbox(self) -> None:
        """
        Print the received and sent messages of the user.
        """
        if self.nb_received_messages == 0 and self.nb_sent_messages == 0:
            print(
                f"{tc.RED.value}{self.name} has not received or sent any messages.{tc.RESET.value}"
            )
            return

        if self.nb_received_messages == 0:
            print(
                f"{tc.RED.value}{self.name} has no received messages.{tc.RESET.value}"
            )
        elif self.nb_received_messages == 1:
            print(
                f"{tc.BOLD.value}{tc.YELLOW.value}{self.name}{tc.RESET.value} has received {tc.BOLD.value}{tc.YELLOW.value}{self.nb_received_messages}{tc.RESET.value} message:"
            )
        else:
            print(
                f"{tc.BOLD.value}{tc.YELLOW.value}{self.name}{tc.RESET.value} has received {tc.BOLD.value}{tc.YELLOW.value}{self.nb_received_messages}{tc.RESET.value} messages:"
            )
        for i in range(self.nb_received_messages):
            print(f'- "{self.received_messages[i]}"')

        if self.nb_sent_messages == 0:
            print(f"{tc.RED.value}{self.name} has no sent messages.{tc.RESET.value}")
        elif self.nb_sent_messages == 1:
            print(
                f"{tc.BOLD.value}{tc.YELLOW.value}{self.name}{tc.RESET.value} has sent {tc.BOLD.value}{tc.YELLOW.value}{self.nb_sent_messages}{tc.RESET.value} message:"
            )
        else:
            print(
                f"{tc.BOLD.value}{tc.YELLOW.value}{self.name}{tc.RESET.value} has sent {tc.BOLD.value}{tc.YELLOW.value}{self.nb_sent_messages}{tc.RESET.value} messages:"
            )
        for i in range(self.nb_sent_messages):
            print(f'- "{self.sent_messages[i]}"')
