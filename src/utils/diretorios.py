import os
import os.path

from .bcolors import BColors as Bc


def criaDiretorio(caminhoImagemProcessada):
    """
    Função que cria o diretório das imagens processadas
    """
    try:
        os.mkdir(caminhoImagemProcessada)
    except FileExistsError:
        Bc.info(f"[INFO] Pasta: {caminhoImagemProcessada} existe!")
        quantidadeArquivos = len(os.listdir(caminhoImagemProcessada))
        Bc.info(f"[INFO] Numero de arquivos na pasta: {str(quantidadeArquivos)}")


def removeArquivos(caminhoImagemProcessada):
    """
    Função apaga as antigas imagens preprocessadas
    """
    for root, _, files in os.walk(caminhoImagemProcessada):
        for file in files:
            os.path.join(root, file)
            if ".jpg" in file:
                os.remove(caminhoImagemProcessada)
