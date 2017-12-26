import numpy as np


# Função de ativação
def sigmoid(soma):
    return 1 / (1 + np.exp(-soma))


def sigmoidDerivada(sig):
    return sig * (1 - sig)


# [cor, largura, altura]
entradas = np.array([[0, 0, sigmoid(12.1)],  # R$ 2
                     [1, 0, sigmoid(12.8)],  # R$ 5
                     [1, 0, sigmoid(13.8)],  # R$ 10
                     [2, 0, sigmoid(14.2)],  # R$ 20
                     [2, 1, sigmoid(14.9)],  # R$ 50
                     [0, 1, sigmoid(15.6)]])  # R$ 100

saidas = np.array([[0, 0, 0],  # R$ 2
                   [1, 0, 0],  # R$ 5
                   [0, 1, 0],  # R$ 10
                   [1, 1, 0],  # R$ 20
                   [0, 0, 1],  # R$ 50
                   [1, 0, 1]])  # R$ 100

with open('rn_sensores.txt', 'r', encoding='utf-8') as rn_sensors:
    entradas = np.array(rn_sensors)

with open('rn_outputs.txt', 'r', encoding='utf-8') as rn_saidas:
    saidas = np.array(rn_saidas)

# Definição dos pesos de cada camada e, consequentemente, 
# o número de neurônios em cada camada
pesos0 = 2 * np.random.random((4, 4)) - 1
pesos1 = 2 * np.random.random((4, 1)) - 1

epocas = 300_000
taxaAprendizagem = 0.75
momento = 1
mediaAbsoluta = 1


def ativar_rede(valores_entradas):
    """Ativa a rede e retorna uma lista com as saídas de cada uma das camadas, sendo que a de saída é a primeira
    :rtype: list
    """
    somaSinapse0 = np.dot(valores_entradas, pesos0)
    camadaOculta = sigmoid(somaSinapse0)
    somaSinapse1 = np.dot(camadaOculta, pesos1)
    return [sigmoid(somaSinapse1), camadaOculta]


for j in range(epocas):
    # Cálculo da saída (feedfoward)

    camadaEntrada = entradas

    respostaDaRede = ativar_rede(camadaEntrada)
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
print(camadaSaida)
