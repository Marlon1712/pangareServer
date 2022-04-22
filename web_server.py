from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

from src.services.banco import Banco


def webserver():

    app = Flask(__name__, template_folder="./web/templates", static_folder="./web/static")
    sock = SocketIO(app)

    messages = []

    colunas = ["id", "DataHora", "processados", "produzidos", "expulsos", "porcentagem_expulsos"]
    # colunas = ["DISTINCT DataHora", "processados"]

    @app.route("/")
    def home():
        banco = Banco("./data/pangare.db", "uip")
        coluna, row = banco.listar(colunas)
        banco.desconect()
        return render_template("pangare.html", coluna=coluna, row=row)

    @app.route("/pangare")
    def pangare():
        return render_template("index.html")

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
