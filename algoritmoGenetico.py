from random import randint, uniform
from time import time
import matplotlib.pyplot as plt


TOLERANCIA =  pow(10,-6)
N_VEZES = 10
CONSISTENCIA = 0.7

def iota(N):
  return range(N)
#gera a população inicial 
def gera_pop_inicial(N,tam_populacao):
    lista_tabuleiros = []
    for _ in range(tam_populacao):
        tab = []
        for _ in range(N):# as posições são geradas automaticamente
            J = randint(0, N-1)
            tab.append(J)
        lista_tabuleiros.append(tab)
    
    return lista_tabuleiros

# calcula o número de ataques entre rainhas
def numero_ataques(T):
    ataques = 0
    for i in range(len(T)-1):
        for r in range(len(T)-1-i):
            j = r+i+1
            if T[i] == T[j] or abs(i-j) == abs(T[i]-T[j]):
                ataques += 1
    
    return ataques


def func_adaptacao(T):
    return 1/(numero_ataques(T)+1)


def roleta(P):
    fitness_list = [func_adaptacao(T) for T in P]
    
    return calcula_roleta(fitness_list)


def calcula_roleta(fitness_list):
    soma = sum(fitness_list)
    prob = [(f/soma) for f in fitness_list]
    acc = 0
    distrib = []
    for p in prob:
        acc += p
        distrib.append(acc)
    
    return distrib

# seleciona uma porcentagem da população a partir da roleta
def selecao(P):
    melhor = None
    melhorImagem = 0
    pior = None
    piorImagem = 2
    media = 0
    parents = []
    dist = roleta(P)
    for j in range(len(P)):
        novaImagem = func_adaptacao(P[j])
        media += novaImagem
        if melhor == None or melhorImagem < novaImagem:#atualiza melhor imagem
            melhor = P[j]
            melhorImagem = novaImagem
        if melhor == None or piorImagem > novaImagem:#atualiza pior imagem
            pior = P[j]
            piorImagem = novaImagem

        coin = uniform(0, 1)
        for k in range(len(P)):
            i = len(P) - 1 - k
            if i == 0:
                parents.append(P[0])
            elif coin > dist[i-1]:
                parents.append(P[i])
                break
    
    return (melhor, pior, media/len(P), parents)

#cria filhos
def splicing(T1, T2):
    pontoSplit = randint(1, len(T1)-2)
    crianca1 = T1[:pontoSplit]+T2[pontoSplit:]
    crianca2 = T2[:pontoSplit]+T1[pontoSplit:]
    return [crianca1,crianca2]


def mutacao(T):
  mutado = T.copy()
  pos = randint(0,len(T)-1)
  novo_gene = randint(0,len(T)-2)
  if T[pos] < novo_gene:
    mutado[pos] = novo_gene
  else:
    mutado[pos] = novo_gene+1
  return mutado


