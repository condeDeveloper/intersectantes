"""A busca: a maior familia intersectante, achada sem usar o teorema.

Montar a familia um conjunto de cada vez, sempre mantendo a propriedade. Em
termos de grafo: os k-subconjuntos sao os vertices, dois sao ligados quando se
intersectam, e a maior familia intersectante e a maior CLIQUE desse grafo.

A primeira versao podava so pelo tamanho - "o que esta na mao mais o que ainda
cabe" - e nao terminava nem com oito elementos. O grafo aqui e DENSO: quase
todos os pares se intersectam, entao "o que ainda cabe" quase nunca corta nada.

A poda que funciona e por COLORACAO: pintar os candidatos de modo que vizinhos
nao repitam cor da um limite superior para a clique que ainda pode sair dali,
porque dois vertices da mesma cor nunca entram juntos. Trocar uma poda pela
outra derrubou n = 8, k = 4 de "nao termina" para menos de um segundo.

Nenhuma informacao do teorema de Erdos-Ko-Rado entra aqui.
"""

from .familias import subconjuntos


def _vizinhos(conjuntos):
    """Para cada conjunto, a mascara dos indices que se intersectam com ele."""
    viz = []
    for a in conjuntos:
        marca = 0
        for j, b in enumerate(conjuntos):
            if a & b:
                marca |= 1 << j
        viz.append(marca)
    return viz


def _colorir(candidatos, viz):
    """Ordena os candidatos por cor e devolve [(indice, limite)] crescente.

    O limite de um vertice e o numero da cor dele: se ele entrar na clique, a
    clique nao pode passar desse numero a partir dali. Percorrendo a lista de
    tras para frente, o primeiro limite que nao serve corta o resto todo.
    """
    ordem = []
    restantes = candidatos
    cor = 0
    while restantes:
        cor += 1
        disponiveis = restantes
        while disponiveis:
            bit = disponiveis & -disponiveis
            indice = bit.bit_length() - 1
            disponiveis &= ~viz[indice] & ~bit
            restantes -= bit
            ordem.append((indice, cor))
    return ordem


class Resultado:
    def __init__(self, n, k, tamanho, exemplo, nos):
        self.n = n
        self.k = k
        self.tamanho = tamanho
        self.exemplo = exemplo
        self.nos = nos


def maior_familia(n, k):
    """O tamanho da maior familia intersectante, e um exemplo dela."""
    conjuntos = subconjuntos(n, k)
    if not conjuntos:
        return Resultado(n, k, 0, [], 0)
    viz = _vizinhos(conjuntos)
    melhor = [0]
    exemplo = [[]]
    nos = [0]

    def crescer(atual, candidatos):
        nos[0] += 1
        if not candidatos:
            if len(atual) > melhor[0]:
                melhor[0] = len(atual)
                exemplo[0] = list(atual)
            return
        for indice, limite in reversed(_colorir(candidatos, viz)):
            if len(atual) + limite <= melhor[0]:
                return
            bit = 1 << indice
            atual.append(conjuntos[indice])
            crescer(atual, candidatos & viz[indice] & ~bit)
            atual.pop()
            candidatos &= ~bit

    crescer([], (1 << len(conjuntos)) - 1)
    return Resultado(n, k, melhor[0], exemplo[0], nos[0])


def _enumerar(n, k, tamanho, guardar):
    """Percorre as familias de `tamanho` em ORDEM CRESCENTE de indice.

    A ordem crescente e o que torna a enumeracao canonica: sem ela a mesma
    familia aparece uma vez para cada ordem em que os conjuntos poderiam ter
    entrado, e a busca estoura. A poda por coloracao, que serve para achar o
    maximo, nao serve aqui: ela reordena os candidatos.
    """
    conjuntos = subconjuntos(n, k)
    viz = _vizinhos(conjuntos)
    total = len(conjuntos)

    def crescer(atual, candidatos, quantos):
        if quantos == tamanho:
            guardar(atual)
            return
        if quantos + bin(candidatos).count("1") < tamanho:
            return
        resto = candidatos
        while resto:
            bit = resto & -resto
            indice = bit.bit_length() - 1
            resto -= bit
            if quantos + bin(resto).count("1") + 1 < tamanho:
                return
            atual.append(indice)
            crescer(atual, resto & viz[indice], quantos + 1)
            atual.pop()

    crescer([], (1 << total) - 1, 0)


def contar_maximas(n, k, tamanho):
    """Quantas familias intersectantes DIFERENTES atingem `tamanho`."""
    quantas = [0]

    def contar(_):
        quantas[0] += 1

    _enumerar(n, k, tamanho, contar)
    return quantas[0]


def listar_maximas(n, k, tamanho):
    """As familias que atingem `tamanho`, cada uma como lista de mascaras."""
    conjuntos = subconjuntos(n, k)
    saida = []
    _enumerar(n, k, tamanho, lambda atual: saida.append([conjuntos[i] for i in atual]))
    return saida
