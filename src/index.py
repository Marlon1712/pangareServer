import logging
import os
import time

import pyautogui

from predicao.resultados import resultadoFinal
from predicao.tratativaPrintOriginal import tratar
from predicao.verificaGarrafaTeste import detectaVerificacaoTestes
from utils.bcolors import BColors as Bc
from utils.navega import contador, gteste, info, popup, uip, verificaTela
from utils.printaTela import captura

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

passw = ["7", "5", "1", "1"]

# Diretorios:
path_atividadeFaltante = "./src/img/garrafasTeste/atividadeFaltando.png"
path_ImagemProcessada = "./src/img/ImgProcess/"
path_imagemOriginal = "./src/img/Print/print.jpg"
path_imagemGTeste = "./src/img/Print/printGrfTeste.png"
path_Modelo = "./src/models/modelo_rf.pkl"
path_namelog = "./logs/Erros.log"

logging.basicConfig(
    filename=path_namelog,
    encoding="utf8",
    level=logging.ERROR,
    format="%(asctime)s file: %(filename)s line: %(lineno)d %(levelname)s -> %(message)s",
    datefmt="%Y-%m-%d %I:%M %p",
)

dicionarioAtividadesGarrafasTeste = {
    "Garrafas_de_Teste": [579, 83, 23, 28],
    "Controlador_do_Fundo": [579, 115, 23, 28],
    "Cont_Fundo_Erro_Transp": [579, 147, 23, 28],
    "Paredes_laterais_entrada": [579, 179, 23, 28],
    "Paredes_laterais_saida": [579, 211, 23, 28],
    "Controlad_Embocadura": [579, 243, 23, 28],
    "Liquido_residual_HF_1": [579, 275, 23, 28],
    "Liquido_residual_HF_2": [579, 307, 23, 28],
    "Liquido_residual_IR": [579, 339, 23, 28],
    "Cor_recipiente_incorreta": [579, 371, 23, 28],
    "Controlo_ext1_entrada": [579, 403, 23, 28],
}


def predicaoGT():
    captura(path_imagemGTeste)
    dicionarioAtividadesFaltantes = dict(enumerate(pyautogui.locateAllOnScreen(path_atividadeFaltante)))
    todasAtividadesFaltantes = {}
    if len(dicionarioAtividadesFaltantes) == 0:
        Bc.info("[INFO] Todas as atividades de garrafas teste foram realizadas")
        for keyBanco, _ in dicionarioAtividadesGarrafasTeste.items():
            todasAtividadesFaltantes[keyBanco] = 1
    else:
        for key, value in dicionarioAtividadesFaltantes.items():
            dicionarioAtividadesFaltantes[key] = list(value)
        for (
            keyBanco,
            valueBanco,
        ) in dicionarioAtividadesGarrafasTeste.items():
            if list(valueBanco) in dicionarioAtividadesFaltantes.values():
                todasAtividadesFaltantes[keyBanco] = 0
            else:
                todasAtividadesFaltantes[keyBanco] = 1

    Bc.succes("[INFO] IMAGEM Garrafa teste capturada!")
    info()
    (
        datagt,
        horagt,
        garrafasProcessadasUltimoTeste,
    ) = detectaVerificacaoTestes(path_imagemGTeste)

    dataHoraGarrafaTeste = f"20{datagt[-2:]}-{datagt[-4:-2]}-{datagt[:-4]} {horagt[:2]}:{horagt[2:4]}:00.000"
    Bc.succes("[INFO] Prevendo os resultados e escrevendo nos bancos de dados !")
    resultadoFinal(
        path_ImagemProcessada,
        path_Modelo,
        dataHoraGarrafaTeste,
        garrafasProcessadasUltimoTeste,
        todasAtividadesFaltantes,
    )


def coleta():
    try:
        os_cmd = 'tasklist /fi "imagename eq javaw.exe" /fo csv 2>NUL | find /I "javaw.exe">NUL'
        os.system("cls" if os.name == "nt" else "clear")

        if os.system(os_cmd) != 0:
            Bc.info("[INFO] Abrindo Pilot !")
            pyautogui.hotkey("win", "1")
            time.sleep(5)

            uip()

            contador()
            Bc.info("[INFO] Capturando a tela para predição numérica!")
            captura(path_imagemOriginal)
            Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
            tratar(path_ImagemProcessada, path_imagemOriginal)
            gteste()
        else:
            Bc.info("[INFO] Programa esta Aberto!")
            if verificaTela("./src/img/comands/Comand_inline.png") is True:
                uip("./src/img/comands/Comand_loginITF.png", passw)
                popup()
                contador()
                Bc.info("[INFO] Capturando a tela para predição numérica!")
                captura(path_imagemOriginal)
                Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
                tratar(path_ImagemProcessada, path_imagemOriginal)
                gteste()
                predicaoGT()
            else:
                info()
                popup()
                contador()
                Bc.info("[INFO] Capturando a tela para predição numérica!")
                captura(path_imagemOriginal)
                Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
                tratar(path_ImagemProcessada, path_imagemOriginal)
                gteste()
                predicaoGT()
    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        os.system("taskkill /im javaw.exe")
        Bc.warging(f"[WARN] Erro ao iniciar rotina {err}")
        Bc.info("[INFO] Pilot foi fechado!")
        raise
