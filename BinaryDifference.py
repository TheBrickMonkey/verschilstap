import numpy as np # Library, np arrays zijn onderliggend in C geschreven dus sneller dan Python
import matplotlib.pyplot as plt # Library om plots te importen
import networkx as nx  # Library om tijd te besparen met plotten van de (gerichte) graaf

def cyclic_left_shift(n, nrOfBits): # Bit shift naar links, nrOfBits = lengte van de rij zodat de bit shift "cyclisch" werkt
    mask = (1 << nrOfBits) - 1
    return ((n << 1) | (n >> (nrOfBits - 1))) & mask

def cyclic_right_shift(n, nrOfBits): # Onnodige & ongebruikte functie
    mask = (1 << nrOfBits) - 1
    return ((n >> 1) | (n << (nrOfBits - 1))) & mask

def findCycle(startNumber, nrOfBits): # Doet berekeningen door bit-shift en daarna XOR
    visitedNumbers = np.zeros((1,101))
    visitedNumbers[0,0] = startNumber

    for i in range(100):
        original_int = np.uint32(visitedNumbers[0,i])
        shifted_int = cyclic_left_shift(original_int, nrOfBits)
        xor_int = original_int ^ shifted_int # XOR (^) is standaardoperator, (1 0 = 1, 0 1 = 1, 0 0 = 0, 1 1 = 0) (Doet hetzelfde als verschilstap en absolute waarde bij 0 en 1)
        visitedNumbers[0,i+1] = xor_int
    return visitedNumbers

def findCycleLength(arr): # Zoekt de cyclus
    for i in range(100):
        for x in range(i,100):
            slow = arr[0, i]
            fast = arr[0, x] # Gaat over elk getal in de uitkomst om een cyclus te vinden

            if slow == fast and i != x: # Zoekt 2 dezelfde getallen op 2 verschillende plekken
                return arr[0, i:(x+1)] # Pas deze "i" aan naar 0 om de volledige figuur te returnen (met boompjes)

def plotArray(sequences, nrOfBits): #Maak plot van sequence adhv networkx library
    G = nx.DiGraph()

    for sequence in sequences:
        for i in range(len(sequence)):
            sequence[i] = np.binary_repr(int(sequence[i]), width=nrOfBits)
        for i in range(len(sequence) - 1):
            G.add_nodes_from(sequence)
            G.add_edge(sequence[i], sequence[i + 1])

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G, seed=125, k=1, iterations = 10000)  # k = afstand tussen nodes, minder iteraties = snellere weergave, vaak minder overzichtelijk
    nx.draw(G, pos, with_labels=True, node_size=200, node_color="#ffffff", font_size=8, font_color="black",arrows=True)
    plt.axis('off')
    plt.show()

n = 12 # Aantal bits per rij (is nodig om een rij cyclisch te maken zodat laatste-eerste)
start_numbers = [i for i in range(2**n)]
sequences = [] # networkX accepteert moeilijk arrays, daarom nu omgezet in list :(
for start_number in start_numbers:
    cyclus = findCycleLength(findCycle(start_number, n)).tolist()
    sequences.append(cyclus)


plotArray(sequences, n)