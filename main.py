"""
Main TP codage.
"""
import matplotlib.pyplot as plt
from scipy.stats import entropy
from dahuffman import HuffmanCodec
import numpy as np
import random


def getLivre(livrePath) -> str:
    with open(livrePath) as file:
        data = file.read()
    return data

def getAlphabet(phrasePasse) -> dict:
    alphabet = dict()
    # parcour des lettres de la phrase.
    for lettre in phrasePasse:
        if lettre in alphabet:# la lettre est-elle déjà présente dans l'alphabet ?0
            alphabet[lettre] += 1# oui, on incrémente.
        else:
            alphabet[lettre] = 1# non, je l'initialise.
    #trie de la liste par ordre décroissant.
    alphabet = {k: v for k, v in sorted(alphabet.items(), key=lambda item: item[1], reverse=True)}
    return alphabet

def getFrequence(alphabet)-> dict:
    total = 0
    for val in alphabet.values():
        total += val
    for key,value in alphabet.items():
        alphabet[key] = value/total
    return alphabet

def entropie(alphabet) -> int:
    return entropy(list(alphabet.values()),base=2)

def byteToBin(byte_array):
    """
    From ByteArray to Binary:
    :return:
    """
    return ''.join(format(byte, '08b') for byte in byte_array)

def binToByte(binary):
    return int(binary, 2).to_bytes((len(binary) + 7) // 8, byteorder='big')

def reshape(array,k:int=4):
    """
    Met sous un format donnée
    [0,0,0,0,0,0,0,0] avec k=2
    [[0,0],
    [0,0],
    [0,0],
    [0,0]]
    NB: Si le nombre n'est pas divisible par k alors des bit de bourrage seront rajouté a la fin.

    :param array:
    :param k:
    :return:
    """
    bourrage = k-(len(array)%k)
    if bourrage == k:bourrage = 0
    array = np.append(array,['0' for i in range(0,bourrage)])
    x = len(array) // k
    return bourrage, np.reshape(array,(x,k))

def addErrorToArray(array):
    """
    Ajoute des erreurs dans le tableau
    Simulation d'un canal de transmission.
    :param array:np.array
    :return: array np.array
    """
    array_error = []
    for e in array:
        r = random.randint(0,len(e)-1)
        e[r]= 1 - int(e[r])
        array_error.append(e)

    return np.array(array_error)

def reformat_array_to_bin(array,bourrage):
    #supprimer le shape
    array = np.reshape(array,array.size)

    #avec bourrage
    for index in range(bourrage):
        array = np.delete(array, len(array)-1)
    #apres suppression bourrage

    str_bin = ''.join(array)
    return str_bin






class Graph():
    def __init__(self):
        pass

    def barplot(self, alphabet: dict) -> None:
        """
        Affiche le tableau de bar avec les valeur et nom du dictionnaire passé en param.
        :param alphabet: dict
        :return: None
        """
        plt.bar(alphabet.keys(), alphabet.values())
        plt.show()

class Huffman():
    def __init__(self,alphabet,liste_phrase_generique,phraseList):
        self.alphabet = alphabet
        self.liste_phrase_generique = liste_phrase_generique
        self.phraseList = phraseList

    def codec(self):
        return HuffmanCodec.from_data(self.liste_phrase_generique)


    def encode(self):
        return self.codec().encode(self.phraseList)


    def decode(self,byte_array):
        return self.codec().decode(byte_array)

if __name__ == '__main__':
    G = Graph()

    phrase = getLivre('./The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt')
    #phrase = getLivre('./livre.txt')
    alphabet = getAlphabet(phrase)
    # print(f"phrase={phrase}")
    #print(f"alphabet={alphabet}")
    #graph:
    #G.barplot(alphabet)

    new_alphabet = getFrequence(alphabet)
    #print(f"new_alphabet={new_alphabet}")

    G.barplot(new_alphabet)

    e = entropie(new_alphabet)
    #print(f"Entropie = {e}")

    #~~~~~~~~
    #Encodage
    #~~~~~~~~

    liste_phrase_generique = list(phrase)
    #print(f"liste_phrase={liste_phrase_generique}")

    sentence = "This is a beautiful day !"
    liste_phrase = list(sentence)
    huffman = Huffman(new_alphabet,liste_phrase_generique,liste_phrase)
    ret = huffman.encode()
    print(f"encodage={ret}")
    liste_bin = byteToBin(ret)#phrase en binaire.

    print(f"Phrase             : {''.join(liste_phrase)}")
    print(f"Phrase en binaire  : {liste_bin}")

    codec = HuffmanCodec.from_data(getLivre('./The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt'))
    #print(codec.print_code_table())

    np_bin = np.array(list(liste_bin))
    #print(f"np_bin = {type(np_bin)}")
    #print(f"np_bin = {np_bin!r}")

    k = 4 # EDIT

    bourrage, new_array = reshape(np_bin,k)

    #print(new_array)
    array_error = addErrorToArray(new_array)
    #print(array_error)

    #~~~~~~
    #Decode
    #~~~~~~


    binary_error = reformat_array_to_bin(array_error,bourrage)
    byte_array_rebuilt = binToByte(binary_error)
    liste_decode = huffman.decode(byte_array_rebuilt)
    message_decode = ''.join(liste_decode)
    print(f"Message décodé     : {message_decode}")




