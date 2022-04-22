import logging
import os

import pyautogui

from .bcolors import info, warging

pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False

# diretorio comandos
verifica_info = "./src/img/comands/Comand_info.png"
tecla_voltar = "./src/img/comands/Comand_voltar.png"
tecla_voltar1 = "./src/img/comands/Comand_voltar1.png"
tecla_voltar2 = "./src/img/comands/Comand_voltar2.png"
tecla_fechar_popup = "./src/img/comands/Comand_msg.png"
tecla_fechar_popup1 = "./src/img/comands/Comand_msg1.png"
tecla_info = "./src/img/comands/Comand_info1.png"
tecla_contador = "./src/img/comands/Comand_tela_contador.png"
tecla_grfTeste = "./src/img/comands/Comand_tela_garafa_teste.png"
tecla_grfTeste1 = "./src/img/comands/Comand_tela_garafa_teste1.png"
tecla_selct_uip = "./src/img/comands/Comand_inline.png"
tecla_login = "./src/img/comands/Comand_login.png"
tecla_login1 = "./src/img/comands/Comand_login1.png"
tecla_login2 = "./src/img/comands/Comand_login2.png"


def verificaTela(image):
    try:
        if pyautogui.locateOnScreen(image):
            return True
        else:
            return False
    except BaseException as err:
        logging.error(f"[ERRO]{err}")
        warging(f"[WARN] {err=}")
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
        warging(f"[WARN] {err=}")
        raise


def popup():
    """Clica na tecla para fechar popup"""
    try:
        if pyautogui.locateOnScreen(tecla_fechar_popup):
            pyautogui.click(tecla_fechar_popup)
        else:
            if pyautogui.locateOnScreen(tecla_fechar_popup1):
                pyautogui.click(tecla_fechar_popup1)

    except BaseException as err:
        logging.error(f"[WARN] {err}")
        warging(f"[WARN] {err}")
        raise


def tela_info():
    """Clica na tecla para abrir tela info

    Raises:
        Exception: Retorna uma exceção caso não encontre a imagem da tecla
    """
    try:
        if pyautogui.locateOnScreen(tecla_info):
            pyautogui.click(tecla_info)
        else:
            raise Exception("Tela info nao localizada!")
    except BaseException as err:
        logging.error(f"[WARN] {err}")
        warging(f"[WARN] {err}")
        raise


def contador():
    """Clica na tecla para abrir tela contador de garrafas e executa a funcao

    Raises:
        Exception: Retorna uma exceção caso não encontre a imagem da tecla
    """
    try:
        if pyautogui.locateOnScreen(tecla_contador):
            pyautogui.click(tecla_contador)
        else:
            raise Exception("Tela contador nao localizada!")
    except BaseException as err:
        logging.error(f"[ERROR] {err}")
        warging(f"[WARN] {err}")
        raise


def gteste():
    """Abre tela de teste de garrafas e executa a funcao


    Raises:
        Exception: Retorna uma exceção caso não encontre tecla de teste
        Exception: Retorna uma exceção caso nao encntre tecla historico garrafa teste
    """
    try:
        if pyautogui.locateOnScreen(tecla_grfTeste):
            pyautogui.click(tecla_grfTeste)
            if pyautogui.locateOnScreen(tecla_grfTeste1):
                pyautogui.click(tecla_grfTeste1)
            else:
                raise Exception("Tela historico garrafa teste nao localizada!")
        else:
            raise Exception("Tela garrafa teste nao localizada!")

    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        warging(f"[WARN] Erro ao obter resultado garrafa teste {err}")
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
        user (str): "./src/img/comands/Comand_loginITF.png"
        passw (list): ["7", "5", "1", "1"]

    Raises:
        Exception: Retorna uma exceção caso não encontre a tecla do inspetor ou login
    """
    try:
        if pyautogui.locateOnScreen(tecla_selct_uip):
            pyautogui.doubleClick(tecla_selct_uip)
            info("[INFO] Tela da UIP aberta com sucesso!")

            for _ in range(3):  # Clicando na porta para ter acesso ao login

                if pyautogui.locateOnScreen(tecla_login):
                    pyautogui.click(tecla_login)
                    login(user, passw)
                    break
                else:
                    if pyautogui.locateOnScreen(tecla_login1):
                        pyautogui.click(tecla_login1)
                        login(user, passw)
                        break
                    else:
                        if pyautogui.locateOnScreen(tecla_login2):
                            pyautogui.click(tecla_login2)
                            login(user, passw)
                            break
                        else:
                            raise Exception("Tecla login nao localizada!")
        else:
            raise Exception("Tela UIP nao localizada!")
    except BaseException as err:
        logging.error(f"[ERRO] {err}")
        warging(f"[WARN] {err}")
        os.system("taskkill /im javaw.exe")
