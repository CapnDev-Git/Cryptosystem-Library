from printer import term_colors as tc

def brute_force(self) -> int:
    if self.debug:
        print(f"Solving {tc.OKGREEN}Discrete Logarithm{tc.RESET} using {tc.BLUE}{tc.BOLD}Brute Force{tc.RESET} method")
    for i in range(1, self.p):
        if self.g ** i % self.p == self.y:
            return i
    return -1

def shanks_bsgs(self) -> int:
    if self.debug:
        print(f"Solving {tc.OKGREEN}Discrete Logarithm{tc.RESET} using {tc.BLUE}{tc.BOLD}Shanks Baby-Step Giant-Step{tc.RESET} method")
    m = int(self.p ** 0.5) + 1
    L1 = [self.g ** i % self.p for i in range(m)]
    L2 = [self.y * self.g ** (-j * m) % self.p for j in range(m)]
    for i in range(m):
        if L1[i] in L2:
            j = L2.index(L1[i])
            return i * m + j
    return -1

def pollard_rho(self) -> int:
    if self.debug:
        print(f"Solving {tc.OKGREEN}Discrete Logarithm{tc.RESET} using {tc.BLUE}{tc.BOLD}Pollard Rho{tc.RESET} method")
    x, y, i = 1, 1, 0
    while i < self.p:
        x = (x * self.g) % self.p
        y = (y * self.y) % self.p
        i += 1
        if x == y:
            return i
    return -1
