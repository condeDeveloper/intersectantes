"""Os numeros do README, presos."""

import unittest
from math import comb

from intersectantes.busca import contar_maximas, listar_maximas, maior_familia
from intersectantes.familias import e_intersectante, estrela


class TestBuscaContraOTeorema(unittest.TestCase):
    def test_todo_caso_ate_oito(self):
        conferidos = 0
        for n in range(2, 9):
            for k in range(1, n + 1):
                if comb(n, k) > 130:
                    continue
                conferidos += 1
                esperado = comb(n - 1, k - 1) if n >= 2 * k else comb(n, k)
                r = maior_familia(n, k)
                self.assertEqual(r.tamanho, esperado, "n=%d k=%d" % (n, k))
                self.assertTrue(e_intersectante(r.exemplo), "n=%d k=%d" % (n, k))
                self.assertEqual(len(r.exemplo), r.tamanho)
        self.assertEqual(conferidos, 35)

    def test_abaixo_de_2k_cabe_todo_mundo(self):
        for n in range(2, 9):
            for k in range(1, n + 1):
                if n < 2 * k:
                    self.assertEqual(maior_familia(n, k).tamanho, comb(n, k), "n=%d k=%d" % (n, k))

    def test_alguns_maximos_de_cabeca(self):
        esperado = {
            (5, 2): 4, (6, 3): 10, (7, 3): 15, (8, 3): 21,
            (7, 4): 35, (8, 4): 35, (8, 5): 56,
        }
        for (n, k), tamanho in esperado.items():
            self.assertEqual(maior_familia(n, k).tamanho, tamanho, "n=%d k=%d" % (n, k))


class TestQuantasMaximas(unittest.TestCase):
    def test_quando_n_passa_de_2k_sao_exatamente_n(self):
        for n in range(3, 9):
            for k in range(2, min(n, 5) + 1):
                if comb(n, k) > 60 or n <= 2 * k:
                    continue
                tamanho = maior_familia(n, k).tamanho
                self.assertEqual(contar_maximas(n, k, tamanho), n, "n=%d k=%d" % (n, k))

    def test_quando_n_e_menor_que_2k_so_ha_uma(self):
        for n, k in ((4, 3), (5, 3), (5, 4), (6, 4), (6, 5), (7, 4), (7, 5)):
            tamanho = maior_familia(n, k).tamanho
            self.assertEqual(contar_maximas(n, k, tamanho), 1, "n=%d k=%d" % (n, k))

    def test_a_tabela_inteira(self):
        esperado = {
            (3, 2): 1, (4, 2): 8, (5, 2): 5, (6, 2): 6, (7, 2): 7, (8, 2): 8,
            (4, 3): 1, (5, 3): 1, (6, 3): 1024, (7, 3): 7, (8, 3): 8,
            (5, 4): 1, (6, 4): 1, (7, 4): 1,
        }
        for (n, k), quantas in esperado.items():
            tamanho = maior_familia(n, k).tamanho
            self.assertEqual(contar_maximas(n, k, tamanho), quantas, "n=%d k=%d" % (n, k))


class TestCasoApertado(unittest.TestCase):
    def test_n_igual_a_2k_segue_a_potencia_de_dois(self):
        for k in (2, 3):
            n = 2 * k
            tamanho = maior_familia(n, k).tamanho
            self.assertEqual(contar_maximas(n, k, tamanho), 2 ** comb(n - 1, k - 1), "k=%d" % k)

    def test_o_maximo_e_metade_dos_conjuntos(self):
        for k in (2, 3, 4):
            n = 2 * k
            self.assertEqual(maior_familia(n, k).tamanho, comb(n, k) // 2, "k=%d" % k)

    def test_a_familia_pega_um_de_cada_par_complementar(self):
        for k in (2, 3):
            n = 2 * k
            tamanho = maior_familia(n, k).tamanho
            cheio = (1 << n) - 1
            for familia in listar_maximas(n, k, tamanho)[:40]:
                for s in familia:
                    self.assertNotIn(cheio ^ s, familia, "n=%d k=%d" % (n, k))

    def test_a_previsao_para_oito_e_quatro(self):
        self.assertEqual(2 ** comb(7, 3), 34359738368)


class TestCustoDaBusca(unittest.TestCase):
    def test_os_nos_medidos(self):
        esperado = {(7, 3): 123, (8, 3): 64, (8, 4): 36}
        for (n, k), nos in esperado.items():
            self.assertEqual(maior_familia(n, k).nos, nos, "n=%d k=%d" % (n, k))

    def test_a_estrela_de_cada_centro_tem_o_mesmo_tamanho(self):
        for n in range(2, 9):
            for k in range(1, n + 1):
                tamanhos = {len(estrela(n, k, c)) for c in range(n)}
                self.assertEqual(len(tamanhos), 1, "n=%d k=%d" % (n, k))
