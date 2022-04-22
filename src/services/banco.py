import sqlite3


class Banco:
    """Classe para manipulacao de banco de dados com SQLite"""

    def __init__(self, db_path: str, tabela: str):
        """Metodo construtor da classe Banco"""
        self._db_path = db_path
        self._tabela = tabela
        self._schema = {}
        self._conexao = sqlite3.connect(self._db_path)
        self._cursor = self._conexao.cursor()

    def desconect(self):

        """Metodo para desconetar do banco de dados"""

        try:
            self._conexao.close()
        except BaseException as err:
            print(err)

    def criar_tabela(self, schema: dict):
        """Metodo para criar tabela no banco de dados

        Args:
            schema (dict): Dicionario contendo o schema da tabela no formato ({'nome_coluna':'tipo_do_dado'})
        """
        self._schema = schema
        try:
            query = f"""CREATE TABLE IF NOT EXISTS {self._tabela}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,"""
            for key, value in schema.items():
                query = query + f""" {key} {value},"""

            query = query[:-1]
            query = query + ")"
            self._cursor.execute(query)
            self._conexao.commit()
        except BaseException as err:
            print(err)

    def insert(self, configuracao: dict):
        """Este metodo serve para inserir valores na tabela

        Args:
            configuracao (dict): dicionario contendo {coluna:valor} a serem inseridos
        """

        try:
            config = ""
            valor = ""
            for key, v in configuracao.items():
                config = config + key + ","
                valor = valor + str(v) + ","
            config = config[:-1]
            valor = valor[:-1]
            query = f"INSERT INTO {self._tabela} ({config}) VALUES ({valor})"
            self._cursor.execute(query)
            self._conexao.commit()
        except BaseException as err:
            print(err)
            raise

    def filtro(self, operador: bool = False, **kwargs) -> list:  # buscar dados
        """Metodo que realiza uma consulta no banco de dados

        Args:
            operador (bool, optional): Define se o operador é AND ou OR. Padrao e False.
            **kwargs: paramento no formato ('nome_da_coluna' = valor) para filtrar a busca

        Returns:
            list: lista de dados encontrados
        """
        try:
            if operador is False:
                op = "AND"
            else:
                op = "OR"
            query = f"SELECT * FROM {self._tabela}"
            if kwargs is not None:
                query = query + " WHERE "
                for key, value in kwargs.items():
                    query = query + f" {key} = {value} {op} "
                if op == "and":
                    query = query[:-5]
                else:
                    query = query[:-4]
            self._cursor.execute(query)
            self._conexao.commit()
            return self._cursor.fetchall()
        except BaseException as err:
            print(f"Erro acesso ao banco {err}")
            raise

    def listar(self, lista: list[str]) -> tuple:
        """Metodo para listar registros da tabela

        Args:
            lista (list[str]): Parametro contendo os campos a serem listados

        Returns:
            tuple: Retorna uma tupla com duas listas no formato (colunas,valores)
        """
        colunas = []
        try:
            query = f"SELECT * FROM {self._tabela}"
            if len(lista) > 0:
                query = f"SELECT {','.join(lista)} FROM {self._tabela}"

            data = self._cursor.execute(query)
            self._conexao.commit()

            for coluna in data.description:
                colunas.append(coluna[0])
            rows = self._cursor.fetchall()
            return (colunas, rows)
        except BaseException as err:
            print(f"Erro acesso ao banco {err}")
            raise

    def update(self, id: int, config: dict):

        try:
            if config is not None:
                for parametro, valor in config.items():
                    query = f"""UPDATE {self._tabela} SET {parametro} = {valor} WHERE id = {id}"""
                    self._cursor.execute(query)
                    self._conexao.commit()
            else:
                raise Exception("Parametro config nao pode ser None informado")
        except BaseException as err:
            print(err)

    def deletar(self, id: int):
        """Metodo para deletar registro do banco de dados

        Args:
            id (int): id do registro a ser deletado
        """
        try:
            query = f"DELETE FROM {self._tabela} WHERE id = {id}"
            self._cursor.execute(query)
            self._conexao.commit()
        except BaseException as err:
            print(err)
            raise
