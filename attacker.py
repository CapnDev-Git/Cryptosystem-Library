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

        self.visible_users = {user for user in self.cs.users}
        self.intercepted_messages = []
        self.debug = debug

    def actualize_users(self):
        self.visible_users = {user for user in self.cs.users}

    def intercept_message(self, attack_type: AttackType, debug: bool = False) -> list:
        (dst, (src, message)) = self.cs.message_queue[-1]
        if self.debug or debug:
            print(
                f"Intercepting message for {tc.BOLD.value}{tc.YELLOW.value}{dst}{tc.RESET.value} from {tc.BOLD.value}{tc.YELLOW.value}{src}{tc.RESET.value} using {tc.BOLD.value}{tc.BLUE.value}{self.attack_names[attack_type.value]}{tc.RESET.value} attack..."
            )

        receiver_found = -1
        p, g = self.cs.p, self.cs.g
        dst_pk = self.cs.get_user_pk(dst)

        # Find the receiver secret key from its public key
        if attack_type.value < self.nb_attacks:
            receiver_sk = self.attacks[attack_type.value](p, g, dst_pk)
        else:
            print(f"{tc.RED.value}Invalid attack type!{tc.RESET.value}")

        # Decrypt the intercepted message
        decrypted_message = ""
        for c1, c2 in message:
            decrypted_message += chr((c2 * get_inverse(c1**receiver_sk % p, p)) % p)

        if self.debug or debug:
            print(
                f'Message intercepted: {tc.BOLD.value}{tc.YELLOW.value}"{decrypted_message}"{tc.RESET.value}'
            )

        # Add the message to the intercepted messages
        self.intercepted_messages.append((src, dst, decrypted_message))
        return decrypted_message

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

    def __str__(self):
        str = ""
        str += f"{tc.BOLD.value}{tc.RED.value}{self.name}{tc.RESET.value} is currently intercepting the traffic on the "
        str += f"{tc.BOLD.value}{tc.BLUE.value}{self.cs_names[self.cs_type]}{tc.RESET.value} "
        str += f"({tc.BOLD.value}p{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{self.cs.p}{tc.RESET.value}, {tc.BOLD.value}g{tc.RESET.value}={tc.BOLD.value}{tc.YELLOW.value}{self.cs.g}{tc.RESET.value}) network.\n"

        str += f"Visible users by attacker:\n"
        if len(self.visible_users) == 0:
            str += f"{tc.RED.value}No visible users.{tc.RESET.value}\n"
            return str
        for user in self.visible_users:
            str += f" - {tc.BOLD.value}{tc.PURPLE.value}{user.name}{tc.RESET.value}: {tc.BOLD.value}pk{tc.RESET.value}={tc.BOLD.value}{tc.BLUE.value}{self.cs.get_user_pk(user.name)}{tc.RESET.value}\n"
        str += "\n"

        str += "Intercepted messages by attacker:\n"
        if len(self.intercepted_messages) == 0:
            str += f"{tc.RED.value}No intercepted messages.{tc.RESET.value}\n"
            return str
        for src, dst, message in self.intercepted_messages:
            str += f" - {tc.BOLD.value}{tc.PURPLE.value}{src}{tc.RESET.value} -> {tc.BOLD.value}{tc.PURPLE.value}{dst}{tc.RESET.value}: {tc.BOLD.value}{tc.YELLOW.value}{message}{tc.RESET.value}\n"
        return str
