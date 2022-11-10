from random import random, randint
from math import floor
# NÚMERO DE INDIVÍDUOS
N_INDIVIDUOS = None
# NÚMERO DE PARES DURANTE A FAZE DE REPRODUÇÃO
P_PARES = None
# PARAMETRO QUE CONTROLA O QUÃO PROVAVEL DE SER ALEATÓRIO O SORTEIO DE PARES É
PARAMETRO_SORTEIO = 0.5
# PARAMETRO QUE CONTROLA O QUÃO PROVAVEL É DE UMA MUTAÇÃO OCORRER
PARAMETRO_MUTACAO = 0.5
# MAIOR NÚMERO DE RODADAS QUE UM VALOR ESCOLHIDO COMO MELHOR PODE FICAR INALTERADO ANTES QUE # O ALGORITMO TERMINE
MAX_CONTADOR_MELHOR_VALOR = None
# MAIOR NÚMERO DE ITERAÇÕES POSSÍVEIS DO ALGORITMO
MAX_ITERACOES = None
TOLERANCIA = pow(10, -6)
# GERA UMA POPULAÇÃO INICIAL UNIFORMEMENTE DISTRIBUÍDA PELO DOMÍNIO DO PROBLEMA DAS N-RAINHAS


def gerarPopulacaoInicial(dimensao):
    pass


def roletaProbabilistica():
    pass


def escolhaDeterministica(funcao, populacao):
    pass


def escolhaAleatoria(populacao):
    potencialParents1 = list(range(len(populacao)))
    potencialParents2 = list(range(len(populacao)))
    parents1 = []
    parents2 = []
    for _ in range(P_PARES):
        parents1.append(potencialParents1.pop(
            randint(0, len(potencialParents1) - 1)))
        parents2.append(potencialParents1.pop(
            randint(0, len(potencialParents2) - 1)))
    return parents1, parents2


def coinToss(parametro):
    return True if random() > parametro else False


def splicing(parent1, parent2):
    return parent1[0:floor(len(parent1)/2)] + parent2[floor(len(parent2)/2):]


def gerarFilhos(pais1, pais2):
    filhos = []
    for i in range(P_PARES):
        novo_filho = splicing(pais1[i], pais2[i])
        filhos.append(novo_filho)
    return filhos


def mutacao(populacao):
    pass


def morte(populacao):
    pass


def getMelhorEPiorIndividuo(populacao, funcao):
    melhorIndividuo = None
    piorIndividuo = None
    for individuo in populacao:
        if melhorIndividuo == None and piorIndividuo == None:
            melhorIndividuo = individuo
            piorIndividuo = individuo
        elif funcao(individuo) < funcao(melhorIndividuo):
            melhorIndividuo = individuo
        elif funcao(individuo) > funcao(piorIndividuo):
            piorIndividuo = individuo
    return melhorIndividuo, piorIndividuo


def algoritmoGenetico(funcao, dimensao):
    contadorMelhorValor = 0
    iteracaoAtual = 0
    populacao = gerarPopulacaoInicial(dimensao)
    melhorIndividuoTotal = None
    imagemMelhorIndividuoTotal = None
    while True:
        pais1 = []
        pais2 = []
        if coinToss(PARAMETRO_SORTEIO):
            pais1, pais2 = escolhaAleatoria(populacao)
        else:
            pais1, pais2 = escolhaDeterministica(funcao,  populacao)
        populacao += gerarFilhos(pais1, pais2)
        if coinToss(PARAMETRO_MUTACAO):
            mutacao(populacao)
        morte(populacao)
        melhorIndividuoRodada, piorIndividuoRodada = getMelhorEPiorIndividuo(
            populacao, funcao)

        if (melhorIndividuoTotal == None) or (funcao(melhorIndividuoRodada) < imagemMelhorIndividuoTotal):
            melhorIndividuoTotal = melhorIndividuoRodada
            imagemMelhorIndividuoTotal = funcao(melhorIndividuoTotal)

        if contadorMelhorValor > MAX_CONTADOR_MELHOR_VALOR:
            return melhorIndividuoTotal, "MAX_CONTADOR"
        elif iteracaoAtual > MAX_ITERACOES:
            return melhorIndividuoTotal, "MAX_ITERACOES"
        elif funcao(piorIndividuoRodada) - funcao(melhorIndividuoRodada) < TOLERANCIA:
            return melhorIndividuoTotal, "DIFERENCA_DAS_IMAGENS"
