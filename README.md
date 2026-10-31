# Famílias intersectantes e o teorema de Erdős–Ko–Rado

Escolha vários subconjuntos de `k` elementos dentro de `{1, ..., n}`, de modo que
**dois quaisquer tenham elemento em comum**. Quantos cabem?

A resposta óbvia é fixar um elemento e pegar todos os conjuntos que o contêm —
uma **estrela**, com `C(n-1, k-1)` conjuntos. Erdős, Ko e Rado provaram em 1961
que, quando `n ≥ 2k`, não existe nada melhor.

Aqui o teorema não entra no código: a maior família é **achada por busca**, e a
fórmula só aparece depois, como juiz. Python puro, sem dependência nenhuma.

## Os quatro achados

1. **A busca bate com `C(n-1, k-1)` em todos os 35 pares `(n, k)` conferidos**,
   até oito elementos. Abaixo de `n = 2k` o teorema não vale, e a busca mostra o
   porquê: cabem **todos** os `C(n, k)` conjuntos, porque dois k-subconjuntos de
   um conjunto pequeno demais não têm como ser disjuntos.
2. **Quando `n > 2k`, as únicas famílias máximas são as `n` estrelas** — não é
   só o tamanho que o teorema acerta, é a forma. Conferido por enumeração
   completa: em `n=7, k=3` há exatamente 7 famílias de 15 conjuntos, e elas são
   as 7 estrelas, uma por elemento.
3. **No caso apertado `n = 2k` o número de ótimas explode para `2^C(n-1,k-1)`.**
   Medido: 8 famílias com `n=4`, **1.024** com `n=6`. A razão é que os conjuntos
   se emparelham com seus complementos, e basta escolher um de cada par. Para
   `n=8, k=4` a mesma conta daria 34.359.738.368, que a enumeração não alcança —
   e por isso esse número está marcado como previsão, não como medida.
4. **A dificuldade da busca não cresce com o tamanho: ela cresce com a folga.**
   `n=8, k=4` sai em 36 nós; `n=9, k=4`, que é maior mas tem `n` apenas um
   acima de `2k`, custa **1.741.096 nós** — quarenta e oito mil vezes mais.

## As tabelas

Tudo abaixo sai de `python -m ferramentas.medidor`. Nenhum número foi digitado à
mão, e todos estão presos em `testes/test_medidas.py`.

### A busca contra o teorema

| n | k | k-subconjuntos | maior família | C(n−1, k−1) | batem |
|---|---|---|---|---|---|
| 5 | 2 | 10 | 4 | 4 | sim |
| 6 | 3 | 20 | 10 | 10 | sim |
| 7 | 3 | 35 | 15 | 15 | sim |
| 7 | 4 | 35 | 35 | 35 | sim (n < 2k: cabe tudo) |
| 8 | 3 | 56 | 21 | 21 | sim |
| 8 | 4 | 70 | 35 | 35 | sim |
| 8 | 5 | 56 | 56 | 56 | sim (n < 2k: cabe tudo) |

Com `--completo` a tabela vai a nove elementos.

### Quantas famílias atingem o máximo

| n | k | máximo | famílias máximas | n > 2k? | são só as estrelas? |
|---|---|---|---|---|---|
| 4 | 2 | 3 | 8 | não | — |
| 5 | 2 | 4 | 5 | sim | sim |
| 6 | 2 | 5 | 6 | sim | sim |
| 6 | 3 | 10 | 1.024 | não | — |
| 7 | 2 | 6 | 7 | sim | sim |
| 7 | 3 | 15 | 7 | sim | sim |
| 8 | 2 | 7 | 8 | sim | sim |
| 8 | 3 | 21 | 8 | sim | sim |

### O caso apertado, n = 2k

| n | k | famílias máximas | 2^C(n−1, k−1) | bate |
|---|---|---|---|---|
| 4 | 2 | 8 | 8 | sim |
| 6 | 3 | 1.024 | 1.024 | sim |

### Onde a busca sofre

| n | k | nós | relação com 2k |
|---|---|---|---|
| 7 | 3 | 123 | n > 2k |
| 8 | 3 | 64 | n > 2k |
| 8 | 4 | 36 | n = 2k |
| 9 | 3 | 103 | n > 2k |
| 9 | 4 | 1.741.096 | n > 2k, por um |

A linha de `n=9, k=4` só aparece com `--completo`, porque leva dois minutos.

## O que as medidas me corrigiram

- **A primeira busca podava só pelo tamanho e não terminava.** "O que está na
  mão mais o que ainda cabe" não corta nada num grafo **denso**, e o grafo da
  interseção é densíssimo: quase todo par de conjuntos se intersecta. Troquei
  pela poda por **coloração** — vértices da mesma cor nunca entram juntos — e
  `n=8, k=4` caiu de "não termina" para 36 nós.
- **Depois a contagem de famílias máximas travou, pelo motivo oposto.** A poda
  por coloração reordena os candidatos, e com isso a mesma família passou a ser
  encontrada uma vez para cada ordem possível. Enumerar exige **ordem
  crescente**; achar o máximo exige coloração. São duas buscas diferentes, e
  agora são duas funções diferentes.
- **Esperava que a dificuldade acompanhasse o número de conjuntos.** Não
  acompanha: `n=9, k=5` tem 126 conjuntos e sai em 127 nós, enquanto `n=9, k=4`
  tem 126 também e custa 1,7 milhão. O que pesa é a folga entre `n` e `2k`.
- **Achei que `n < 2k` fosse um caso sem graça.** É ele que mostra onde a
  hipótese do teorema está: com `n` pequeno demais, dois k-subconjuntos não
  conseguem ser disjuntos, então a família máxima é o conjunto inteiro de
  `C(n, k)` subconjuntos, e `C(n-1, k-1)` deixa de ser o teto.

## Como está organizado

```
intersectantes/familias.py  os k-subconjuntos como máscaras, e a estrela
intersectantes/busca.py     a busca com poda por coloração e a enumeração canônica
ferramentas/medidor.py      roda tudo e imprime as tabelas acima
testes/                     32 testes
```

A bateria confere a busca contra uma força bruta de verdade — todas as famílias
possíveis, sem poda nenhuma — em todos os casos com até 15 subconjuntos.

## Rodar

```bash
python -m unittest discover -s testes -t . -v   # a bateria inteira
python -m ferramentas.medidor                   # recalcula as tabelas deste README
python -m ferramentas.medidor --completo        # inclui n = 9
```

Sem `pip install`: não há dependência. Precisa de Python 3.11 ou mais novo.

## Licença

MIT.
