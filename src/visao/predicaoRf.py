import pickle

import cv2

from .preprocessamentoImagem import SimplePreprocessor


def carregaModelo(caminhoModelo):
    """
    Função que carrega o modelo criado
    """
    # carregando o modelo pre treinado
    modelo = pickle.load(open(caminhoModelo, "rb"))
    return modelo


def predicao(caminhoImagem, modelo):
    """
           Função que pega o modelo criado (Random Forest),
    faz a predição e retorna o número recortado
    """

    imagem = cv2.imread(caminhoImagem)

    sp = SimplePreprocessor(32, 32)

    imagem = sp.preprocess(imagem)

    pred = int(modelo.predict([imagem.reshape(3072)]))

    return pred
