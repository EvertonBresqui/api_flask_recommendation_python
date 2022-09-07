from sklearn.preprocessing import MinMaxScaler
import scipy.sparse as sparse
import numpy as np
import pandas as pd
from pandas import DataFrame
from src.config import Config
from src.core.server.instance import server
from src.core.server.resource_db import ResourceDb


class Recommendation(object):

    _body = None
    _model = None
    _df = None

    def process(self, body):
        result = []
        self.__resource_db = ResourceDb()

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
        collection_pre_processed_name = Config.getNameCollectionPreProcessed(
            server.conf_sale["increment_id"])
        # Obtem os dados da coleção pre processada
        collection_pre_processed = self.__resource_db.selectMany(collection_pre_processed_name, {}, {
                                                                 "product_id": 1, "customer_id": 1, "qty_salable": 1, "_id": 0})
        # Converte cursor para Data Frame
        self._df = DataFrame(collection_pre_processed)
        sparse_user_item = sparse.csr_matrix((self._df['qty_salable'].astype(
            float), (self._df['customer_id'], self._df['product_id'])))
        # Get the trained user and item vectors. We convert them to
        # csr matrices to work with our previous recommend function.
        user_vecs = sparse.csr_matrix(self._model.user_factors)
        item_vecs = sparse.csr_matrix(self._model.item_factors)
        # Create recommendations for users
        recommendations = []
        for user_id in self._body['users']:
            recommendation = self.recommend(user_id, sparse_user_item, user_vecs, item_vecs, server.conf_params['num_items'])
            # Converte os dados para Json
            recommendations.append(recommendation.to_json(orient="split"))

        return recommendations

    # ------------------------------
    # CREATE USER RECOMMENDATIONS
    # ------------------------------

    def recommend(self, user_id, sparse_user_item, user_vecs, item_vecs, num_items=10):
        """The same recommendation function we used before"""

        user_interactions = sparse_user_item[user_id, :].toarray()

        user_interactions = user_interactions.reshape(-1) + 1
        user_interactions[user_interactions > 1] = 0

        rec_vector = user_vecs[user_id, :].dot(item_vecs.T).toarray()

        min_max = MinMaxScaler()
        rec_vector_scaled = min_max.fit_transform(
            rec_vector.reshape(-1, 1))[:, 0]
        recommend_vector = user_interactions * rec_vector_scaled

        item_idx = np.argsort(recommend_vector)[::-1][:num_items]

        values = []
        scores = []

        for idx in item_idx:
            values.append(idx)
            scores.append(recommend_vector[idx])

        recommendations = pd.DataFrame({'values': values, 'score': scores})

        return recommendations

    def validate(self):
        if(isinstance(self._body['users'], list) and len(self._body['users']) > 0):
            return True
        return False
