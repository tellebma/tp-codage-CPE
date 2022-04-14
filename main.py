"""
Main TP codage.
"""
import matplotlib.pyplot as plt
from scipy.stats import entropy
from dahuffman import HuffmanCodec
import numpy as np
import random

from codageCanal import *


def getLivre(livrePath) -> str:
    with open(livrePath) as file:
        data = file.read()
    return data


def getAlphabet(phrasePasse) -> dict:
    alphabet = dict()
    # parcour des lettres de la phrase.
    for lettre in phrasePasse:
        if lettre in alphabet:  # la lettre est-elle déjà présente dans l'alphabet ?0
            alphabet[lettre] += 1  # oui, on incrémente.
        else:
            alphabet[lettre] = 1  # non, je l'initialise.
    # trie de la liste par ordre décroissant.
    alphabet = {k: v for k, v in sorted(alphabet.items(), key=lambda item: item[1], reverse=True)}
    return alphabet


def getFrequence(alphabet) -> dict:
    total = 0
    for val in alphabet.values():
        total += val
    for key, value in alphabet.items():
        alphabet[key] = value / total
    return alphabet


def entropie(alphabet) -> int:
    return entropy(list(alphabet.values()), base=2)


def byteToBin(byte_array):
    """
    From ByteArray to Binary:
    :return:
    """
    return ''.join(format(byte, '08b') for byte in byte_array)


