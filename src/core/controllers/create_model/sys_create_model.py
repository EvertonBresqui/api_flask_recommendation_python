from flask import request
from src.core.server.jwt import Jwt
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
from src.core.create_model import CreateModel
app = server.app

class SysCreateModelController(AbstractController):

    @app.route("/syscreatemodel", methods=["POST"])
    @Jwt.token_required
    def sysCreateModel(user, *args, **kwags):
        # Instancia o objeto
        sys_create_model = CreateModel()

        # Cria modelo
        result = sys_create_model.createModel()
        # Verifica se ocorreram erros
        if result == False:
            return AbstractController.response(500, 'Failed to create model!', 'result', result)

        response = AbstractController.response(200, 'Model successfully created!', 'result', result)
        return response
