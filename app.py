from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

from src.services.banco import Banco


def webserver():

    app = Flask(__name__, template_folder="./web/templates", static_folder="./web/static")
    sock = SocketIO(app)

    messages = []

    colunas = [
        "DISTINCT horario_garrafa_teste",
        "Garrafas_de_Teste",
        "Controlador_do_Fundo",
        "Cont_Fundo_Erro_Transp",
        "Paredes_laterais_entrada",
        "Paredes_laterais_saida",
        "Controlad_Embocadura",
        "Liquido_residual_HF_1",
        "Liquido_residual_HF_2",
        "Liquido_residual_IR",
        "Cor_recipiente_incorreta",
        "Controlo_ext1_entrada",
    ]
    # colunas = ["DISTINCT DataHora", "processados"]

    @app.route("/garrafa-teste")
    def home():
        banco = Banco("./data/pangare.db", "gft")
        coluna, row = banco.listar(colunas)
        banco.desconect()
        return render_template("garrafaTeste.html", coluna=coluna, row=row)

    @app.route("/")
    def pangare():
        banco = Banco("./data/pangare.db", "uip")
        coluna, row = banco.listar([])
        banco.desconect()
        return render_template("contadores.html", coluna=coluna, row=row)

    @app.route("/config")
    def tec():
        return render_template("config.html")

    @app.route("/config-1")
    def tec1():
        return render_template("config1.html")

    @sock.on("sendMessage")
    def send_message_handler(msg):
        # banco = Banco("dados.db", "pangare")
        # result = banco.buscar()
        emit("getMessage", msg, broadcast=True)

    @sock.on("message")
    def message_handler(msg):
        send(messages)

    sock.run(app, host="0.0.0.0", debug=True)


if __name__ == "__main__":
    webserver()
