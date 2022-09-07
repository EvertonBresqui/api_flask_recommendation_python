from flask import Flask
from src.config import Config
from flask import request

class Server():
    def __init__(self):
        self.app = Flask(__name__)

    def run(self,):
        self.app.run(
            debug=True
        )

    def setContextConfGeneral(self):
        try:
            body = request.get_json()
            # Seta as configurações do grupo no escopo global
            if "sale_group" in body:
                self.conf_sale_group = Config.getSaleGroup(body["sale_group"])
            else:
                self.conf_sale_group = None
            # Seta as configurações da loja no escopo global
            if "increment_id" in body:
                self.conf_sale = Config.getSale(body["increment_id"])
            else:
                self.conf_sale = None
            # Seta as configurações dos parâmetros no escopo global
            if self.conf_sale != None:
                self.conf_params = Config.getParams(body["increment_id"])
            else:
                self.conf_params = None
        except:
            self.conf_sale_group = None
            self.conf_sale = None
            self.conf_params = None
            
server = Server()
