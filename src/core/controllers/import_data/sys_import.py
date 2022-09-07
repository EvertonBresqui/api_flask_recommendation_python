from flask import request
from src.core.server.jwt import Jwt
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
from src.core.models.import_data.sys_import import SysImportModel
app = server.app

class SysImportController(AbstractController):
    
    # Save data in collection 
    @app.route("/sysimport", methods=["POST"])
    @Jwt.token_required
    def saveData(user, *args, **kwags):
        body = request.get_json()

        # Instancia o objeto
        sysModel = SysImportModel()

        # Salva os dados na collection
        result = sysModel.saveData(body['params'], body['data'])
        # Verifica se ocorreram erros
        if len(result['errors']) > 0:
            return AbstractController.response(500, 'Failed to save data!', 'result', result)

        response = AbstractController.response(200, 'Data saved successfully!', 'result', result)
        return response
