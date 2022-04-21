import logging
import os
import time

import pyautogui

from utils.bcolors import BColors as Bc
from utils.navega import contador, gteste, info, popup, uip, verificaTela
from utils.printaTela import captura
from visao.resultados import resultadoFinal
from visao.tratativaPrintOriginal import tratar
from visao.verificaGarrafaTeste import detectaVerificacaoTestes

# ---------------Importações para preditiva numérica de rejeição---------------#


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

passw = ["7", "5", "1", "1"]

# Diretorios:
caminhoImagemProcessada = "./src/img/ImgProcess/"
imagemOriginal = "./src/img/Print/print.jpg"
imagemGTeste = "./src/img/printGrfTeste.png"
nomeArquivo = "./src/csv/inline.csv"
caminhoHistorico = "./src/img/Historico/"
caminhoModelo = "./src/models/modelo_rf.pkl"
namelog = "./src/logs/Erros.log"

logging.basicConfig(
    filename=namelog,
    encoding="utf8",
    level=logging.ERROR,
    format="%(asctime)s file: %(filename)s line: %(lineno)d %(levelname)s -> %(message)s",
    datefmt="%Y-%m-%d %I:%M %p",
)


def predicaoGT():
    dicionarioAtividadesGarrafasTesteUIP1 = {
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
    captura(imagemGTeste)
    dicionarioAtividadesFaltantes = dict(
        enumerate(pyautogui.locateAllOnScreen("./src/img/garrafasTeste/atividadeFaltando.png"))
    )
    todasAtividadesFaltantes = {}
    if len(dicionarioAtividadesFaltantes) == 0:
        Bc.info("[INFO] Todas as atividades de garrafas teste foram realizadas")
        for keyBanco, _ in dicionarioAtividadesGarrafasTesteUIP1.items():
            todasAtividadesFaltantes[keyBanco] = 1
    else:
        for key, value in dicionarioAtividadesFaltantes.items():
            dicionarioAtividadesFaltantes[key] = list(value)
        for (
            keyBanco,
            valueBanco,
        ) in dicionarioAtividadesGarrafasTesteUIP1.items():
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
    ) = detectaVerificacaoTestes("./src/img/printGrfTeste.png")

    dataHoraGarrafaTeste = f"20{datagt[-2:]}-{datagt[-4:-2]}-{datagt[:-4]} {horagt[:2]}:{horagt[2:4]}:00.000"
    Bc.succes("[INFO] Prevendo os resultados e escrevendo nos bancos de dados !")
    resultadoFinal(
        caminhoImagemProcessada,
        caminhoModelo,
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
            captura(imagemOriginal)
            Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
            tratar(caminhoImagemProcessada, imagemOriginal)
            gteste()
        else:
            Bc.info("[INFO] Programa esta Aberto!")
            if verificaTela("./src/comands/Comand_inline.png") is True:
                uip("./src/comands/Comand_loginITF.png", passw)
                popup()
                contador()
                Bc.info("[INFO] Capturando a tela para predição numérica!")
                captura(imagemOriginal)
                Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
                tratar(caminhoImagemProcessada, imagemOriginal)
                gteste()
                predicaoGT()
            else:
                info()
                popup()
                contador()
                Bc.info("[INFO] Capturando a tela para predição numérica!")
                captura(imagemOriginal)
                Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
                tratar(caminhoImagemProcessada, imagemOriginal)
                gteste()
                predicaoGT()
    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        os.system("taskkill /im javaw.exe")
        Bc.warging(f"[WARN] Erro ao iniciar rotina {err}")
        Bc.info("[INFO] Pilot foi fechado!")
        raise
