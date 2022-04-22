import os
import pickle

import imutils
from cv2 import cv2
from imutils import contours, paths

from .preprocessamentoImagem import Loader, SimplePreprocessor


def detectaVerificacaoTestes(caminhoPrintTeste):

    # Coletando prints dos displays para obter as imagens:
    # Tirando o print de começo para coletar os números:
    # im = pyautogui.screenshot('./print.jpg') #Armazena o print para cada
    # compilação (LIBERAR QUANDO FOR UTILIZAR)
    im_uso = cv2.imread(caminhoPrintTeste)

    data = im_uso[120:146, 327:504]
    rec_proc = im_uso[248:275, 240:368]

    cv2.imwrite("./src/img/cortes" + "/Data" + ".jpg", data)
    cv2.imwrite("./src/img/cortes" + "/Rec_processados" + ".jpg", rec_proc)

    def recorte(display):  # display = Data ou Rec_processados
        i = 0
        im = cv2.imread("./src/img/cortes/" + str(display) + ".jpg")
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

        # Obtenção dos contornos dos números e ordenação dos mesmos da esquerda
        # para a direita (forma de leitura)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = contours.sort_contours(cnts, method="left-to-right")[0]  # Coloca os cortes na ordem de leitura

        for c in cnts:
            area = cv2.contourArea(c)
            (x, y, w, h) = cv2.boundingRect(c)
            if area > 10:
                if h > 10 and w < 10:
                    num = im[y : y + h, x : x + w]
                    cv2.imwrite("./src/img/numeros/" + str(display) + "/numero_" + str(i) + ".jpg", num)
                    i += 1
                elif h > 8 and w > 13 and w < 16:
                    metade = int(x + w / 2)
                    num1 = im[y - 1 : y + h + 1, x - 1 : metade]
                    num2 = im[y - 1 : y + h + 1, metade : x + w + 1]
                    cv2.imwrite("./src/img/numeros/" + str(display) + "/numero_" + str(i) + ".jpg", num1)
                    i += 1
                    cv2.imwrite("./src/img/numeros/" + str(display) + "/numero_" + str(i) + ".jpg", num2)
                    i += 1

    # Excluindo os números que já tinham sido salvos em outras compilações:
    data = list(paths.list_images("./src/img/numeros/Data"))
    rec_proc = list(paths.list_images("./src/img/numeros/Rec_processados"))

    # Deleta as imagens dos números caso elas existam nas pastas
    for i, _ in enumerate(data):
        if data != []:
            os.remove(data[i])

    for i, _ in enumerate(rec_proc):
        if rec_proc != []:
            os.remove(rec_proc[i])

    # Salvando os números em ordem de cada display:
    recorte("Data")
    recorte("Rec_processados")

    # Carrega o modelo "modelo_knn.pkl" para a variável model
    with open("./src/models/modelo_knn.pkl", "rb") as f:
        model = pickle.load(f)

    caminho = "./src/img/numeros"
    imagePaths = list(paths.list_images(caminho))  # Cria uma lista com todas as imagens presentes nas pastas internas

    # Pré-processamento das imagens para serem preditas pelo KNN
    sp = SimplePreprocessor(32, 32)  # Pré-processamento para 32x32 pixels
    sdl = Loader(preprocessors=[sp])  # Definição da forma de carregamento
    (numeros, displays) = sdl.load_predict(imagePaths)
    numeros = numeros.reshape((numeros.shape[0], 3072))

    Data = []
    Rec_processados = []

    # Separação dos números por display
    for i, _ in enumerate(displays):
        if displays[i] == "Data":
            Data.append(numeros[i])
        if displays[i] == "Rec_processados":
            Rec_processados.append(numeros[i])

    hora_data = model.predict(Data)
    rec_proc = model.predict(Rec_processados)

    num_hora = ""
    num_data = ""
    num_process = ""

    for i, _ in enumerate(hora_data):
        if i < 4:
            num_hora = num_hora + hora_data[i]
        else:
            num_data = num_data + hora_data[i]

    for i, _ in enumerate(rec_proc):
        num_process = num_process + rec_proc[i]

    return str(num_data), str(num_hora), str(num_process)
