import logging
import os
import time

import pyautogui
from utils.BColors import BColors
from utils.printaTela import captura

from resultados import resultadoFinal
from tratativaPrintOriginal import tratar
from verificaGarrafaTeste import detectaVerificacaoTestes

# ---------------Importações para preditiva numérica de rejeição---------------#


pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

# Diretorios:
caminhoImagemProcessada = "./Imagem/ImgProcess/"
imagemOriginal = "./Imagem/Print/print.jpg"
imagemGTeste = "./Imagem/printGrfTeste.png"
nomeArquivo = "./csv/inline.csv"
caminhoHistorico = "./Imagem/Historico/"
caminhoModelo = "./models/modelo_rf.pkl"
equipamentoColunaSQL = "UIP_GRF_01"

caminhoArquivo = "./csv/inline.csv"
caminhoGeral = "./csv/"
caminhoDestino = "./csv/"
nomeArquivoAtual = "inline.csv"


def verificaTela(image):
    try:
        if pyautogui.locateOnScreen(image):
            return True
        else:
            return False
    except BaseException as err:
        logging.error(err)
        BColors.warging(f"[WARN] Unexpected {err=}, {type(err)=}")


def voltar():
    try:
        if pyautogui.locateOnScreen("./comands/Comand_voltar.png"):
            pyautogui.click("./comands/Comand_voltar.png")
        else:
            if pyautogui.locateOnScreen("./comands/Comand_voltar1.png"):
                pyautogui.click("./comands/Comand_voltar1.png")
            else:
                pyautogui.click("./comands/Comand_voltar2.png")
    except BaseException as err:
        logging.error(err)
        BColors.warging(f"[WARN] Unexpected {err=}, {type(err)=}")


def msg():
    try:
        if pyautogui.locateOnScreen("./comands/Comand_msg.png"):
            pyautogui.click("./comands/Comand_msg.png")
        if pyautogui.locateOnScreen("./comands/Comand_msg1.png"):
            pyautogui.click("./comands/Comand_msg1.png")
    except BaseException as err:
        logging.error(f"Mensagem nao localizada {err}")
        BColors.warging(f"[WARN] mensagem nao localizada {err}")


def info():
    try:
        msg()
        if pyautogui.locateOnScreen("./comands/Comand_info1.png"):
            pyautogui.click("./comands/Comand_info1.png")
    except BaseException as err:
        logging.error(f"Erro ao voltar para tela principal {err}")
        BColors.warging(f"[WARN]Erro ao voltar para tela principal {err}")


def contador():
    try:
        msg()
        if pyautogui.locateOnScreen("./comands/Comand_tela_contador.png"):
            pyautogui.click("./comands/Comand_tela_contador.png")
            BColors.ok("[INFO] Capturando a tela para predição numérica!")
            captura(imagemOriginal)
            BColors.ok("[INFO] Realizando as tratativas e recortes na imagem original!")
            tratar(caminhoImagemProcessada, imagemOriginal)
    except BaseException as err:
        logging.error(f"Erro ao acessar tela contadores {err}")
        BColors.warging(f"[WARN] Erro ao acessar tela contadores {err}")

    info()


def gteste():
    try:
        msg()
        if pyautogui.locateOnScreen("./comands/Comand_tela_garafa_teste.png"):
            pyautogui.click("./comands/Comand_tela_garafa_teste.png")

        if pyautogui.locateOnScreen("./comands/Comand_tela_garafa_teste1.png"):
            pyautogui.click("./comands/Comand_tela_garafa_teste1.png")
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
            dicionarioAtividadesFaltantes = dict(
                enumerate(pyautogui.locateAllOnScreen("./img/garrafasTeste/atividadeFaltando.png"))
            )
            todasAtividadesFaltantes = {}
            if len(dicionarioAtividadesFaltantes) == 0:
                BColors.ok("[INFO] Todas as atividades de garrafas teste foram realizadas")
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

            captura(imagemGTeste)
            BColors.ok("[INFO] IMAGEM Garrafa teste capturada!")
            info()
            (
                dataGarrafaTeste,
                horaGarrafaTeste,
                garrafasProcessadasUltimoTeste,
            ) = detectaVerificacaoTestes("./Imagem/printGrfTeste.png")

            dataHoraGarrafaTeste = str(
                str("20")
                + dataGarrafaTeste[-2:]
                + "-"
                + dataGarrafaTeste[-4:-2]
                + "-"
                + dataGarrafaTeste[:-4]
                + " "
                + horaGarrafaTeste[:2]
                + ":"
                + horaGarrafaTeste[2:4]
                + ":00.000"
            )

            BColors.ok("[INFO] Prevendo os resultados e escrevendo nos bancos de dados !")
            resultadoFinal(
                caminhoImagemProcessada,
                imagemOriginal,
                nomeArquivo,
                caminhoHistorico,
                caminhoModelo,
                equipamentoColunaSQL,
                dataHoraGarrafaTeste,
                garrafasProcessadasUltimoTeste,
                todasAtividadesFaltantes,
            )
        else:
            raise Exception("Tela garrafa teste nao localizada")
    except BaseException as err:
        logging.error(f"Erro ao obter resultado garrafa teste {err}")
        BColors.warging(f"[WARN] Erro ao obter resultado garrafa teste {err}")
        # os.system("taskkill /im javaw.exe")


