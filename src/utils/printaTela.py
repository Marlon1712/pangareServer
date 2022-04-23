import os

import pyautogui

from .bcolors import error, succes


def captura(caminho_print: str):
    """Metodo para capturar a tela e salvar em um arquivo.

    Args:
        caminho_print (str): Caminho para salvar a tela.
    """
    x = 1
    try:
        if os.path.isfile(caminho_print):
            os.remove(caminho_print)

        while x < 2:
            pyautogui.screenshot(caminho_print)
            x += 1

        succes("IMAGEM capturada!")
    except BaseException as err:
        error(f"Unexpected {err=}, {type(err)=}")
