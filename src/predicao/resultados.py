from datetime import datetime

from ..services.escritaDados import escreveSQL, printaResultados  # escreveIGS
from .predicaoRf import carregaModelo, predicao

# from src.igs import *


def resultadoFinal(
    caminhoImagemProcessada,
    caminhoModelo,
    dataHoraGarrafaTeste,
    garrafasProcessadasUltimoTeste,
    todasAtividadesFaltantes,
    st,
    console,
):
    """
    Função que recebe as informações e consolida todas elas, salvando as
    predições em um csv e em um banco de dados e printa elas em sequencia
    """
    modelo = carregaModelo(caminhoModelo)
    num_proc, num_prod, num_exp = numerosOitoCaixas(caminhoImagemProcessada, modelo)
    (
        rec_delta_A,
        rec_delta_B,
        rec_err_boca,
        rec_err_parede,
        rec_err_fundo,
        rec_err_residual,
    ) = numeroSeteCaixas(caminhoImagemProcessada, modelo)
    resultadosFinais = [
        num_proc,
        num_prod,
        num_exp,
        rec_delta_A,
        rec_delta_B,
        rec_err_boca,
        rec_err_parede,
        rec_err_fundo,
        rec_err_residual,
    ]
    resultadosFinais = [int(x) for x in resultadosFinais]

    st.update("[bold green]Predição dos dados realizada![/]")

    # variaveis de data e hora
    DataHora = datetime.now()

    # Porcentagem dos números
    # Porcentagens dos números
    porcentagemProcessados = 0 if int(num_proc) == 0 else 100
    porcentagemProduzidos = 0 if int(num_proc) == 0 else round((int(num_prod) / int(num_proc)) * 100, 2)
    porcentagemExpulsos = 0 if int(num_proc) == 0 else round((int(num_exp) / int(num_proc)) * 100, 2)
    porcentagemDelta01 = 0 if int(num_proc) == 0 else round((int(rec_delta_A) / int(num_proc)) * 100, 2)
    porcentagemDelta02 = 0 if int(num_proc) == 0 else round((int(rec_delta_B) / int(num_proc)) * 100, 2)
    porcentagemBoca = 0 if int(num_proc) == 0 else round((int(rec_err_boca) / int(num_proc)) * 100, 2)
    porcentagemParede = 0 if int(num_proc) == 0 else round((int(rec_err_boca) / int(num_proc)) * 100, 2)
    porcentagemFundo = 0 if int(num_proc) == 0 else round((int(rec_err_fundo) / int(num_proc)) * 100, 2)
    porcentagemResidual = 0 if int(num_proc) == 0 else round((int(rec_err_residual) / int(num_proc)) * 100, 2)

    # Lista de colunas
    colunasSQL = [
        "DataHora",
        "processados",
        "porcentagem_processados",
        "produzidos",
        "porcentagem_produzidos",
        "expulsos",
        "porcentagem_expulsos",
        "delta_01",
        "porcentagem_delta_01",
        "delta_02",
        "porcentagem_delta_02",
        "boca",
        "porcentagem_boca",
        "parede",
        "porcentagem_parede",
        "fundo",
        "porcentagem_fundo",
        "residual",
        "porcentagem_residual",
        "horario_garrafa_teste",
        "falhas_garrafa_teste",
        "recipientes_processados_garrafa_teste",
    ]

    # Nova Lista com todos os valores
    valoresPredicao = [
        DataHora,
        num_proc,
        porcentagemProcessados,
        num_prod,
        porcentagemProduzidos,
        num_exp,
        porcentagemExpulsos,
        rec_delta_A,
        porcentagemDelta01,
        rec_delta_B,
        porcentagemDelta02,
        rec_err_boca,
        porcentagemBoca,
        rec_err_boca,
        porcentagemParede,
        rec_err_fundo,
        porcentagemFundo,
        rec_err_residual,
        porcentagemResidual,
        datetime.strptime(dataHoraGarrafaTeste, "%Y-%m-%d %H:%M:%S.%f"),
        todasAtividadesFaltantes,
        garrafasProcessadasUltimoTeste,
    ]

    # Printando resultados
    printaResultados(colunasSQL, valoresPredicao, console)

    # Escrevendo dados no IGS
    # escreveIGS(valoresPredicao,st)

    # Escrevendo os dados no SQLite
    # if DataHora.minute == 0:
    #     escreveSQL(colunasSQL, valoresPredicao,st)
    escreveSQL(colunasSQL, valoresPredicao, st, console)


def numerosOitoCaixas(caminhoImagemProcessada, modelo):
    """
    Função para predição dos numeros com oito caixas do inspetor
    """

    h = 1

    # Variaveis de retorno
    num_proc = ""
    num_prod = ""
    num_exp = ""

    while h < 9:
        img_proc = str(caminhoImagemProcessada) + str("/rec_proc") + str(h) + str(".png")
        img_prod = str(caminhoImagemProcessada) + str("/rec_prod") + str(h) + str(".png")
        img_exp = str(caminhoImagemProcessada) + str("/rec_exp") + str(h) + str(".png")

        img1 = predicao(img_proc, modelo)
        img2 = predicao(img_prod, modelo)
        img3 = predicao(img_exp, modelo)

        num_proc = str(num_proc) + str(img1)
        num_prod = str(num_prod) + str(img2)
        num_exp = str(num_exp) + str(img3)

        h = h + 1

    return int(num_proc), int(num_prod), int(num_exp)


def numeroSeteCaixas(caminhoImagemProcessada, modelo):
    """
    Função para predição dos numeros com sete caixas do inspetor
    """
    j = 1

    # variáveis de retorno
    rec_delta_A = ""
    rec_delta_B = ""
    rec_err_boca = ""
    rec_err_parede = ""
    rec_err_fundo = ""
    rec_err_residual = ""

    while j < 8:
        img_delta_A = str(caminhoImagemProcessada) + str("/rec_delta_A") + str(j) + str(".png")
        img_delta_B = str(caminhoImagemProcessada) + str("/rec_delta_B") + str(j) + str(".png")
        img_err_boca = str(caminhoImagemProcessada) + str("/rec_err_boca") + str(j) + str(".png")
        img_ams_parede = str(caminhoImagemProcessada) + str("/rec_err_parede") + str(j) + str(".png")
        img_ams_fundo = str(caminhoImagemProcessada) + str("/rec_err_fundo") + str(j) + str(".png")
        img_ams_residual = str(caminhoImagemProcessada) + str("/rec_err_residual") + str(j) + str(".png")

        img4 = predicao(img_delta_A, modelo)
        img5 = predicao(img_delta_B, modelo)
        img6 = predicao(img_err_boca, modelo)
        img7 = predicao(img_ams_parede, modelo)
        img8 = predicao(img_ams_fundo, modelo)
        img9 = predicao(img_ams_residual, modelo)

        rec_delta_A = str(rec_delta_A) + str(img4)
        rec_delta_B = str(rec_delta_B) + str(img5)
        rec_err_boca = str(rec_err_boca) + str(img6)
        rec_err_parede = str(rec_err_parede) + str(img7)
        rec_err_fundo = str(rec_err_fundo) + str(img8)
        rec_err_residual = str(rec_err_residual) + str(img9)

        j = j + 1

    return (
        int(rec_delta_A),
        int(rec_delta_B),
        int(rec_err_boca),
        int(rec_err_parede),
        int(rec_err_fundo),
        int(rec_err_residual),
    )