def uip():
    try:
        if pyautogui.locateOnScreen("./comands/Comand_inline.png"):

            if pyautogui.locateOnScreen("./comands/Comand_inline.png"):
                pyautogui.doubleClick("./comands/Comand_inline.png")
                BColors.ok("[INFO] Tela da UIP aberta com sucesso!")
            else:
                BColors.ok("[INFO] Tela do UIP não encontrada!")
                os.system("taskkill /im javaw.exe")
                raise Exception("UIP nao localizada")

            for _ in range(3):  # Clicando na porta para ter acesso ao login
                try:
                    if pyautogui.locateOnScreen("./comands/Comand_login.png"):
                        pyautogui.click("./comands/Comand_login.png")

                        if pyautogui.locateOnScreen("./comands/Comand_login1.png"):
                            pyautogui.click("./comands/Comand_login1.png")
                            break

                        if pyautogui.locateOnScreen("./comands/Comand_login2.png"):
                            pyautogui.click("./comands/Comand_login2.png")
                            break

                    else:
                        BColors.ok("[INFO] Comando nao localizado")
                        msg()

                except BaseException as err:
                    logging.error(f"Erro ao acessar tela de login {err}")
                    BColors.warging(f"[WARN] Erro ao acessar tela de login {err}")

                time.sleep(1)

            pyautogui.click("./comands/Comand_loginITF.png")  # Imagem para nome do LOGIN ITF
            pyautogui.press(["7", "5", "1", "1"])  # Senha para acesso Administrador do UIP
    except BaseException as err:
        logging.error(f"Falha ao identificar inspetor e/ou usuario ITF -> {err}")
        BColors.warging(f"[WARN] Falha ao identificar inspetor e/ou usuario ITF -> {err}")
        os.system("taskkill /im javaw.exe")


def coleta():
    try:
        namelog = "./logs/Erros.log"
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
            BColors.ok("[INFO] Abrindo Pilot !")
            pyautogui.hotkey("win", "1")  # Abrindo Pilot
            time.sleep(5)

            uip()
            contador()
            gteste()

        else:
            BColors.ok("[INFO] Programa esta Aberto!")
            if verificaTela("./comands/Comand_inline.png"):
                uip()
                contador()
                gteste()
            else:
                info()
                contador()
                gteste()
    except BaseException as err:
        logging.error(err)
        BColors.warging(f"[WARN] Erro ao iniciar rotina {err}")
        BColors.ok("[INFO] Pilot foi fechado!")
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

    BColors.ok("[INFO] IMAGEM Garrafa teste capturada!")
    info()
    (
        dataGarrafaTeste,
        horaGarrafaTeste,
        garrafasProcessadasUltimoTeste,
    ) = detectaVerificacaoTestes("./Imagem/printGrfTeste.png")

    dataHoraGarrafaTeste = str(
        str("20")
        + dataGarrafaTeste[-2:]
        + "-"
        + dataGarrafaTeste[-4:-2]
        + "-"
        + dataGarrafaTeste[:-4]
        + " "
        + horaGarrafaTeste[:2]
        + ":"
        + horaGarrafaTeste[2:4]
        + ":00.000"
    )

    BColors.ok("[INFO] Prevendo os resultados e escrevendo nos bancos de dados !")
    resultadoFinal(
        caminhoImagemProcessada,
        imagemOriginal,
        nomeArquivo,
        caminhoHistorico,
        caminhoModelo,
        equipamentoColunaSQL,
        dataHoraGarrafaTeste,
        garrafasProcessadasUltimoTeste,
        todasAtividadesFaltantes,
    )


teste()
