import logging
import os
import time

import pyautogui
from rich.console import Console

from .predicao.resultados import resultadoFinal
from .predicao.tratativaPrintOriginal import tratar
from .predicao.verificaGarrafaTeste import detectaVerificacaoTestes
from .utils.navega import popup, tela_contador, tela_gteste, tela_info, tela_login_uip, uip
from .utils.printaTela import captura

console = Console()

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = False

# Diretorios:
path_atividadeFaltante = "./src/img/grfTeste/atividadeFaltando.png"
path_ImagemProcessada = "./src/img/processada/"
path_imagemOriginal = "./src/img/contadores/contadores.jpg"
path_imagemGTeste = "./src/img/grfTeste/grfTeste.png"
path_Modelo = "./src/models/modelo_rf.pkl"
path_namelog = "./logs/Erros.log"

# Comandos
tecla_uip = "./src/img/comands/inline.png"
tecla_login = "./src/img/comands/loginITF.png"
passw = ["7", "5", "1", "1"]

logging.basicConfig(
    filename=path_namelog,
    encoding="utf8",
    level=logging.ERROR,
    format="%(asctime)s file: %(filename)s line: %(lineno)d %(levelname)s -> %(message)s",
    datefmt="%Y-%m-%d %I:%M %p",
)

dicionarioAtividadesGarrafasTeste = {
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


def predicaoGT(console, st):
    dicionarioAtividadesFaltantes = dict(enumerate(pyautogui.locateAllOnScreen(path_atividadeFaltante)))

    todasAtividadesFaltantes = {}
    if len(dicionarioAtividadesFaltantes) == 0:
        st.update("[bold green]Todas as atividades de garrafas teste foram realizadas][/]")
        for keyBanco, _ in dicionarioAtividadesGarrafasTeste.items():
            todasAtividadesFaltantes[keyBanco] = 1
    else:
        for key, value in dicionarioAtividadesFaltantes.items():
            dicionarioAtividadesFaltantes[key] = list(value)
        for (
            keyBanco,
            valueBanco,
        ) in dicionarioAtividadesGarrafasTeste.items():
            if list(valueBanco) in dicionarioAtividadesFaltantes.values():
                todasAtividadesFaltantes[keyBanco] = 0
            else:
                todasAtividadesFaltantes[keyBanco] = 1
    (
        datagt,
        horagt,
        garrafasProcessadasUltimoTeste,
    ) = detectaVerificacaoTestes(path_imagemGTeste)

    dataHoraGarrafaTeste = f"20{datagt[-2:]}-{datagt[-4:-2]}-{datagt[:-4]} {horagt[:2]}:{horagt[2:4]}:00.000"
    st.update("[bold green]Prevendo os resultados, enviando para IGS e salvando no SQLite![/]")
    resultadoFinal(
        path_ImagemProcessada,
        path_Modelo,
        dataHoraGarrafaTeste,
        garrafasProcessadasUltimoTeste,
        todasAtividadesFaltantes,
        st,
        console,
    )


def coleta(modo="Producao"):

    with console.status(f"[bold green]Programa executando em {modo} Producao![/]"):
        time.sleep(1)
    try:
        start = time.time()
        with console.status("[bold green]Verificando se pilot esta aberto!]/]"):
            os.system("cls" if os.name == "nt" else "clear")
            os_cmd = 'tasklist /fi "imagename eq javaw.exe" /fo csv 2>NUL | find /I "javaw.exe">NUL'

        if os.system(os_cmd) != 0:
            with console.status("[bold green]Abrindo Pilot![/]"):
                # info("Abrindo Pilot !")
                pyautogui.hotkey("win", "1")
                time.sleep(5)

            with console.status("[bold green]Abrindo Pilot![/]") as st:
                uip(console, st)

            with console.status("[bold green]fazendo login![/]"):
                tela_login_uip(tecla_login, passw, console)

            with console.status("[bold green]Verificando Popup aberto![/]"):
                popup(console)

            with console.status("[bold green]Acessando tela contadores![/]"):
                tela_contador(console)

            with console.status("[bold green]Capturando tela contadores![/]") as st:
                # info("Capturando a tela Contadores!")
                captura(path_imagemOriginal, console, st)

            with console.status("[bold green]Voltando para tela principal![/]"):
                tela_info(console)

            with console.status("[bold green]Acessando tela Historico garrafa teste![/]"):
                tela_gteste(console)

            with console.status("[bold green]Capturando tela garrafa teste![/]") as st:
                # info("Capturando a tela Garrafa Teste!")
                captura(path_imagemGTeste, console, st)

            with console.status("[bold green]Realizando tratativas na imagem![/]"):
                # info("Realizando as tratativas e recortes na imagem original!")
                tratar(path_ImagemProcessada, path_imagemOriginal)
            with console.status("[bold green]Prevendo valors garrafa teste![/]") as st:
                predicaoGT(console, st)

            with console.status("[bold green]Voltando para tela principal![/]"):
                tela_info(console)

        else:
            with console.status("[bold green]Pilot Aberto![/]"):
                # info("Programa esta Aberto!")
                pass
            with console.status("[bold green]Verificando Popup aberto![/]"):
                popup(console)

            with console.status("[bold green]Acessando tela contadores![/]"):
                tela_contador(console)

            with console.status("[bold green]Capturando tela contadores![/]") as st:
                # info("Capturando a tela Contadores!")
                captura(path_imagemOriginal, console, st)

            with console.status("[bold green]Voltando para tela principal![/]"):
                tela_info(console)

            with console.status("[bold green]Acessando tela Historico garrafa teste![/]"):
                tela_gteste(console)

            with console.status("[bold green]Capturando tela garrafa teste![/]") as st:
                # info("Capturando a tela Garrafa Teste!")
                captura(path_imagemGTeste, console, st)

            with console.status("[bold green]Realizando tratativas na imagem![/]"):
                # info("Realizando as tratativas e recortes na imagem original!")
                tratar(path_ImagemProcessada, path_imagemOriginal)
            with console.status("[bold green]Prevendo valors garrafa teste![/]") as st:
                predicaoGT(console, st)
            with console.status("[bold green]Voltando para tela principal![/]"):
                tela_info(console)

        final = time.time()
        console.print(f"[bold red]Tempo de execução: [bold green]{round(final - start,2)}[/] segundos")
    except BaseException as err:
        logging.error(f"{err}")
        os.system("taskkill /im javaw.exe")
        console.log(f"[bold red]Erro ao iniciar rotina {err}[/]")
        console.log("[bold red]Pilot foi fechado![/]")


if __name__ == "__main__":
    coleta("[bold red]Dev[/]")
