from src.config import Config
from src.core.server.instance import server
from src.core.server.resource_db import ResourceDb

class Recommendation(object):

    _body = None
    _model = None
    __resource_db = None

    def __init__(self) -> None:
        self.__resource_db = ResourceDb()

    def process(self, body):
        result = []

        self._body = body

        # Valida os dados
        if(self.validate()):
            self.load_model()

            result = self.recommendation()

        return result

    def load_model(self):
        # Obtem nome do modelo
        name_model = Config.getNameModel(server.conf_sale["increment_id"])
        self._model = self.__resource_db.getLargeData(name_model)

    def recommendation(self):
        products_related = []        

        for product_id in self._body['products']:
            products_related.append(self.direct_relation(product_id))

        return products_related
    
    def direct_relation(self, product_id):
        result = []
        data = self._model.to_dict('records')
        for row in data:
            antecedents = list(row['antecedents'])
            if str(product_id) in antecedents:
                row['antecedents'] = list(row['antecedents'])
                row['consequents'] = list(row['consequents'])
                result.append(row)
        
        return result

    def validate(self):
        if(isinstance(self._body['products'], list) and len(self._body['products']) > 0):
            return True
        return False
