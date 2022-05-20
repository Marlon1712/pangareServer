import json
import logging
import os
import sys
import time
from datetime import datetime

import pyautogui

from src.predicao.resultados import resultadoFinal
from src.predicao.tratativaPrintOriginal import tratar
from src.predicao.verificaGarrafaTeste import detectaVerificacaoTestes
from src.utils.navega import popup, tela_contador, tela_gteste, tela_info, tela_login_uip, uip
from src.utils.printaTela import captura

parametro = ""
for param in sys.argv:
    parametro = param

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False

# Diretorios:
path_atividadeFaltante = "./src/img/grfTeste/atividadeFaltando.png"
path_ImagemProcessada = "./src/img/processada/"
path_imagemOriginal = "./src/img/contadores/contadores.jpg"
path_imagemGTeste = "./src/img/grfTeste/grfTeste.png"
path_Modelo = "./src/models/modelo_rf.pkl"
path_namelog = "./logs/Erros.log"

# Comandos
tecla_uip = "./src/img/comands/inline.png"
tecla_login = "./src/img/comands/loginITF.png"
passw = ["8", "5", "1", "1"]

logging.basicConfig(
    filename=path_namelog,
    encoding="utf8",
    filemode="w",
    level=logging.ERROR,
    format="%(asctime)s file: %(filename)s line: %(lineno)d %(levelname)s -> %(message)s",
    datefmt="%Y-%m-%d %I:%M %p",
)

dicionarioAtividadesGarrafasTeste = {
    "GARRAFAS": [579, 83, 23, 28],
    "FUNDO_OPACO": [579, 115, 23, 28],
    "FUNDO_TRANSPARENT": [579, 147, 23, 28],
    "PAREDE_ENTRADA": [579, 179, 23, 28],
    "PAREDE_SAIDA": [579, 211, 23, 28],
    "BOCA": [579, 243, 23, 28],
    "HF_1": [579, 275, 23, 28],
    "HF_2": [579, 307, 23, 28],
    "IR": [579, 339, 23, 28],
    "COR": [579, 371, 23, 28],
    "CONTORNO": [579, 403, 23, 28],
}


def predicaoGT():
    garrafaTeste = {}
    (
        datagt,
        horagt,
        garrafasProcessadasUltimoTeste,
    ) = detectaVerificacaoTestes(path_imagemGTeste)
    garrafaTeste["DATA_HORA_GFT"] = f"20{datagt[-2:]}-{datagt[-4:-2]}-{datagt[:-4]} {horagt[:2]}:{horagt[2:4]}:00.000"
    dicionarioAtividadesFaltantes = dict(enumerate(pyautogui.locateAllOnScreen(path_atividadeFaltante)))
    # dicionarioAtividadesFaltantes = {}
    if len(dicionarioAtividadesFaltantes) == 0:
        for keyBanco, _ in dicionarioAtividadesGarrafasTeste.items():
            garrafaTeste[keyBanco] = 1
    else:
        for key, value in dicionarioAtividadesFaltantes.items():
            dicionarioAtividadesFaltantes[key] = list(value)
        for (
            keyBanco,
            valueBanco,
        ) in dicionarioAtividadesGarrafasTeste.items():
            if list(valueBanco) in dicionarioAtividadesFaltantes.values():
                garrafaTeste[keyBanco] = 0
            else:
                garrafaTeste[keyBanco] = 1
    garrafaTeste["PROCESSADA_ULTIMO_TESTE"] = garrafasProcessadasUltimoTeste

    return garrafaTeste


def coleta():

    try:

        # janela = os.system('tasklist /fi "imagename eq javaw.exe" /fo csv 2>NUL | find /I "javaw.exe">NUL')
        # os.system("cls" if os.name == "nt" else "clear")

        # if janela != 0:
        #     os.system("./pilot.lnk")
        #     time.sleep(5)
        #     uip()
        #     time.sleep(2)
        #     tela_login_uip(tecla_login, passw)

        # popup()
        # tela_contador()
        # captura(path_imagemOriginal)
        # tela_info()
        # tela_gteste()
        # captura(path_imagemGTeste)

        tratar(path_ImagemProcessada, path_imagemOriginal)
        resultado = resultadoFinal(path_ImagemProcessada, path_Modelo)
        resultadogft = predicaoGT()

        resultado.update(resultadogft)
        resultadojson = json.dumps(resultado)
        print(resultadojson)
    except BaseException as err:
        logging.error(f"{err}")
        # os.system("taskkill /F /im javaw.exe")


if __name__ == "__main__":
    coleta()
