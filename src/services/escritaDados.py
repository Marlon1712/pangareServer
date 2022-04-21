from utils.bcolors import BColors as Bc

from .banco import Banco
from .igs import IGS

# import logging


def escreveSQL(prefixo, listaResultados):
    """
    Função criada para escrever os resultados do inspetor no banco de dados
    local da cervejaria uberlândia.\n
    :lista_colunas: lista com os nomes das colunas, se possivel identicas ao do
    banco de dados local, para escrita.\n
    :lista_valores: valores calculados após a detecção numérica para serem
    salvos no banco de dados já com as porcentagens.\n
    """
    banco = Banco("./data/pangare.db", "uip")
    banco.criar_tabela(
        {
            "DataHora": "DATETIME",
            "processados": "INTEGER",
            "porcentagem_processados": "REAL",
            "produzidos": "INTEGER",
            "porcentagem_produzidos": "REAL",
            "expulsos": "INTEGER",
            "porcentagem_expulsos": "REAL",
            "delta_01": "INTEGER",
            "porcentagem_delta_01": "REAL",
            "delta_02": "INTEGER",
            "porcentagem_delta_02": "REAL",
            "boca": "INTEGER",
            "porcentagem_boca": "REAL",
            "parede": "INTEGER",
            "porcentagem_parede": "REAL",
            "fundo": "INTEGER",
            "porcentagem_fundo": "REAL",
            "residual": "INTEGER",
            "porcentagem_residual": "REAL",
            "horario_garrafa_teste": "DATETIME",
            "Garrafas_de_Teste": "BOOLEAN",
            "Controlador_do_Fundo": "BOOLEAN",
            "Cont_Fundo_Erro_Transp": "BOOLEAN",
            "Paredes_laterais_entrada": "BOOLEAN",
            "Paredes_laterais_saida": "BOOLEAN",
            "Controlad_Embocadura": "BOOLEAN",
            "Liquido_residual_HF_1": "BOOLEAN",
            "Liquido_residual_HF_2": "BOOLEAN",
            "Liquido_residual_IR": "BOOLEAN",
            "Cor_recipiente_incorreta": "BOOLEAN",
            "Controlo_ext1_entrada": "BOOLEAN",
            "recipientes_processados_garrafa_teste": "INTEGER",
        }
    )
    inputDicionario = {}
    for i, keyBanco in enumerate(prefixo):
        if keyBanco == "falhas_garrafa_teste":
            for key, valor in listaResultados[i].items():
                inputDicionario[key] = valor
        else:
            if keyBanco == "DataHora" or keyBanco == "horario_garrafa_teste":
                inputDicionario[keyBanco] = f"'{listaResultados[i]}'"
            else:
                inputDicionario[keyBanco] = listaResultados[i]

    try:
        banco.insert(inputDicionario)
        Bc.succes("[INFO] Dados escritos na tabela do SQLite!")
    except BaseException as err:
        Bc.error(f"Unexpected {err=}, {type(err)=}")
        Bc.error("[ERRO] Falha ao salvar no banco")


uip = IGS()


def escreveIGS(resultados):

    uip.write("ns=2;s=L502_INSPETORES.UIP502001.DATA_COLETA;datatype=DateTime", resultados[0])
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.PROCESSADA;datatype=Double",
        int(resultados[2]),
    )
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.PRODUZIDA;datatype=Double", int(resultados[4]))
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.EXPULSA;datatype=Double", int(resultados[6]))
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.BOCA;datatype=Double", int(resultados[12]))
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.PAREDE;datatype=Double", int(resultados[14]))
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.FUNDO;datatype=Double", int(resultados[16]))
    uip.write("ns=2;s=L502_INSPETORES.UIP502001.RESIDUAL;datatype=Double", int(resultados[18]))
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.DATA_COLETA_TESTE;datatype=DateTime",
        resultados[19],
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.RESULT_CHECK;datatype=Boolean",
        (0 if sum([int(x) for x in resultados[19].values()]) <= 3 else 1),
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_BOCA;datatype=Boolean",
        resultados[19]["Controlad_Embocadura"],
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_FUNDO;datatype=Boolean",
        (0 if resultados[19]["Controlador_do_Fundo"] != 1 or resultados[19]["Cont_Fundo_Erro_Transp"] != 1 else 1),
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_PAREDE;datatype=Boolean",
        (0 if resultados[19]["Paredes_laterais_entrada"] != 1 or resultados[19]["Paredes_laterais_saida"] != 1 else 1),
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_RESIDOS_LIQUIDOS;datatype=Boolean",
        resultados[19]["Liquido_residual_IR"],
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_RESIDOS_CAUSTICOS;datatype=Boolean",
        (0 if resultados[19]["Liquido_residual_HF_1"] != 1 or resultados[19]["Liquido_residual_HF_2"] != 1 else 1),
    )
    uip.write(
        "ns=2;s=L502_INSPETORES.UIP502001.CHECK_INSPECAO_PORCENTO_REJEICAO;datatype=Double",
        resultados[7],
    )

    Bc.succes("[INFO] Dados enviados para o Servidor IGS!")


def printaResultados(prefixo, listaResultados):

    for i, keyBanco in enumerate(prefixo):
        if keyBanco == "falhas_garrafa_teste":
            for key, valor in listaResultados[i].items():
                print(f"{key} : {'OK' if valor == 1 else 'NOK'}")
        else:
            print(f"{keyBanco} : {listaResultados[i]}")

    print(f"Result_Check : {'NOK' if sum([ int(x) for x in listaResultados[20].values() ]) <= 3 else 'OK'}")
