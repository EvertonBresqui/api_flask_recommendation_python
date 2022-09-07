from flask import request
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
from src.core.pre_processing import PreProcessing
from src.core.server.jwt import Jwt
app = server.app

class PreProcessController(AbstractController):

    # Save data in collection 
    @app.route("/preprocess", methods=["POST"])
    @Jwt.token_required
    def preprocess(user, *args, **kwags):
        body = request.get_json()

        # Instancia o objeto
        pre_process = PreProcessing()

        # Salva os dados na collection
        result = pre_process.preProcessing()
        # Verifica se ocorreram erros
        if result == False:
            return AbstractController.response(500, 'Failed pre-processing!', 'result', result)

        response = AbstractController.response(200, 'Success in pre-processing!', 'result', result)
        return response
