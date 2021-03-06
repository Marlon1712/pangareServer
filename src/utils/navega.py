import logging
import time

import pyautogui

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False

# diretorio comandos
tela_home = "C:/pangare/src/img/comands/home.png"
tecla_voltar = "C:/pangare/src/img/comands/voltar.png"
tecla_voltar1 = "C:/pangare/src/img/comands/voltar1.png"
tecla_voltar2 = "C:/pangare/src/img/comands/voltar2.png"
tecla_fechar_popup = "C:/pangare/src/img/comands/popup.png"
tecla_fechar_popup1 = "C:/pangare/src/img/comands/popup1.png"
tecla_info = "C:/pangare/src/img/comands/info.png"
tecla_contador = "C:/pangare/src/img/comands/tela_contador.png"
tecla_grfTeste = "C:/pangare/src/img/comands/tela_garafa_teste.png"
tecla_grfTeste1 = "C:/pangare/src/img/comands/tela_garafa_teste1.png"
tecla_selct_uip = "C:/pangare/src/img/comands/inline.png"
tecla_login = "C:/pangare/src/img/comands/login.png"
tecla_login1 = "C:/pangare/src/img/comands/login1.png"
tecla_login2 = "C:/pangare/src/img/comands/login2.png"


def verificaTela():
    try:
        if pyautogui.locateOnScreen(tela_home):
            return True
        else:
            return False
    except BaseException as err:
        logging.error(f"[ERRO]{err}")
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
        logging.error(err)
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
        logging.error(err)
        raise


def tela_contador():
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
        logging.error(err)
        raise


def tela_gteste():
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
        logging.error(err)
        raise


def tela_login_uip(user: str, passw: list):

    try:
        inicio = time.time()
        while True:
            if pyautogui.locateOnScreen(tecla_login):
                pyautogui.click(tecla_login)
            else:
                if pyautogui.locateOnScreen(tecla_login1):
                    pyautogui.click(tecla_login1)
                else:
                    if pyautogui.locateOnScreen(tecla_login2):
                        pyautogui.click(tecla_login2)

            if pyautogui.locateOnScreen(user):
                # Tecla para LOGIN ITF
                pyautogui.click(user)
                # Senha para acesso Administrador do UIP
                pyautogui.press(passw)
                # raise Exception("Tela login nao localizada!")
                break
            fim = time.time()
            if fim - inicio > 10:
                raise ValueError("tela login nao localizado")
    except BaseException as err:
        logging.error(err)
        raise


def uip():
    """Clica na tecla para abrir tela do inspetor e executa o login

    Args:
        user (str): "C:/pangare/src/img/comands/Comand_loginITF.png"
        passw (list): ["7", "5", "1", "1"]

    Raises:
        Exception: Retorna uma exceção caso não encontre a tecla do inspetor ou login
    """
    try:
        if pyautogui.locateOnScreen(tecla_selct_uip):
            pyautogui.doubleClick(tecla_selct_uip)
        else:
            raise Exception("Tela UIP nao localizada!")
    except BaseException as err:
        logging.error(err)
        raise
