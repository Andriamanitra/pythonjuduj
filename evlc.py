import random
from math import log2
from math import ceil

N = 26235947428953663183191
INITIAL_CHAINS = [[1,2,3,5,7], [1,2,3,6,7],
                 [1,2,4,5,7], [1,2,4,6,7],
                 [1,2,4,8,9], [1,2,3,5,10],
                 [1,2,3,6,9], [1,2,4,5,10],
                 [1,2,4,6,10], [1,2,4,8,9],
                 [1,2,3,6,12], [1,2,4,6,12],
                 [1,2,4,8,12], [1,2,4,8,16]]



class Chainlink:
    def __init__(self, ch, p1, p2):
        self.__left = p1
        self.__right = p2
        self.__value = ch[p1] + ch[p2]
    def left(self):
        return self.__left
    def right(self):
        return self.__right
    #def __get__(self):
    #    return self.__value
    def __int__(self):
        return self.__value
    def __mul__(self, other):
        return self.__value * other
    def __add__(self, other):
        return self.__value + other
    def __radd__(self, other):
        return self.__value + other
    def __eq__(self, other):
        return self.__value == other
    def __gt__(self, other):
        return self.__value > other
    def __lt__(self, other):
        return self.__value < other
    def __ge__(self, other):
        return self.__value >= other
    def __le__(self, other):
        return self.__value <= other
    def __str__(self):
        return str(self.__value)

class Chainfinder:
    def __init__(self, ch=[]):
        if not ch:
            self.chain = random.choice(INITIAL_CHAINS)
        else:
            self.chain = ch
            #self.chain = self.repair_chain(self.chain)
            return
        if random.randint(1,5) <= 3:
            i = len(self.chain)-1
            while self.chain[i]*2 <= N:
                self.double()
                i += 1
        self.chain = sorted(self.chain)
        r = random.randint(0,3)
        if r == 0:
            next_el = Chainlink(self.chain, self.last_i(), self.last_i()-1)
        elif r == 1:
            next_el = Chainlink(self.chain, self.last_i(), random.randint(0, self.last_i()))
        elif r == 2:
            halfway = len(self)//2 + 1
            next_el = Chainlink(self.chain, random.randint(0, halfway-1), random.randint(halfway, self.last_i()))
        elif r == 3:
            i = -2
            while self.last() + self.chain[i] > N:
                i -= 1
            next_el = Chainlink(self.chain, self.last_i(), i)
        if next_el <= N and next_el not in self.chain:
            self.add(next_el)
        self.chain = self.repair_chain(self.chain)

    def crossover(self, other):
        r = random.randint(5, len(self)-1)
        child_chain = []
        for i in range(0, r):
            child_chain.append(self.chain[i])
        for i in range(r, len(other)):
            x = other.chain[i].left()
            y = other.chain[i].right()
            child_chain.append(Chainlink(child_chain, x, y))
        child_chain = self.repair_chain(child_chain)
        return Chainfinder(child_chain)

    def mutate(self, x=1):
        mutated_chain = [i for i in self.chain]
        for _ in range(x):
            r = random.randint(3, len(mutated_chain)-1)
            if random.randint(0,1):
                mutated_chain[r] = Chainlink(mutated_chain, r-1, r-2)
                mutated_chain = mutated_chain[:r+1]
            else:
                r2 = random.randint(2, r-1)
                mutated_chain[r] = Chainlink(mutated_chain, len(mutated_chain)-1, r2)
                mutated_chain = mutated_chain[:r+1]
            mutated_chain = self.repair_chain(mutated_chain)
        return Chainfinder(mutated_chain)

    def repair_chain(self, ch):
        ch = [i for i in ch if i <= N]
        ch = sorted(ch)
        while ch[-1] != N:
            for i in range(len(ch)):
                if ch[i]+ch[-1] == N:
                    ch.append(Chainlink(ch, i, len(ch)-1))
                    return ch
            r = random.randint(0,5)
            if r == 0 and ch[-1]*2 <= N:
                while ch[-1]*2 <= N:
                    ch.append(Chainlink(ch, len(ch)-1, len(ch)-1))
            elif r == 1:
                ri = random.randint(0, len(ch)-1)
                if ch[-1]+ch[ri] <= N:
                    ch.append(Chainlink(ch, len(ch)-1, ri))
            else:
                i = -2
                while ch[-1]+ch[i] > N:
                    i -= 1
                ch.append(Chainlink(ch, len(ch)-1, i))
        return ch

    def add(self, x):
        if x not in self.chain:
            self.chain.append(x)
    def double(self):
        self.add(Chainlink(self.chain, self.last_i(), self.last_i()))
    def get_chain(self):
        return [int(i) for i in self.chain]
    def last(self):
        return self.chain[-1]
    def last_i(self):
        return len(self.chain)-1
    def fitness(self):
        return len(self.chain)-1
    def print_chain(self, include_l=False):
        if include_l:
            print("l="+str(self.fitness())+"\n[", end="")
        for link in self.chain[:-1]:
            print(link, end=", ")
        print(str(self.chain[-1])+"]")
    def __len__(self):
        return len(self.chain)
    def __gt__(self, other):
        return self.fitness() < other.fitness()
    def __lt__(self, other):
        return self.fitness() > other.fitness()
    def __ge__(self, other):
        return self.fitness() <= other.fitness()
    def __le__(self, other):
        return self.fitness() >= other.fitness()


def binary_representation(n):
    return bin(n)[2:]


def print_chain(ch):
    print("l("+str(ch[-1])+") = "+str(len(ch)-1) + ":\n" + str(ch))
    #print(binary_representation(ch[-1]))


def print_chain_l(ch):
    print("l("+str(ch[-1])+") = "+str(len(ch)-1))