def algoritmo_genetico(numeroRainhas,tam_populacao, gen, prob_cross, prob_mut, elit):
  populacao = gera_pop_inicial(numeroRainhas,tam_populacao)
  melhor_fit = []
  media_fit = []
  countMelhor = 0
  ultimoMelhor= None
  for iteracao in range(gen-1):
    melhor,pior, media, selec_pop = selecao(populacao)
    melhor_fit.append(func_adaptacao(melhor))
    media_fit.append(media)
    if 1- func_adaptacao(melhor) <TOLERANCIA:#parada caso a solução foi encontrada
        return (melhor_fit, media_fit, func_adaptacao(melhor), melhor, iteracao, "SOLUÇÃO ENCONTRADA")
    elif abs(func_adaptacao(melhor) - func_adaptacao(pior)) < TOLERANCIA:# parada caso a população esteja homogenea demais
        return (melhor_fit, media_fit, func_adaptacao(melhor), melhor,iteracao,"POPULAÇÃO HOMOGENEA DEMAIS")
    if ultimoMelhor != None and func_adaptacao(melhor)== func_adaptacao(ultimoMelhor):# contagem de estabilidade
        countMelhor+=1
    else:
        ultimoMelhor = melhor
        countMelhor =0

    if countMelhor > 0.1* gen:#parada caso o algoritmo esteja num plato
        return (melhor_fit, media_fit, func_adaptacao(melhor), melhor,iteracao, "ALGORITMO ESTABILIZADO")
    filhos = []
    for i in range(len(selec_pop)//2):#formação dos filhos
      if uniform(0, 1) < prob_cross:
        cross = splicing(selec_pop[2*i], selec_pop[2*i+1])
        filhos += cross
      else:
        filhos += selec_pop[2*i:2*i+2]
    mut_pop = []
    for i in range(len(filhos)):
      if uniform(0, 1) < prob_mut:
        mut = mutacao(filhos[i])
        mut_pop.append(mut)
      else:
        mut_pop.append(filhos[i])
    nova_pop = mut_pop.copy()
    if elit:
      i = randint(0,len(nova_pop)-1)
      nova_pop[i] = melhor
    populacao = nova_pop
  melhor,pior, media, _ = selecao(populacao)
  melhor_fit.append(func_adaptacao(melhor))
  media_fit.append(media)
  return (melhor_fit, media_fit, func_adaptacao(melhor), melhor,iteracao,"MAX ITERAÇÕES")


def add_dado(y, label2=''):
  x = iota(len(y))
  plt.plot(x, y, label=label2)


def termina_dado(eixoY='', titulo=''):
  plt.ylabel(eixoY)
  plt.xlabel('Geração')
  plt.title(titulo)
  plt.show()


def faz_grafico(y, label2='', eixoY='', titulo=''):
  x = iota(len(y))
  plt.plot(x, y, label=label2)
  plt.ylabel(eixoY)
  plt.xlabel('Geração')
  plt.title(titulo)
  #plt.yticks([0,2,4,6])
  plt.legend()
  plt.show()

#executa o algoritmo varias vezes. Caso convirja mais que 70% das vezes, retorna a média de iterações
def testarConsistencia(numeroRainhas,tam_populacao , gen, prob_cross, prob_mut, elit,):
    count = 0
    iteracoes = []
    for _ in range(N_VEZES):
        _,_ , resultado , _,iteracao, _ = algoritmo_genetico(
            numeroRainhas,tam_populacao,  gen, prob_cross, prob_mut, elit)
        if abs(resultado -1) < TOLERANCIA:
            count +=1
            iteracoes.append(iteracao)
    if count/N_VEZES >= CONSISTENCIA:
        print(sum(iteracoes)/len(iteracoes))
    else:
         print("Não consistente")

#executa o algoritmo 10 vezes e plota um gráfico com as médias de adaptabilidade
def executar_ag_10_vezes(numeroRainhas, tam_populacao, gen, prob_cross, prob_mut, elit):
  lista_media = []
  for i in range(10):
    melhores, media,_,_,_ = algoritmo_genetico(
        numeroRainhas,  tam_populacao,gen, prob_cross, prob_mut, elit)
    add_dado(melhores)
    lista_media.append(media)
  termina_dado(eixoY='Fitness', titulo='Melhores')
  for i in range(len(lista_media)):
    add_dado(lista_media[i])
  termina_dado(eixoY='Fitness', titulo='Medias')


# analise 8 rainhas
# com elitismo
executar_ag_10_vezes(8, 100, 100, 0.7, 0.02, True) 
#sem elitismo
executar_ag_10_vezes(8, 100, 100, 0.7, 0.02, False)
# variando tamanho populacional
executar_ag_10_vezes(8, 50, 100, 0.7, 0.02, True) 
executar_ag_10_vezes(8, 200, 100, 0.7, 0.02, True)
#variando número de gerações
executar_ag_10_vezes(8, 100, 50, 0.7, 0.02, True)
executar_ag_10_vezes(8, 100, 200, 0.7, 0.02, True)
#variando probabilidade de crossover
executar_ag_10_vezes(8, 100, 100, 0.5, 0.02, True)
executar_ag_10_vezes(8, 100, 100, 0.9, 0.02, True)
executar_ag_10_vezes(8, 100, 100, 0.95, 0.02, True)
#variando probabilidade de mutação
executar_ag_10_vezes(8, 100, 100, 0.7, 0, True)
executar_ag_10_vezes(8, 100, 100, 0.7, 0.1, True)
executar_ag_10_vezes(8, 100, 100, 0.7, 0.08, True)

# analise 16 rainhas
#com elitismo
executar_ag_10_vezes(16,200,300,0.7,0.02,True)
#sem elitismo 
executar_ag_10_vezes(16,200,300,0.7,0.02,False)
#variando tamanho populacional
executar_ag_10_vezes(16, 100, 300, 0.7, 0.02, True)
executar_ag_10_vezes(16, 400, 300, 0.7, 0.02, True)
#variando número de gerações
executar_ag_10_vezes(16, 200, 150, 0.7, 0.02, True)
executar_ag_10_vezes(16, 200, 600, 0.7, 0.02, True)
#variando probabilidade de crossover
executar_ag_10_vezes(16, 200, 300, 0.9, 0.02, True)
executar_ag_10_vezes(16,200,300,0.2,0.02,True)
#variando probabilidade de mutração
executar_ag_10_vezes(16,200,200,0.7,0.1,True)
executar_ag_10_vezes(16,200,200,0.7,0,True)