def binToByte(binary):
    return int(binary, 2).to_bytes((len(binary) + 7) // 8, byteorder='big')


def reshape(array, k: int = 4):
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
    bourrage = k - (len(array) % k)
    if bourrage == k: bourrage = 0
    array = np.append(array, ['0' for i in range(0, bourrage)])
    x = len(array) // k
    return bourrage, np.reshape(array, (x, k))


def addErrorToArray(array):
    """
    Ajoute des erreurs dans le tableau
    Simulation d'un canal de transmission.
    :param array:np.array
    :return: array np.array
    """
    array_error = []
    for e in array:
        r = random.randint(0, len(e) - 1)
        e[r] = 1 - int(e[r])
        array_error.append(e)

    return np.array(array_error)


def reformat_array_to_bin(array, bourrage):
    # supprimer le shape
    array = np.reshape(array, array.size)

    # avec bourrage
    for index in range(bourrage):
        array = np.delete(array, len(array) - 1)

    # apres suppression bourrage
    str_bin = ''.join(array.astype(str))
    return str_bin


def showDecodedMessage(array, bourrage):
    binary_error = reformat_array_to_bin(array, bourrage)
    byte_array_rebuilt = binToByte(binary_error)
    liste_decode = huffman.decode(byte_array_rebuilt)
    return ''.join(liste_decode)


class Graph:
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
    def __init__(self, alphabet, liste_phrase_generique, phraseList):
        self.alphabet = alphabet
        self.liste_phrase_generique = liste_phrase_generique
        self.phraseList = phraseList

    def codec(self):
        return HuffmanCodec.from_data(self.liste_phrase_generique)

    def encode(self):
        return self.codec().encode(self.phraseList)

    def decode(self, byte_array):
        return self.codec().decode(byte_array)


if __name__ == '__main__':

    G = Graph()

    phrase = getLivre('./The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt')
    # phrase = getLivre('./livre.txt')
    alphabet = getAlphabet(phrase)
    # print(f"phrase={phrase}")
    # print(f"alphabet={alphabet}")
    # graph:
    # G.barplot(alphabet)

    new_alphabet = getFrequence(alphabet)
    # print(f"new_alphabet={new_alphabet}")

    G.barplot(new_alphabet)

    e = entropie(new_alphabet)
    print(f"Entropie = {e}")  # nb de bit moyen codage.

    # ~~~~~~~~
    # Encodage
    # ~~~~~~~~

    liste_phrase_generique = list(phrase)

    # ~~~~~~~~~~
    # Pour réduire le temps d'exec
    phrase = phrase  # prend les 200 premier char.
    # ~~~~~~~~~~

    # print(f"liste_phrase={liste_phrase_generique}")

    # sentence = "This is a beautiful day !"
    # liste_phrase = list(sentence)
    liste_phrase = list(phrase)
    huffman = Huffman(new_alphabet, liste_phrase_generique, liste_phrase)
    ret = huffman.encode()
    # print(f"encodage={ret}")
    liste_bin = byteToBin(ret)  # phrase en binaire.

    # print(f"Phrase             : {''.join(liste_phrase)}")
    # print(f"Phrase en binaire  : {liste_bin}")

    codec = HuffmanCodec.from_data(getLivre('./The_Adventures_of_Sherlock_Holmes_A_Scandal_In_Bohemia.txt'))
    print(codec.print_code_table())

    np_bin = np.array(list(liste_bin))
    # print(f"np_bin = {type(np_bin)}")
    # print(f"np_bin = {np_bin!r}")

    k, n = (4, 7)  # EDIT

    bourrage, nouveau_message_code = reshape(np_bin, k)

    # sans codageCanal:
    print(f"matric message :{nouveau_message_code[0:4]}")
    # on affiche seulement les 4 premiers ca ne sert a rien d'etre spammé inutilement.

    ####
    # INTEGRERE Codage Canal
    ####

    cc = CodageCanal(k, n)
    # genpoly => 1101b sert a generer le message codé. avec redondance codagecanal.
    # fec_cycle constructeur codage canal [block.FECCyclic(genpoly)]
    genpoly, fec_cycle = cc.genpoly()
    print(f"Polynome généré : {genpoly}")

    nouveau_message_code_codage_canal = cc.codageCanal(nouveau_message_code,
                                                       fec_cycle)  # génère le message avec la redondance.
    # print(nouveau_message_code)

    ####
    # FIN INTEGRERE Codage Canal
    ####

    # ~~~~
    # Ajout erreur
    # ~~~~

    # Ajout des erreurs dans les messages.
    array_error = nouveau_message_code
    array_error_codage_canal = nouveau_message_code_codage_canal
    # To edit.
    nombre_erreur = 1  # test avec x nombres d'erreurs ajouté dans le code.
    for i in range(0, nombre_erreur):
        # Ajout des erreurs dans les messages.
        array_error = addErrorToArray(array_error)
        array_error_codage_canal = addErrorToArray(array_error_codage_canal)

    ###
    # DECODAGE CANAL
    ###
    array_error_codage_canal_decode = cc.decodageCanal(array_error_codage_canal, fec_cycle)
    ###
    # Fin DECODAGE CANAL
    ###

    # ~~~~~~
    # Decode huffman
    # ~~~~~~

    message_decode = showDecodedMessage(array_error, bourrage)
    message_decode_codage_canal = showDecodedMessage(array_error_codage_canal_decode, bourrage)

    # ~~~~~~~~~~~~~~~~~~~~~~~
    # Interpretation resultat
    # ~~~~~~~~~~~~~~~~~~~~~~~

    backslashN = '\n'  # var mise en forme text

    taux = cc.tauxErreur(phrase, message_decode_codage_canal)
    print("******************")
    print("Avec Codage Canal:")
    print(end="    ")  # useless mise en forme terminal.
    print(f"Message décodé passé par le codage canal: {message_decode_codage_canal[:20].replace(backslashN, '/n')}")
    print(end="    ")
    print(
        f"Il y a eu un taux d'erreur de : {taux['%erreur'] * 100}% et donc un taux de ressemblance de {taux['%ressemblance'] * 100}%")
    # print(end="    ")
    # print(taux,end="\n\n")
    print()

    taux = cc.tauxErreur(phrase, message_decode)
    print("******************")
    print("Sans Codage Canal:")
    print(end="    ")
    print(f"Message décodé: {message_decode[:20].replace(backslashN, '/n')}")
    print(end="    ")
    print(
        f"Il y a eu un taux d'erreur de : {taux['%erreur'] * 100}% et donc un taux de ressemblance de {taux['%ressemblance'] * 100}%")
    print(end="    ")
    # print(taux)
