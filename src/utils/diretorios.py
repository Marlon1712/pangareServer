import os
import os.path


def criaDiretorio(caminhoImagemProcessada):
    """
    Função que cria o diretório das imagens processadas
    """
    try:
        os.mkdir(caminhoImagemProcessada)
    except FileExistsError:
        pass


def removeArquivos(caminhoImagemProcessada):
    """
    Função apaga as antigas imagens preprocessadas
    """
    for root, _, files in os.walk(caminhoImagemProcessada):
        for file in files:
            os.path.join(root, file)
            if ".jpg" in file:
                os.remove(caminhoImagemProcessada)
