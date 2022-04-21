import os, sys, os.path
import csv
import pyodbc
import pandas as pd
import numpy as np
from datetime import datetime

def criaDiretorio(caminhoImagemProcessada):
	"""
	Função que cria o diretório das imagens processadas
	"""
	try:
		os.mkdir(caminhoImagemProcessada)
	except FileExistsError:
		print(f'\033[92m[INFO] Pasta: {caminhoImagemProcessada} existe!')
		quantidadeArquivos = len(os.listdir(caminhoImagemProcessada))
		print('\033[92m[INFO] Numero de arquivos na pasta: ' + str(quantidadeArquivos))

def removeArquivos(caminhoImagemProcessada):
	"""
	Função apaga as antigas imagens preprocessadas
	"""
	for root, dirs, files in os.walk(caminhoImagemProcessada):
		for file in files:
			cami = os.path.join(root,file)
			if '.jpg' in file:
				os.remove(caminhoImagemProcessada)	


def moverHistoricoMensalColeta(caminhoGeral, caminhoDestino, caminhoArquivo, nomeArquivo, extensao = '.csv'):    
            

    diretorio = os.listdir(caminhoGeral)
    now = datetime.now()
    dia = str(now.day)
    hora = now.strftime("%H:%M")
    horario = (dia + (">") + hora)
    transferencia = "1>00:0"
    segunda = "31>23:59"
    terceira = "30>23:59"

    def verificaDiretorio(caminhoGeral, diretorio, extensao, caminhoDestino, caminhoArquivo):
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year
        
        if (nomeArquivo in diretorio):
            if(os.path.exists(caminhoDestino) == True):
                sufixo = 'historico' + str(dia) + str(mes) + str(ano) + extensao
                os.rename(caminhoArquivo, caminhoGeral + sufixo)
                shutil.move(caminhoGeral + sufixo, caminhoDestino)
                print("\033[92m[INFO] Feito Transferencia")
        else:
            print("\033[93m[INFO] Transferencia não realizada")

    if horario == transferencia:
        verificaDiretorio(caminhoGeral, diretorio, extensao, caminhoDestino, caminhoArquivo)
    
    elif horario == segunda:
        verificaDiretorio(caminhoGeral, diretorio, extensao, caminhoDestino, caminhoArquivo)    
        
    elif horario == terceira:
        verificaDiretorio(caminhoGeral, diretorio, extensao, caminhoDestino, caminhoArquivo)
    
    else:
        print("\033[93m[INFO] Não foi movido o arquivo .csv para o historico. Somente será movido no ultimo dia do mês.")
    
        

