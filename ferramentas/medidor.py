"""Roda as buscas e imprime as tabelas do README.

    python -m ferramentas.medidor
    python -m ferramentas.medidor --completo   # inclui n = 9, que custa milhoes de nos

Nenhum numero do README foi digitado a mao, e todos estao presos em
testes/test_medidas.py.
"""

import sys
import time
from math import comb

from intersectantes.busca import contar_maximas, listar_maximas, maior_familia
from intersectantes.familias import e_intersectante, estrela, para_conjunto

COMPLETO = "--completo" in sys.argv
ATE_N = 9 if COMPLETO else 8
TETO_DE_CONJUNTOS = 130


def milhar(n):
    return "{:,}".format(n).replace(",", ".")


def previsao_ekr(n, k):
    """O que o teorema diz: C(n-1, k-1) quando n >= 2k, e tudo quando n < 2k."""
    return comb(n - 1, k - 1) if n >= 2 * k else comb(n, k)


def main():
    comeco = time.time()

    print("## A busca contra o teorema\n")
    print("| n | k | k-subconjuntos | maior familia | C(n-1, k-1) | batem | nos da busca |")
    print("|---|---|---|---|---|---|---|")
    for n in range(2, ATE_N + 1):
        for k in range(1, n + 1):
            if comb(n, k) > TETO_DE_CONJUNTOS:
                continue
            r = maior_familia(n, k)
            previsto = previsao_ekr(n, k)
            print(
                "| %d | %d | %s | %d | %d | %s | %s |"
                % (
                    n, k, milhar(comb(n, k)), r.tamanho, previsto,
                    "sim" if r.tamanho == previsto else "NAO", milhar(r.nos),
                )
            )

    print("\n## Quantas familias atingem o maximo\n")
    print("| n | k | maximo | familias maximas | n > 2k? | so as estrelas? |")
    print("|---|---|---|---|---|---|")
    for n in range(3, 9):
        for k in range(2, min(n, 5) + 1):
            if comb(n, k) > 60:
                continue
            r = maior_familia(n, k)
            quantas = contar_maximas(n, k, r.tamanho)
            print(
                "| %d | %d | %d | %s | %s | %s |"
                % (
                    n, k, r.tamanho, milhar(quantas),
                    "sim" if n > 2 * k else "nao",
                    "sim" if quantas == n and n > 2 * k else "-",
                )
            )

    print("\n## O caso apertado, n = 2k\n")
    print("| n | k | familias maximas | 2^C(n-1, k-1) | bate |")
    print("|---|---|---|---|---|")
    for k in (2, 3):
        n = 2 * k
        r = maior_familia(n, k)
        quantas = contar_maximas(n, k, r.tamanho)
        previsto = 2 ** comb(n - 1, k - 1)
        print(
            "| %d | %d | %s | %s | %s |"
            % (n, k, milhar(quantas), milhar(previsto), "sim" if quantas == previsto else "NAO")
        )
    print()
    print("para n = 8 e k = 4 a mesma conta daria %s, que a enumeracao nao alcanca."
          % milhar(2 ** comb(7, 3)))

    print("\n## As estrelas, de perto\n")
    for n, k in ((5, 2), (6, 3), (7, 3)):
        e = estrela(n, k, 0)
        print(
            "n=%d k=%d: a estrela do elemento 0 tem %d conjuntos, e intersectante: %s"
            % (n, k, len(e), e_intersectante(e))
        )
    print()
    familias = listar_maximas(7, 3, maior_familia(7, 3).tamanho)
    print("em n=7, k=3 sao %d familias maximas; a primeira e:" % len(familias))
    for s in familias[0][:5]:
        print("  %s" % sorted(para_conjunto(s, 7)))
    print("  ... (%d ao todo)" % len(familias[0]))

    print("\n## Onde a busca sofre\n")
    print("| n | k | nos | relacao com 2k |")
    print("|---|---|---|---|")
    for n, k in ((7, 3), (8, 3), (8, 4), (9, 3), (9, 4)):
        if n > ATE_N:
            continue
        r = maior_familia(n, k)
        relacao = "n = 2k" if n == 2 * k else ("n > 2k" if n > 2 * k else "n < 2k")
        print("| %d | %d | %s | %s |" % (n, k, milhar(r.nos), relacao))

    print("\n(medido em %.1f s)" % (time.time() - comeco))


if __name__ == "__main__":
    main()
