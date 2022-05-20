import numpy as np
from cv2 import cv2
from PIL import Image
from src.utils.diretorios import criaDiretorio, removeArquivos


def tratar(caminhoImagemProcessada, imagemOriginal):

    # Função definida para tratar imagem, nessa função são passados os parametros
    # para que recortada a imagem nos quadrantes a serem analizados. Caso suas
    # imagens salvas na pasta ImgProcess estejam sendo recordadas de forma incorreta.
    # No campo dimCrop voçe ira fazer o ajuste necessario.

    criaDiretorio(caminhoImagemProcessada)
    removeArquivos(caminhoImagemProcessada)

    imagemPrintada = cv2.imread(imagemOriginal)

    caixasMaximas = [
        9,
        9,
        9,
        8,
        8,
        8,
        8,
        8,
        8,
    ]  # passando máximo de caixinhas para recorte

    dimensoesCortes = [
        (480, 80 + 4, 114, 28),
        (480, 114 + 4, 114, 28),
        (480, 147 + 4, 114, 28),
        (480, 191 + 4, 114, 28),
        (480, 224 + 4, 114, 28),
        (480, 266 + 4, 114, 28),
        (480, 299 + 4, 114, 28),
        (480, 333 + 4, 114, 28),
        (480, 366 + 4, 114, 28),
    ]

    cortesSegundoEixo = np.full((9), 114, dtype=int)

    sufixosInspetor = [
        "rec_proc",
        "rec_prod",
        "rec_exp",
        "rec_delta_A",
        "rec_delta_B",
        "rec_err_boca",
        "rec_err_parede",
        "rec_err_fundo",
        "rec_err_residual",
    ]

    caminhosImagens = [caminhoImagemProcessada + x for x in sufixosInspetor]

    # Para cada valor, fa o corte da imagem
    for i in range(0, len(dimensoesCortes)):
        corteImagem(
            imagemPrintada,
            dimensoesCortes[i],
            cortesSegundoEixo[i],
            caminhosImagens[i],
            caixasMaximas[i],
        )


def corteImagem(imagem, dimensao, baseX, baseCaminho, max):
    """
    Função destinada a realizar o corte dos quadrantes que foram recortados das imagens
    pela função tratar, assim separando numero a numero para que seja avaliado.
    """

    tipoImagem = ".png"
    # Corta a imagem e salva
    x1, y1, w1, h1 = dimensao
    corteImagem = imagem[y1 : y1 + h1, x1 : x1 + w1]
    im = Image.fromarray(corteImagem)
    im.save(baseCaminho + tipoImagem)

    # Abre a imagem salva
    img = cv2.imread(baseCaminho + tipoImagem)

    i = 1
    while i < max:
        y2, w2, h2 = 0, 15, 26
        x2 = baseX - 14 * i
        crop_img = img[y2 : y2 + h2, x2 : x2 + w2]

        im = Image.fromarray(crop_img)
        im.save(baseCaminho + str(max - i) + tipoImagem)

        i = i + 1
