import enum
from printer import term_colors as tc
from utils import get_inverse
from cryptosystems import ElGamal


class CryptosystemType(enum.Enum):
    ELGAMAL = 0
    RSA = 1


class AttackType(enum.Enum):
    BRUTE_FORCE = 0
    SHANKS_BSGS = 1


class Attacker:
    def __init__(
        self,
        name: str,
        cryptosystem: ElGamal,
        cryptosystem_type: CryptosystemType = CryptosystemType.ELGAMAL,
        attack_type: AttackType = AttackType.BRUTE_FORCE,
        debug: bool = False,
    ):
        self.name = name

        self.attacks = [self.brute_force, self.shanks_bsgs]
        self.nb_attacks = len(self.attacks)

        self.attack_names = ["Brute Force", "Shanks Baby-Step Giant-Step"]
        self.cs_names = ["ElGamal", "RSA"]
        self.attack_type = attack_type

        self.cs = cryptosystem
        self.cs_type = cryptosystem_type.value
        self.visible_users = [user for user in self.cs.users if user != self.name]
        self.intercepted_messages = []
        self.debug = debug

    def intercept_message(self, attack_type: AttackType, debug: bool = False) -> list:
        (dst, (src, message)) = self.cs.message_queue[-1]
        if self.debug or debug:
            print(
                f"Intercepting message for {tc.BOLD.value}{tc.YELLOW.value}{dst}{tc.RESET.value} from {tc.BOLD.value}{tc.YELLOW.value}{src}{tc.RESET.value} using {tc.BOLD.value}{tc.BLUE.value}{self.attack_names[attack_type.value]}{tc.RESET.value} attack..."
            )

        sks, found = [], -1
        p, g = self.cs.p, self.cs.g
        for t in message:
            if attack_type.value < self.nb_attacks:
                found = self.attacks[attack_type.value](p, g, t[0])
            else:
                print(f"{tc.RED.value}Invalid attack type!{tc.RESET.value}")

            if found != -1:
                sks.append(found)
            else:
                print(f"{tc.RED.value}Couldn't find the result!{tc.RESET.value}")

        if self.debug or debug:
            print(
                f"{tc.BOLD.value}{tc.RED.value}Secret keys{tc.RESET.value} of {tc.BOLD.value}{tc.YELLOW.value}{src}{tc.RESET.value} used for encrypting message sent to {tc.BOLD.value}{tc.YELLOW.value}{dst}{tc.RESET.value}: {sks}"
            )

        # Decrypt the message

        return sks

    def brute_force(self, p: int, g: int, b: int) -> int:
        """
        Solve the Discrete Logarithm using the Brute Force method.

        Returns:
        --------
        int
            The result of the attack.
        """
        if self.debug:
            print(
                f"Solving {tc.GREEN.value}Discrete Logarithm{tc.RESET.value} using {tc.BLUE.value}{tc.BOLD.value}Brute Force{tc.RESET.value} method"
            )

        for i in range(1, p):
            if g**i % p == b:
                return i
        return -1

    def shanks_bsgs(self, p: int, g: int, b: int) -> int:
        """
        Solve the Discrete Logarithm using the Shanks Baby-Step Giant-Step method.

        Returns:
        --------
        int
            The result of the attack.
        """
        if self.debug:
            print(
                f"Solving {tc.GREEN.value}Discrete Logarithm{tc.RESET.value} using {tc.BLUE.value}{tc.BOLD.value}Shanks Baby-Step Giant-Step{tc.RESET.value} method"
            )
        n = int(p**0.5) + 1
        baby_steps = [(g**i) % p for i in range(n)]

        # Precompute g^(-n)
        g_inv_n = get_inverse(g**n, p)

        # Compute and verify each value (optimization)
        for j in range(n):
            y = (b * (g_inv_n**j)) % p
            if y in baby_steps:
                i = baby_steps.index(y)
                return i + j * n
        return -1

    # def intercept_message(
    #     self,
    #     attacker: str,
    #     victim: str,
    #     encrypted: tuple,
    #     attack_type: int = AttackType.BRUTE_FORCE,
    #     debug: bool = False,
    # ) -> tuple:
    #     """
    #     Intercept a message from a sender to a receiver.

    #     Parameters:
    #     -----------
    #     attacker : str
    #         The attacker's name.
    #     encrypted : list
    #         The encrypted message.
    #     attack_type : int, optional
    #         The type of attack, by default AttackType.BRUTE_FORCE

    #     Returns:
    #     --------
    #     tuple
    #         The decrypted message.
    #     """

    #     if self.debug or debug:
    #         print(
    #             f"Intercepting message ({tc.BOLD.value}c1{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{encrypted[0]}{tc.RESET.value}, {tc.BOLD.value}c2{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{encrypted[1]}{tc.RESET.value}) for {attacker}...",
    #             end=" ",
    #         )

    #     # Get all the secret keys used to encrypt the message via bruteforce
    #     sks = self.attack(attack_type, encrypted)
    #     print(f"Secret keys hacked: {sks}")

    def __str__(self):
        str = ""
        str += f"{tc.BOLD.value}Attacker {tc.RED.value}{self.name}{tc.RESET.value} is currently intercepting the traffic on the "
        str += f"{tc.BOLD.value}{tc.BLUE.value}{self.cs_names[self.cs_type]}{tc.RESET.value} "
        str += f"({tc.BOLD.value}p{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{self.cs.p}{tc.RESET.value}, {tc.BOLD.value}g{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{self.cs.g}{tc.RESET.value})"
        str += " network.\n"
        str += f"Visible Users:\n"
        for user in self.visible_users:
            str += f"- {tc.BOLD.value}{tc.YELLOW.value}{user.name}{tc.RESET.value}: {tc.BOLD.value}pk{tc.RESET.value}={tc.BOLD.value}{tc.BLUE.value}{self.cs.get_user_pk(user.name)}{tc.RESET.value}\n"
        return str
