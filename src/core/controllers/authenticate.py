from flask import request
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
from src.core.models.authenticate import Authenticate as AuthenticateModel
from src.core.server.jwt import Jwt
app = server.app

class Authenticate(AbstractController):

    @app.route("/auth", methods=["POST"])
    def authenticate():
        body = request.get_json()
        # Instancia o objeto
        authenticate = AuthenticateModel()
        #Faz a autenticação
        result = authenticate.auth(body)
        # Verifica se ocorreram erros
        if result['result'] == False:
            return AbstractController.response(401, 'Failed to perform authentication!', 'result', result)

        response = AbstractController.response(200, 'Authentication successful!', 'result', result)
        return response

    @app.route("/tokenvalid", methods=["POST"])
    @Jwt.token_required
    def tokenValid(user, *args, **kwags):
        response = AbstractController.response(200, 'valid')

        return response