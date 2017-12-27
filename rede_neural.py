import ast

import numpy as np


def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


# Função de ativação
def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))


def sigmoidDerivada(sig):
    return sig * (1 - sig)


modo_treino = False
entradas = np.array([])
saidas = np.array([])


def lista_binaria(param):
    direcao = param[0]
    if direcao == 1:
        return [1, 0, 0, 0]
    elif direcao == 2:
        return [0, 1, 0, 0]
    elif direcao == 3:
        return [0, 0, 1, 0]
    elif direcao == 4:
        return [0, 0, 0, 1]
    return [0, 0, 0, 1]


# Loading the data for training
with open('rn_data', 'r', encoding='utf-8') as rn_data:
    for line in rn_data:
        rn_data_array = ast.literal_eval(line)

        entradas = np.array([item[0:-1] for item in rn_data_array])
        # entradas = np.array([valmap(item[0], 0, 500, 0, 1) + item[1:-1] for item in entradas])
        for item in entradas:
            item[0] = valmap(item[0], 0, 500, 0, 1)

        saidas = np.array([lista_binaria(item[-1:]) for item in rn_data_array])

# Definição dos pesos de cada camada e, consequentemente, 
# o número de neurônios em cada camada
pesos0 = 2 * np.random.random((4, 6)) - 1
pesos1 = 2 * np.random.random((6, 4)) - 1

epocas = 0
if modo_treino:
    epocas = 300_000

taxaAprendizagem = 0.3
momento = 1
mediaAbsoluta = 1


def ativar_rede(valores_entradas, pesos):
    """Ativa a rede e retorna uma lista com as saídas de cada uma das camadas, sendo que a de saída é a primeira
    :rtype: list
    """
    somaSinapse0 = np.dot(valores_entradas, pesos[0])
    camadaOculta = sigmoid(somaSinapse0)
    somaSinapse1 = np.dot(camadaOculta, pesos[1])
    return [sigmoid(somaSinapse1), camadaOculta]


for j in range(epocas):
    print('Generation {0}'.format(j))
    camadaEntrada = entradas

    # Cálculo da saída (feedfoward)
    respostaDaRede = ativar_rede(camadaEntrada, [pesos0, pesos1])
    camadaOculta = respostaDaRede[1]
    camadaSaida = respostaDaRede[0]

    # Atualização de pesos (backpropagation)

    erroCamadaSaida = saidas - camadaSaida
    mediaAbsoluta = np.mean(np.abs(erroCamadaSaida))
    print("Erro: " + str(mediaAbsoluta))

    derivadaSaida = sigmoidDerivada(camadaSaida)
    deltaSaida = erroCamadaSaida * derivadaSaida

    pesos1Transposta = pesos1.T
    deltaSaidaXPeso = deltaSaida.dot(pesos1Transposta)
    deltaCamadaOculta = deltaSaidaXPeso * sigmoidDerivada(camadaOculta)

    camadaOcultaTransposta = camadaOculta.T
    pesosNovo1 = camadaOcultaTransposta.dot(deltaSaida)
    pesos1 = (pesos1 * momento) + (pesosNovo1 * taxaAprendizagem)

    camadaEntradaTransposta = camadaEntrada.T
    pesosNovo0 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momento) + (pesosNovo0 * taxaAprendizagem)

# Treinamento finalizado
if modo_treino:
    with open('rn_weights', 'w', encoding='utf-8') as rn_data:
        rn_data.write(str([str(pesos0), str(pesos1)]))

print(pesos0)
print(pesos1)
