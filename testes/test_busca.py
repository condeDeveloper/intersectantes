"""A busca conferida contra a forca bruta de verdade, onde ela ainda cabe."""

import unittest
from itertools import combinations
from math import comb

from intersectantes.busca import contar_maximas, listar_maximas, maior_familia
from intersectantes.familias import e_intersectante, subconjuntos


def maior_por_forca_bruta(n, k):
    """O maximo achado olhando TODAS as familias possiveis.

    E 2 elevado ao numero de k-subconjuntos, entao so serve para casos
    minusculos. Mas nao usa poda, nem coloracao, nem ordem: e a definicao.
    """
    conjuntos = subconjuntos(n, k)
    melhor = 0
    for tamanho in range(len(conjuntos), 0, -1):
        for familia in combinations(conjuntos, tamanho):
            if e_intersectante(familia):
                return tamanho
    return melhor


class TestContraForcaBruta(unittest.TestCase):
    def test_casos_pequenos(self):
        for n in range(2, 7):
            for k in range(1, n + 1):
                if comb(n, k) > 15:
                    continue
                self.assertEqual(
                    maior_familia(n, k).tamanho,
                    maior_por_forca_bruta(n, k),
                    "n=%d k=%d" % (n, k),
                )


class TestExemplo(unittest.TestCase):
    def test_o_exemplo_e_valido(self):
        for n in range(2, 9):
            for k in range(1, n + 1):
                if comb(n, k) > 70:
                    continue
                r = maior_familia(n, k)
                self.assertTrue(e_intersectante(r.exemplo), "n=%d k=%d" % (n, k))
                self.assertEqual(len(set(r.exemplo)), r.tamanho, "n=%d k=%d" % (n, k))
                for s in r.exemplo:
                    self.assertEqual(bin(s).count("1"), k)

    def test_nao_da_para_acrescentar_nada_ao_exemplo(self):
        # o maximo e maximal: todo conjunto de fora briga com alguem de dentro
        for n, k in ((5, 2), (6, 3), (7, 3), (8, 3)):
            r = maior_familia(n, k)
            dentro = set(r.exemplo)
            for s in subconjuntos(n, k):
                if s in dentro:
                    continue
                self.assertFalse(
                    e_intersectante(list(dentro) + [s]), "n=%d k=%d s=%d" % (n, k, s)
                )


class TestEnumeracao(unittest.TestCase):
    def test_listar_e_contar_concordam(self):
        for n, k in ((4, 2), (5, 2), (6, 3), (7, 3), (6, 2)):
            tamanho = maior_familia(n, k).tamanho
            self.assertEqual(
                len(listar_maximas(n, k, tamanho)),
                contar_maximas(n, k, tamanho),
                "n=%d k=%d" % (n, k),
            )

    def test_nenhuma_familia_listada_se_repete(self):
        for n, k in ((4, 2), (6, 3), (7, 3)):
            tamanho = maior_familia(n, k).tamanho
            familias = [frozenset(f) for f in listar_maximas(n, k, tamanho)]
            self.assertEqual(len(set(familias)), len(familias), "n=%d k=%d" % (n, k))

    def test_toda_familia_listada_e_intersectante(self):
        for n, k in ((4, 2), (5, 2), (6, 3), (7, 3)):
            tamanho = maior_familia(n, k).tamanho
            for familia in listar_maximas(n, k, tamanho):
                self.assertTrue(e_intersectante(familia), "n=%d k=%d" % (n, k))
                self.assertEqual(len(familia), tamanho)

    def test_contar_tamanho_maior_que_o_maximo_da_zero(self):
        for n, k in ((5, 2), (6, 3), (7, 3)):
            tamanho = maior_familia(n, k).tamanho
            self.assertEqual(contar_maximas(n, k, tamanho + 1), 0, "n=%d k=%d" % (n, k))
