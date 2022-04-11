from sk_dsp_comm import fec_block as block
import commpy.channelcoding as cg
from genpoly import cyclic_code_genpoly
import numpy as np

# https://pysdr.org/content/channel_coding.html

class GestionErreur:
    def __init__(self, k, n):
        # fec_block.FECCyclic()
        self.k = k
        self.n = n
        pass

    def genpoly(self):
        # init code gestion erreur  (1101)
        genpoly = format(cyclic_code_genpoly(self.n, self.k)[0], 'b')

        return genpoly, block.FECCyclic(genpoly)

    def codageCanal(self, matrice, fec_cyclic):
        n_ligne_matrice = len(matrice)
        matrice = np.reshape(matrice, np.size(matrice)).astype(int)
        codewords = fec_cyclic.cyclic_encoder(matrice)
        matrice = np.reshape(codewords, (n_ligne_matrice, self.n))

        return matrice

    def decodageCanal(self,matrice,fec_cyclic):
        n_ligne_matrice = len(matrice)
        matrice = np.reshape(matrice, np.size(matrice))
        decoded_message = fec_cyclic.cyclic_decoder(matrice)
        return np.reshape(decoded_message, (n_ligne_matrice, self.k))

    def tauxErreur(self,phrase_sans_erreur,phrase_erreur):
        tauxDErreur = {"%erreur":0,"%ressemblance":0}
        phrase_sans_erreur = phrase_sans_erreur[:100]
        phrase_erreur = phrase_erreur[:100]
        for i in range(len(phrase_sans_erreur)):
            if phrase_sans_erreur[i] == phrase_erreur[i]:
                # pas d'erreur
                tauxDErreur["%ressemblance"] += 1
            else:
                tauxDErreur["%erreur"] += 1
        tauxDErreur["%ressemblance"] /= len(phrase_sans_erreur)
        tauxDErreur["%erreur"] /= len(phrase_sans_erreur)
        return tauxDErreur

if __name__ == '__main__':
    k = 57
    n = 63
    genpoly = format(cyclic_code_genpoly(n, k)[0], 'b')
    print(genpoly)
