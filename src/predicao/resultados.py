from datetime import datetime

from .predicaoRf import carregaModelo, predicao

# from src.igs import *


def resultadoFinal(
    caminhoImagemProcessada,
    caminhoModelo,
    dataHoraGarrafaTeste,
    garrafasProcessadasUltimoTeste,
    todasAtividadesFaltantes,
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

    # variaveis de data e hora
    DataHora = datetime.now()

    # Porcentagens dos números
    porcentagemProcessados = 0 if num_proc == 0 else 100
    porcentagemProduzidos = 0 if num_proc == 0 else round((num_prod / num_proc) * 100, 2)
    porcentagemExpulsos = 0 if num_proc == 0 else round((num_exp / num_proc) * 100, 2)
    porcentagemDelta01 = 0 if num_proc == 0 else round((rec_delta_A / num_proc) * 100, 2)
    porcentagemDelta02 = 0 if num_proc == 0 else round((rec_delta_B / num_proc) * 100, 2)
    porcentagemBoca = 0 if num_proc == 0 else round((rec_err_boca / num_proc) * 100, 2)
    porcentagemParede = 0 if num_proc == 0 else round((rec_err_parede / num_proc) * 100, 2)
    porcentagemFundo = 0 if num_proc == 0 else round((rec_err_fundo / num_proc) * 100, 2)
    porcentagemResidual = 0 if num_proc == 0 else round((rec_err_residual / num_proc) * 100, 2)

    # Lista de colunas
    resultados = {
        "DataHora": DataHora,
        "processados": num_proc,
        "porcentagem_processados": porcentagemProcessados,
        "produzidos": num_prod,
        "porcentagem_produzidos": porcentagemProduzidos,
        "expulsos": num_exp,
        "porcentagem_expulsos": porcentagemExpulsos,
        "delta_01": rec_delta_A,
        "porcentagem_delta_01": porcentagemDelta01,
        "delta_02": rec_delta_B,
        "porcentagem_delta_02": porcentagemDelta02,
        "boca": rec_err_boca,
        "porcentagem_boca": porcentagemBoca,
        "parede": rec_err_parede,
        "porcentagem_parede": porcentagemParede,
        "fundo": rec_err_fundo,
        "porcentagem_fundo": porcentagemFundo,
        "residual": rec_err_residual,
        "porcentagem_residual": porcentagemResidual,
        "horario_garrafa_teste": datetime.strptime(dataHoraGarrafaTeste, "%Y-%m-%d %H:%M:%S.%f"),
        "falhas_garrafa_teste": todasAtividadesFaltantes,
        "recipientes_processados_garrafa_teste": garrafasProcessadasUltimoTeste,
    }

    return resultados


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
