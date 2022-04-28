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
        num_err_ech,
        num_err_cap,
        num_err_rot,
        num_ams_ech,
        num_ams_cap,
        num_ams_rec,
    ) = numeroSeteCaixas(caminhoImagemProcessada, modelo)
    resultadosFinais = [
        num_proc,
        num_prod,
        num_exp,
        num_err_ech,
        num_err_cap,
        num_err_rot,
        num_ams_ech,
        num_ams_cap,
        num_ams_rec,
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
    porcentagemDelta01 = 0 if int(num_proc) == 0 else round((int(num_err_ech) / int(num_proc)) * 100, 2)
    porcentagemDelta02 = 0 if int(num_proc) == 0 else round((int(num_err_cap) / int(num_proc)) * 100, 2)
    porcentagemBoca = 0 if int(num_proc) == 0 else round((int(num_err_rot) / int(num_proc)) * 100, 2)
    porcentagemParede = 0 if int(num_proc) == 0 else round((int(num_ams_ech) / int(num_proc)) * 100, 2)
    porcentagemFundo = 0 if int(num_proc) == 0 else round((int(num_ams_cap) / int(num_proc)) * 100, 2)
    porcentagemResidual = 0 if int(num_proc) == 0 else round((int(num_ams_rec) / int(num_proc)) * 100, 2)

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
        num_err_ech,
        porcentagemDelta01,
        num_err_cap,
        porcentagemDelta02,
        num_err_rot,
        porcentagemBoca,
        num_ams_ech,
        porcentagemParede,
        num_ams_cap,
        porcentagemFundo,
        num_ams_rec,
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
    escreveSQL(colunasSQL, valoresPredicao, st,console)


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
    num_err_ech = ""
    num_err_cap = ""
    num_err_rot = ""
    num_ams_ech = ""
    num_ams_cap = ""
    num_ams_rec = ""

    while j < 8:
        img_err_ech = str(caminhoImagemProcessada) + str("/rec_err_ech") + str(j) + str(".png")
        img_err_cap = str(caminhoImagemProcessada) + str("/rec_err_cap") + str(j) + str(".png")
        img_err_rot = str(caminhoImagemProcessada) + str("/rec_err_rot") + str(j) + str(".png")
        img_ams_ech = str(caminhoImagemProcessada) + str("/rec_ams_ech") + str(j) + str(".png")
        img_ams_cap = str(caminhoImagemProcessada) + str("/rec_ams_cap") + str(j) + str(".png")
        img_ams_rec = str(caminhoImagemProcessada) + str("/rec_ams_rec") + str(j) + str(".png")

        img4 = predicao(img_err_ech, modelo)
        img5 = predicao(img_err_cap, modelo)
        img6 = predicao(img_err_rot, modelo)
        img7 = predicao(img_ams_ech, modelo)
        img8 = predicao(img_ams_cap, modelo)
        img9 = predicao(img_ams_rec, modelo)

        num_err_ech = str(num_err_ech) + str(img4)
        num_err_cap = str(num_err_cap) + str(img5)
        num_err_rot = str(num_err_rot) + str(img6)
        num_ams_ech = str(num_ams_ech) + str(img7)
        num_ams_cap = str(num_ams_cap) + str(img8)
        num_ams_rec = str(num_ams_rec) + str(img9)

        j = j + 1

    return (
        int(num_err_ech),
        int(num_err_cap),
        int(num_err_rot),
        int(num_ams_ech),
        int(num_ams_cap),
        int(num_ams_rec),
    )
