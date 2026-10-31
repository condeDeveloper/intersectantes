"""Os k-subconjuntos de {0, ..., n-1}, e o que significa uma familia
intersectante.

Uma familia de conjuntos e INTERSECTANTE quando dois quaisquer dela tem pelo
menos um elemento em comum. A pergunta de Erdos, Ko e Rado, de 1961: qual e a
maior familia intersectante de k-subconjuntos de um conjunto de n elementos?

Cada subconjunto vira uma mascara de bits, e "ter elemento em comum" vira um
`and` diferente de zero. E so isso que a busca precisa saber.
"""

from itertools import combinations
from math import comb


def subconjuntos(n, k):
    """Todos os k-subconjuntos de {0..n-1}, como mascaras de bits."""
    if not 0 <= k <= n:
        raise ValueError("k=%d nao cabe em n=%d" % (k, n))
    return [sum(1 << i for i in grupo) for grupo in combinations(range(n), k)]


def quantos_subconjuntos(n, k):
    """C(n, k), pela formula."""
    return comb(n, k)


def e_intersectante(familia):
    """Dois quaisquer da familia tem elemento em comum?"""
    lista = list(familia)
    for i, a in enumerate(lista):
        for b in lista[i + 1 :]:
            if not a & b:
                return False
    return True


def estrela(n, k, centro):
    """A familia de todos os k-subconjuntos que contem `centro`.

    E a construcao obvia, e e ela que o teorema diz ser otima quando n > 2k:
    todo mundo contem o mesmo elemento, entao todo mundo se intersecta.
    """
    bit = 1 << centro
    return [s for s in subconjuntos(n, k) if s & bit]


def para_conjunto(mascara, n):
    """A mascara de volta como conjunto de inteiros."""
    return {i for i in range(n) if mascara >> i & 1}
