import ast

import numpy as np


def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


# Função de ativação
def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))


def sigmoid_derivada(sig):
    return sig * (1 - sig)


def lista_binaria(param):
    direcao = param[0]
    # return [valmap(direcao, 1, 4, 0, 1)]

    if direcao == 1:
        return [1, 0]
    elif direcao == 2:
        return [0, 1]
    elif direcao == 3:
        return [0, 0]
    elif direcao == 4:
        return [1, 1]


entradas = np.array([])
saidas = np.array([])

# Loading the data for training
with open('rn_data', 'r', encoding='utf-8') as rn_data:
    for line in rn_data:
        rn_data_array = ast.literal_eval(line)

        entradas = np.array([item[0:-1] for item in rn_data_array])
        for item in entradas:
            item[0] = valmap(item[0], 0, 500, 0, 1)

        saidas = np.array([lista_binaria(item[-1:]) for item in rn_data_array])

# Definição dos pesos de cada camada e, consequentemente, 
# o número de neurônios em cada camada

modo_treino = True
num_entradas = 4
num_camada_oculta = 3
num_saidas = 2
taxaAprendizagem = 0.1
momentum = 1
epocas = 1_000_000

pesos0 = 2 * np.random.random((num_entradas, num_camada_oculta)) - 1
pesos1 = 2 * np.random.random((num_camada_oculta, num_saidas)) - 1

if not modo_treino:
    epocas = 0

mediaAbsoluta = 1


def ativar_rede(valores_entradas, pesos):
    """Ativa a rede e retorna uma lista com as saídas de cada uma das camadas, sendo que a de saída é a primeira
    :rtype: list
    """
    soma_sinapse_0 = np.dot(valores_entradas, pesos[0])
    camada_oculta = sigmoid(soma_sinapse_0)
    soma_sinapse_1 = np.dot(camada_oculta, pesos[1])
    return [sigmoid(soma_sinapse_1), camada_oculta]


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

    derivadaSaida = sigmoid_derivada(camadaSaida)
    deltaSaida = erroCamadaSaida * derivadaSaida

    pesos1Transposta = pesos1.T
    deltaSaidaXPeso = deltaSaida.dot(pesos1Transposta)
    deltaCamadaOculta = deltaSaidaXPeso * sigmoid_derivada(camadaOculta)

    camadaOcultaTransposta = camadaOculta.T
    pesosNovo1 = camadaOcultaTransposta.dot(deltaSaida)
    pesos1 = (pesos1 * momentum) + (pesosNovo1 * taxaAprendizagem)

    camadaEntradaTransposta = camadaEntrada.T
    pesosNovo0 = camadaEntradaTransposta.dot(deltaCamadaOculta)
    pesos0 = (pesos0 * momentum) + (pesosNovo0 * taxaAprendizagem)

# Treinamento finalizado
if modo_treino:
    with open('rn_weights', 'w', encoding='utf-8') as rn_data:
        rn_data.write(str([str(pesos0), str(pesos1)]))

print(pesos0)
print(pesos1)
