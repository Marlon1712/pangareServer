import cv2
import numpy as np
from PIL import Image
from utils.diretorios import criaDiretorio, removeArquivos


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
        (480, 79 + 4, 114, 32),
        (480, 113 + 4, 114, 32),
        (480, 145 + 4, 114, 32),
        (480, 189 + 4, 114, 32),
        (480, 222 + 4, 114, 32),
        (480, 263 + 4, 114, 32),
        (480, 297 + 4, 114, 32),
        (480, 330 + 4, 114, 32),
        (480, 365 + 4, 114, 32),
    ]

    cortesSegundoEixo = np.full((9), 114, dtype=int)

    sufixosInspetor = [
        "rec_proc",
        "rec_prod",
        "rec_exp",
        "rec_err_ech",
        "rec_err_cap",
        "rec_err_rot",
        "rec_ams_ech",
        "rec_ams_cap",
        "rec_ams_rec",
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
