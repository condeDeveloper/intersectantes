import unittest
from itertools import combinations
from math import comb

from intersectantes.busca import listar_maximas, maior_familia
from intersectantes.familias import (
    e_intersectante,
    estrela,
    para_conjunto,
    quantos_subconjuntos,
    subconjuntos,
)


class TestSubconjuntos(unittest.TestCase):
    def test_quantos_sao(self):
        for n in range(1, 10):
            for k in range(n + 1):
                self.assertEqual(len(subconjuntos(n, k)), comb(n, k), "n=%d k=%d" % (n, k))
                self.assertEqual(quantos_subconjuntos(n, k), comb(n, k))

    def test_cada_um_tem_k_elementos(self):
        for n in range(1, 8):
            for k in range(n + 1):
                for s in subconjuntos(n, k):
                    self.assertEqual(bin(s).count("1"), k)

    def test_nenhum_se_repete(self):
        for n in range(1, 9):
            for k in range(n + 1):
                lista = subconjuntos(n, k)
                self.assertEqual(len(set(lista)), len(lista))

    def test_recusa_k_impossivel(self):
        with self.assertRaises(ValueError):
            subconjuntos(3, 4)
        with self.assertRaises(ValueError):
            subconjuntos(3, -1)

    def test_volta_para_conjunto(self):
        for s in subconjuntos(5, 3):
            self.assertEqual(len(para_conjunto(s, 5)), 3)


class TestIntersectante(unittest.TestCase):
    def test_a_definicao(self):
        n, k = 5, 2
        for tamanho in range(1, 5):
            for familia in combinations(subconjuntos(n, k), tamanho):
                pela_definicao = all(
                    a & b for a, b in combinations(familia, 2)
                )
                self.assertEqual(e_intersectante(familia), bool(pela_definicao))

    def test_familia_de_um_e_sempre_intersectante(self):
        for s in subconjuntos(6, 3):
            self.assertTrue(e_intersectante([s]))

    def test_disjuntos_nao_passam(self):
        self.assertFalse(e_intersectante([0b0011, 0b1100]))


class TestEstrela(unittest.TestCase):
    def test_tamanho_da_estrela(self):
        for n in range(2, 9):
            for k in range(1, n + 1):
                self.assertEqual(len(estrela(n, k, 0)), comb(n - 1, k - 1), "n=%d k=%d" % (n, k))

    def test_a_estrela_e_intersectante(self):
        for n in range(2, 8):
            for k in range(1, n + 1):
                for centro in range(n):
                    self.assertTrue(e_intersectante(estrela(n, k, centro)))

    def test_todo_membro_contem_o_centro(self):
        for centro in range(6):
            for s in estrela(6, 3, centro):
                self.assertTrue(s >> centro & 1)

    def test_a_estrela_atinge_o_maximo_quando_n_passa_de_2k(self):
        for n in range(3, 9):
            for k in range(1, n + 1):
                if n > 2 * k and comb(n, k) <= 60:
                    self.assertEqual(
                        len(estrela(n, k, 0)), maior_familia(n, k).tamanho, "n=%d k=%d" % (n, k)
                    )

    def test_as_maximas_sao_as_estrelas(self):
        for n, k in ((5, 2), (7, 3), (8, 3)):
            tamanho = maior_familia(n, k).tamanho
            familias = [frozenset(f) for f in listar_maximas(n, k, tamanho)]
            estrelas = [frozenset(estrela(n, k, c)) for c in range(n)]
            self.assertEqual(set(familias), set(estrelas), "n=%d k=%d" % (n, k))