def binary_method(n):
    chain = [1]
    for bit in binary_representation(n)[1:]: # first "1" needs to be ignored
        # double if "0"
        if bit == "0":
            chain.append(chain[-1]*2)
        # double and add if "1"
        elif bit == "1":
            chain.append(chain[-1]*2)
            chain.append(chain[-1]+1)
    return chain


def modulus_method(n, mod=4):
    intermediates = set()
    chain = set()
    chain.add(n)
    while n > 1:
        intermediates.add(n % mod)
        new_n = n - (n % mod)
        if new_n < mod:
            return sorted(list(set(chain).union(addition_sequence(intermediates))))
        else:
            n = new_n
        chain.add(n)
        while n % 2 == 0:
            if n//2 < mod:
                return sorted(list(set(chain).union(addition_sequence(intermediates))))
            n = n//2
            chain.add(n)


def window_method(n, window_size=4):
# I'm pretty sure this is actually analogous to modulus method
    b = binary_representation(n)
    i = 0
    c = False
    intermediates = []
    chain = []

    while  i < len(b):
        if not c:
            if b[i] == "1":
                j1 = 0+i
                c = True
            if chain:
                chain.append(chain[-1]*2)
        if c and i == j1 + window_size - 1:
            j2 = 0+i
            while b[j2] == "0":
                j2 = j2 - 1
            w = int(b[j1:j2+1], 2)
            intermediates.append(w)

            if not chain:
                chain.append(w)
            else:
                for it in range(j1, j2): chain.append(chain[-1]*2)
                chain.append(chain[-1]+w)
            for it in range(j2, i): chain.append(chain[-1]*2)

            c = False
        i += 1
    if c:
        i -= 1
        j2 = 0+i
        while b[j2] == "0":
            j2 = j2 - 1
        w = int(b[j1:j2+1], 2)
        intermediates.append(w)
        for it in range(j1, j2): chain.append(chain[-1]*2)
        chain.append(chain[-1]+w)
        for it in range(j2, i): chain.append(chain[-1]*2)
    print("Intermediates:")
    print(intermediates)
    print()
    intermediate_sequence = addition_sequence(intermediates)
    chain = sorted(list(set(chain).union(intermediate_sequence)))
    return chain


def number_of_1s(n):
    return binary_representation(n).count("1")


def lower_bound(n):
    return ceil(log2(n) + log2(number_of_1s(n)) - 2.13)


def addition_sequence(x):
    seq = set()
    for n in x:
        for m in binary_method(n):
            seq.add(m)
    return sorted(list(seq))


def verify_chain(n, ch):
    r = True
    if ch[-1] != n:
        print("CHAIN DOES NOT END IN n")
        r = False
    for x in range(len(ch)-1, 1, -1):
        for (i,j) in [(i,j) for i in range(x) for j in range(x)]:
            if ch[i]+ch[j] == ch[x]:
                break
        else:
            print("CHAIN NOT VALID AT INDEX "+str(x))
            r = False
    if ch[1] != 2:
        print("CHAIN NOT VALID AT INDEX 1")
        r = False
    if ch[0] != 1:
        print("CHAIN NOT VALID AT INDEX 0")
        r = False
    return r


def main():
    monsters = []
    gen = 0
    best = 715517
    lbm = 0 # last beneficial mutation
    monster_count = 25
    max_gens_without_improvement = 100
    freak_accidents_per_gen = 2
    darwinization = 10


    for u in range(monster_count):
        monsters.append(Chainfinder())
    print("Spawned "+str(monster_count)+" chainfinder monsters")
    while True:
        alpha = monsters.pop(monsters.index(max(monsters)))
        beta = monsters.pop(monsters.index(max(monsters)))
        omega = monsters.pop(monsters.index(max(monsters)))
        print("Gen #"+str(gen)+", min(l)="+str(alpha.fitness()))
        if alpha.fitness() < best:
            lbm = 0+gen
            best = alpha.fitness()
            if alpha.fitness() < 100:
                alpha.print_chain()
            if not verify_chain(N, alpha.get_chain()):
                raise Exception("evolutionary method is broken")
        monsters.append(alpha)
        monsters.append(beta)
        monsters.append(omega)
        for _ in range(freak_accidents_per_gen):
            monsters.pop(random.randint(0, len(monsters)-1))
        for _ in range(darwinization):
            monsters.pop(monsters.index(min(monsters)))
        monsters.append(alpha.crossover(beta))
        monsters.append(alpha.crossover(random.choice(monsters)))
        monsters.append(alpha.crossover(random.choice(monsters)))
        monsters.append(beta.crossover(random.choice(monsters)))
        monsters.append(beta.crossover(random.choice(monsters)))
        monsters.append(omega.crossover(random.choice(monsters)))
        monsters.append(alpha.mutate())
        monsters.append(alpha.mutate(10))
        monsters.append(beta.mutate())
        monsters.append(omega.mutate())
        while len(monsters) < monster_count:
            monsters.append(Chainfinder())
        gen += 1
        if gen-lbm > max_gens_without_improvement:
            print("reached "+str(max_gens_without_improvement)+
                " generations without improvements, terminating")
            break
    print("\n")
    print("Results with evolutionary:\nl("+str(N)+") =", best)
    chain = binary_method(N)
    if verify_chain(N, chain):
        print("Results with binary method:")
        print_chain_l(chain)
    else:
        raise Exception("binary method is broken")
    chain = modulus_method(N, 8)
    if verify_chain(N, chain):
        print("Results with modulus method:")
        print_chain_l(chain)
    else:
        raise Exception("modulus method is broken")
    print("Lower bound for l("+str(N)+") = "+str(lower_bound(N)))


main()