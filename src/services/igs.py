import logging

from opcua import Client, ua


class IGS:
    """
    Casse criada para falicitar conexao e escrita de dados no servidor IGS
    """

    def __init__(self, servidor="opc.tcp://10.174.12.247:49311"):
        self.client = Client(servidor)  # IP servidor IGS

    def write(self, tag_igs: str, valor):
        """
        Este metodo serve para escrever valor das tags no servidor IGS

        Args:
            tag_igs (string): neste parametro deve-se fornecer o endereco da tag
                              no servidor
            valor (any): neste campo deve-se passar o valor a ser enviado.

        Raises:
            ValueError: caso ocorra um erro durante execucao uma um erro sera
                        retornado

        Returns:
            None|error: metodo nao retorna nada caso operacao realizada com
                          sucesso e erro caso falha.
        """
        x = tag_igs.index("datatype=")
        datatype = tag_igs[x + 9 :]
        try:
            self.client.connect()
            tag = self.client.get_node(tag_igs)

            if datatype == "Boolean":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Boolean))
                except BaseException as err:
                    return err
            elif datatype == "SByte":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.SByte))
                except BaseException as err:
                    return err
            elif datatype == "Byte":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Byte))
                except BaseException as err:
                    return err
            elif datatype == "UInt16":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.UInt16))
                except BaseException as err:
                    return err
            elif datatype == "UInt32":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.UInt32))
                except BaseException as err:
                    return err
            elif datatype == "UInt64":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.UInt64))
                except BaseException as err:
                    return err
            elif datatype == "Int16":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Int16))
                except BaseException as err:
                    return err
            elif datatype == "Int32":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Int32))
                except BaseException as err:
                    return err
            elif datatype == "Int64":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Int64))
                except BaseException as err:
                    return err
            elif datatype == "Float":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Float))
                except BaseException as err:
                    return err
            elif datatype == "Double":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.Double))
                except BaseException as err:
                    return err
            elif datatype == "String":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.String))
                except BaseException as err:
                    return err
            elif datatype == "DateTime":
                try:
                    var_w = ua.DataValue(ua.Variant(valor, ua.VariantType.DateTime))
                except BaseException as err:
                    return err
            else:
                raise ValueError('"%s" datatype not implemented' % datatype)

            var_w.ServerTimestamp = None
            var_w.SourceTimestamp = None

            tag.set_value(var_w)
        except BaseException as err:
            print(f"Erro ao escrever no IGS {err}")
            logging.error(f"Erro ao escrever no IGS {err}")
            return err
        finally:
            self.client.disconnect()
