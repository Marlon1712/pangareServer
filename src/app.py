import logging
import os
import time

import pyautogui

from utils.bcolors import BColors as Bc
from utils.printaTela import captura
from visao.resultados import resultadoFinal
from visao.tratativaPrintOriginal import tratar
from visao.verificaGarrafaTeste import detectaVerificacaoTestes

# ---------------Importações para preditiva numérica de rejeição---------------#


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

# Diretorios:
caminhoImagemProcessada = "./src/img/ImgProcess/"
imagemOriginal = "./src/img/Print/print.jpg"
imagemGTeste = "./src/img/printGrfTeste.png"
nomeArquivo = "./src/csv/inline.csv"
caminhoHistorico = "./src/img/Historico/"
caminhoModelo = "./src/models/modelo_rf.pkl"


def verificaTela(image):
    try:
        if pyautogui.locateOnScreen(image):
            return True
        else:
            return False
    except BaseException as err:
        logging.error(err)
        Bc.warging(f"[WARN] Unexpected {err=}, {type(err)=}")


def voltar():
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_voltar.png"):
            pyautogui.click("./src/comands/Comand_voltar.png")
        else:
            if pyautogui.locateOnScreen("./src/comands/Comand_voltar1.png"):
                pyautogui.click("./src/comands/Comand_voltar1.png")
            else:
                pyautogui.click("./src/comands/Comand_voltar2.png")
    except BaseException as err:
        logging.error(err)
        Bc.warging(f"[WARN] Unexpected {err=}, {type(err)=}")


def msg():
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_msg.png"):
            pyautogui.click("./src/comands/Comand_msg.png")
        if pyautogui.locateOnScreen("./src/comands/Comand_msg1.png"):
            pyautogui.click("./src/comands/Comand_msg1.png")
    except BaseException as err:
        logging.error(f"Mensagem nao localizada {err}")
        Bc.warging(f"[WARN] mensagem nao localizada {err}")


def info():
    try:
        msg()
        if pyautogui.locateOnScreen("./src/comands/Comand_info1.png"):
            pyautogui.click("./src/comands/Comand_info1.png")
    except BaseException as err:
        logging.error(f"Erro ao voltar para tela principal {err}")
        Bc.warging(f"[WARN]Erro ao voltar para tela principal {err}")


def contador():
    try:
        msg()
        if pyautogui.locateOnScreen("./src/comands/Comand_tela_contador.png"):
            pyautogui.click("./src/comands/Comand_tela_contador.png")
            Bc.info("[INFO] Capturando a tela para predição numérica!")
            captura(imagemOriginal)
            Bc.info("[INFO] Realizando as tratativas e recortes na imagem original!")
            tratar(caminhoImagemProcessada, imagemOriginal)
    except BaseException as err:
        logging.error(f"Erro ao acessar tela contadores {err}")
        Bc.warging(f"[WARN] Erro ao acessar tela contadores {err}")

    info()


def gteste():
    try:
        msg()
        if pyautogui.locateOnScreen("./src/comands/Comand_tela_garafa_teste.png"):
            pyautogui.click("./src/comands/Comand_tela_garafa_teste.png")

        if pyautogui.locateOnScreen("./src/comands/Comand_tela_garafa_teste1.png"):
            pyautogui.click("./src/comands/Comand_tela_garafa_teste1.png")
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
        else:
            raise Exception("Tela garrafa teste nao localizada")
    except BaseException as err:
        logging.error(f"Erro ao obter resultado garrafa teste {err}")
        Bc.warging(f"[WARN] Erro ao obter resultado garrafa teste {err}")
        # os.system("taskkill /im javaw.exe")


def uip():
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_inline.png"):

            if pyautogui.locateOnScreen("./src/comands/Comand_inline.png"):
                pyautogui.doubleClick("./src/comands/Comand_inline.png")
                Bc.info("[INFO] Tela da UIP aberta com sucesso!")
            else:
                Bc.info("[INFO] Tela do UIP não encontrada!")
                os.system("taskkill /im javaw.exe")
                raise Exception("UIP nao localizada")

            for _ in range(3):  # Clicando na porta para ter acesso ao login
                try:
                    if pyautogui.locateOnScreen("./src/comands/Comand_login.png"):
                        pyautogui.click("./src/comands/Comand_login.png")

                        if pyautogui.locateOnScreen("./src/comands/Comand_login1.png"):
                            pyautogui.click("./src/comands/Comand_login1.png")
                            break

                        if pyautogui.locateOnScreen("./src/comands/Comand_login2.png"):
                            pyautogui.click("./src/comands/Comand_login2.png")
                            break

                    else:
                        Bc.info("[INFO] Comando nao localizado")
                        msg()

                except BaseException as err:
                    logging.error(f"Erro ao acessar tela de login {err}")
                    Bc.warging(f"[WARN] Erro ao acessar tela de login {err}")

                time.sleep(1)

            pyautogui.click("./src/comands/Comand_loginITF.png")  # Imagem para nome do LOGIN ITF
            pyautogui.press(["7", "5", "1", "1"])  # Senha para acesso Administrador do UIP
    except BaseException as err:
        logging.error(f"Falha ao identificar inspetor e/ou usuario ITF -> {err}")
        Bc.warging(f"[WARN] Falha ao identificar inspetor e/ou usuario ITF -> {err}")
        os.system("taskkill /im javaw.exe")


def coleta():
    try:
        namelog = "./src/logs/Erros.log"
        logging.basicConfig(
            filename=namelog,
            encoding="utf8",
            level=logging.ERROR,
            format="%(asctime)s file: %(filename)s line: %(lineno)d %(levelname)s -> %(message)s",
            datefmt="%Y-%m-%d %I:%M %p",
        )
        os.system("cls" if os.name == "nt" else "clear")
        os_cmd = 'tasklist /fi "imagename eq javaw.exe" /fo csv 2>NUL | find /I "javaw.exe">NUL'
        if os.system(os_cmd) != 0:
            Bc.info("[INFO] Abrindo Pilot !")
            pyautogui.hotkey("win", "1")  # Abrindo Pilot
            time.sleep(5)

            uip()
            contador()
            gteste()

        else:
            Bc.info("[INFO] Programa esta Aberto!")
            if verificaTela("./src/comands/Comand_inline.png"):
                uip()
                contador()
                gteste()
            else:
                info()
                contador()
                gteste()
    except BaseException as err:
        logging.error(err)
        Bc.warging(f"[WARN] Erro ao iniciar rotina {err}")
        Bc.info("[INFO] Pilot foi fechado!")
        os.system("taskkill /im javaw.exe")


def teste():
    tratar(caminhoImagemProcessada, imagemOriginal)
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

    todasAtividadesFaltantes = {}
    for keyBanco, _ in dicionarioAtividadesGarrafasTesteUIP1.items():
        todasAtividadesFaltantes[keyBanco] = 1

    Bc.succes("[INFO] IMAGEM Garrafa teste capturada!")
    info()
    (
        dgt,
        hgt,
        garrafasProcessadasUltimoTeste,
    ) = detectaVerificacaoTestes("./src/img/printGrfTeste.png")

    dataHoraGarrafaTeste = f"20{dgt[-2:]}-{dgt[-4:-2]}-{dgt[:-4]} {hgt[:2]}:{hgt[2:4]}:00.000"

    Bc.succes("[INFO] Prevendo os resultados e escrevendo nos bancos de dados !")
    resultadoFinal(
        caminhoImagemProcessada,
        caminhoModelo,
        dataHoraGarrafaTeste,
        garrafasProcessadasUltimoTeste,
        todasAtividadesFaltantes,
    )


teste()
