from .banco import Banco
from .igs import IGS

# import logging


def escreveSQL(prefixo, listaResultados, st, console):
    """
    Função criada para escrever os resultados do inspetor no banco de dados
    local da cervejaria uberlândia.\n
    :lista_colunas: lista com os nomes das colunas, se possivel identicas ao do
    banco de dados local, para escrita.\n
    :lista_valores: valores calculados após a detecção numérica para serem
    salvos no banco de dados já com as porcentagens.\n
    """
    banco = Banco("./data/pangare.db", "uip")
    bancoGfT = Banco("./data/pangare.db", "gft")

    banco.criar_tabela(
        {
            "DataHora": "DATETIME NOT NULL UNIQUE",
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
        }
    )
    bancoGfT.criar_tabela(
        {
            "horario_garrafa_teste": "DATETIME NOT NULL UNIQUE",
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
    inputCDicionario = {}
    inputGftDicionario = {}

    for i, keyBanco in enumerate(prefixo):
        if keyBanco == "falhas_garrafa_teste":
            for key, valor in listaResultados[i].items():
                inputGftDicionario[key] = valor
        else:
            if keyBanco == "DataHora":
                inputCDicionario[keyBanco] = f"'{listaResultados[i]}'"
            else:
                if keyBanco == "horario_garrafa_teste":
                    inputGftDicionario[keyBanco] = f"'{listaResultados[i]}'"
                else:
                    if keyBanco == "recipientes_processados_garrafa_teste":
                        inputGftDicionario[keyBanco] = listaResultados[i]
                    else:
                        inputCDicionario[keyBanco] = listaResultados[i]

    # for i, key, value in enumerate(inputDicionario.values()):
    #     if i < 18:
    #         inputCDicionario[key] = value
    #     else:
    #         inputGftDicionario[key] = value

    try:
        banco.insert(inputCDicionario)
        bancoGfT.insert(inputGftDicionario)
        st.update("[bold green]Dados escritos na tabela do SQLite![/]")
    except BaseException as err:
        console.log(f"[bold red]Unexpected {err=}, {type(err)=}[/]")
        console.log("[bold red]Falha ao salvar no banco[/]")


uip = IGS()


def escreveIGS(resultados, st):

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

    st.update("Dados enviados para o Servidor IGS![/]")


def printaResultados(prefixo, listaResultados, st):
    st.print(f"[blue bold]{'=' *18}[ Contadores ]{'=' *18}[/]")
    for i, keyBanco in enumerate(prefixo):
        if keyBanco == "falhas_garrafa_teste":
            for key, valor in listaResultados[i].items():
                st.print(f"[yellow][bold]{key}[/][/] : {'[green]OK[/]' if valor == 1 else '[red]NOK[/]'}")
        else:
            if keyBanco == "horario_garrafa_teste":
                st.print(f"[blue bold]{'=' *17}[ Garrafa Teste ]{'=' *16}[/]")
                st.print(f"[yellow][bold]{keyBanco}[/][/] : [green]{listaResultados[i]}[/]")
            else:
                st.print(f"[yellow][bold]{keyBanco}[/][/] : [green]{listaResultados[i]}[/]")

    st.print(f"[blue bold]{'=' *50}[/]")
