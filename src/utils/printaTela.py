import logging
import os

import pyautogui


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
            pyautogui.screenshot(caminho_print, region=(0, 0, 1025, 762))
            x += 1

    except BaseException as err:
        logging.error(err)
