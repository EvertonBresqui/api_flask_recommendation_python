from flask import request
from src.core.server.jwt import Jwt
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
from src.core.recommendation import Recommendation
app = server.app

class SysRecommendationController(AbstractController):

    @app.route("/sysrecommendation", methods=["POST"])
    @Jwt.token_required
    def sysrecommendation(user, *args, **kwags):
        result = {}

        body = request.get_json()
        # Instancia o objeto
        recommendation_model = Recommendation()
        # Obtem a recomendação
        result = recommendation_model.recommendation(body)

        if result is not False:
            response = AbstractController.response(200, 'Recommendation processing success!', 'result', result)
        else:
            response = AbstractController.response(500, 'Recommendation processing failure!', 'result', result)
        
        return response
