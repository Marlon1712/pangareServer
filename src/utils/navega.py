import logging
import os

import pyautogui

from utils.bcolors import BColors as Bc

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

# diretorio comandos
tecla_voltar = "./src/comands/Comand_voltar.png"
tecla_voltar1 = "./src/comands/Comand_voltar1.png"
tecla_voltar2 = "./src/comands/Comand_voltar2.png"


def verificaTela(image):
    try:
        if pyautogui.locateOnScreen(image):
            return True
        else:
            return False
    except BaseException as err:
        logging.error(f"[ERRO]{err}")
        Bc.warging(f"[WARN] {err=}")
        raise


def voltar():
    """Clique na tecla voltar

    Raises:
        Exception: Retorna uma exceção caso não encontre a imagem da tecla
    """
    try:
        if pyautogui.locateOnScreen(tecla_voltar):
            pyautogui.click(tecla_voltar)
        else:
            if pyautogui.locateOnScreen(tecla_voltar1):
                pyautogui.click(tecla_voltar1)
            else:
                if pyautogui.locateOnScreen(tecla_voltar2):
                    pyautogui.click(tecla_voltar2)
                else:
                    raise Exception("Tecla voltar nao localizada!")
    except BaseException as err:
        logging.error(err)
        Bc.warging(f"[WARN] {err=}")
        raise


def popup():
    """Clica na tecla para fechar popup"""
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_msg.png"):
            pyautogui.click("./src/comands/Comand_msg.png")
        else:
            if pyautogui.locateOnScreen("./src/comands/Comand_msg1.png"):
                pyautogui.click("./src/comands/Comand_msg1.png")

    except BaseException as err:
        logging.error(f"[WARN] {err}")
        Bc.warging(f"[WARN] {err}")
        raise


def info():
    """Clica na tecla para abrir tela info

    Raises:
        Exception: Retorna uma exceção caso não encontre a imagem da tecla
    """
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_info1.png"):
            pyautogui.click("./src/comands/Comand_info1.png")
        else:
            raise Exception("Tela info nao localizada!")
    except BaseException as err:
        logging.error(f"[WARN] {err}")
        Bc.warging(f"[WARN] {err}")
        raise


def contador():
    """Clica na tecla para abrir tela contador de garrafas e executa a funcao

    Raises:
        Exception: Retorna uma exceção caso não encontre a imagem da tecla
    """
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_tela_contador.png"):
            pyautogui.click("./src/comands/Comand_tela_contador.png")
        else:
            raise Exception("Tela contador nao localizada!")
    except BaseException as err:
        logging.error(f"[ERROR] {err}")
        Bc.warging(f"[WARN] {err}")
        raise


def gteste(func):
    """Abre tela de teste de garrafas e executa a funcao


    Raises:
        Exception: Retorna uma exceção caso não encontre tecla de teste
        Exception: Retorna uma exceção caso nao encntre tecla historico garrafa teste
    """
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_tela_garafa_teste.png"):
            pyautogui.click("./src/comands/Comand_tela_garafa_teste.png")
            if pyautogui.locateOnScreen("./src/comands/Comand_tela_garafa_teste1.png"):
                pyautogui.click("./src/comands/Comand_tela_garafa_teste1.png")
            else:
                raise Exception("Tela historico garrafa teste nao localizada!")
        else:
            raise Exception("Tela garrafa teste nao localizada!")

    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        Bc.warging(f"[WARN] Erro ao obter resultado garrafa teste {err}")
        raise


def login(user: str, passw: list):
    if pyautogui.locateOnScreen(user):
        # Tecla para LOGIN ITF
        pyautogui.click(user)
        # Senha para acesso Administrador do UIP
        pyautogui.press(passw)
    else:
        raise Exception("Tecla login ITF nao localizada!")


def uip(user, passw):
    """Clica na tecla para abrir tela do inspetor e executa o login

    Args:
        user (str): "./src/comands/Comand_loginITF.png"
        passw (list): ["7", "5", "1", "1"]

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
    """
    try:
        if pyautogui.locateOnScreen("./src/comands/Comand_inline.png"):
            pyautogui.doubleClick("./src/comands/Comand_inline.png")
            Bc.info("[INFO] Tela da UIP aberta com sucesso!")

            for _ in range(3):  # Clicando na porta para ter acesso ao login

                if pyautogui.locateOnScreen("./src/comands/Comand_login.png"):
                    pyautogui.click("./src/comands/Comand_login.png")
                    login(user, passw)
                    break
                else:
                    if pyautogui.locateOnScreen("./src/comands/Comand_login1.png"):
                        pyautogui.click("./src/comands/Comand_login1.png")
                        login(user, passw)
                        break
                    else:
                        if pyautogui.locateOnScreen("./src/comands/Comand_login2.png"):
                            pyautogui.click("./src/comands/Comand_login2.png")
                            login(user, passw)
                            break
                        else:
                            raise Exception("Tecla login nao localizada!")
        else:
            raise Exception("Tela UIP nao localizada!")
    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        Bc.warging(f"[WARN] {err}")
        os.system("taskkill /im javaw.exe")
