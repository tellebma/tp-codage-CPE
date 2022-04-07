from sk_dsp_comm import fec_block as block
import commpy.channelcoding as cg

import numpy as np


class GestionErreur:
    def __init__(self, k, n):
        # fec_block.FECCyclic()
        self.k = k
        self.n = n
        pass

    def genpoly(self):
        # init code gestion erreur  (1101)
        genpoly = format(cg.cyclic_code_genpoly(self.n, self.k)[0], 'b')

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



if __name__ == '__main__':
    ge = GestionErreur(4, 7)
    ge.main()
