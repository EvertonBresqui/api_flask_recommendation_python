import scipy.sparse as sparse
import implicit # The Cython library
from pandas import DataFrame
from src.core.server.resource_db import ResourceDb
from src.core.server.instance import server
from src.config import Config

class CreateModel():

    __resource_db = None
    __name_collection = None
    __model = None

    def __init__(self) -> None:
        self.__name_collection = Config.getNameCollectionPreProcessed(server.conf_sale["increment_id"])
        self.__resource_db = ResourceDb()

    def process(self):
        # Obtem os dados da coleção pre processada
        collection_pre_processed = self.__resource_db.selectMany(self.__name_collection, {}, {"product_id": 1, "customer_id": 1, "qty_salable": 1, "_id": 0})
        # Converte cursor para Data Frame5
        df = DataFrame(collection_pre_processed)
        # Faz o treinamento
        self.train(df)
        # Salva o modelo
        self.saveModel()

    def train(self, training):
        index = training.index
        if(len(index) == 0):
            raise ValueError('Training data not informed.')

        sparse_item_user = sparse.csr_matrix((training['qty_salable'].astype(float), (training['product_id'], training['customer_id'])))
        
        self.__model = implicit.als.AlternatingLeastSquares(factors=server.conf_params['factors'], regularization=server.conf_params['regularization'], iterations=server.conf_params['iterations'])
        # Calculate the confidence by multiplying it by our alpha value.
        data_conf = (sparse_item_user * server.conf_params['alpha_val']).astype('double')

        # Fit the model
        self.__model.fit(data_conf)

    def saveModel(self):
        # Obtem nome do modelo
        name_model = Config.getNameModel(server.conf_sale["increment_id"])
        # Deleta o modelo anterior
        self.__resource_db.deleteLargeData(name_model)
        # Salva o modelo
        isSaved = self.__resource_db.saveLargeData(name_model, self.__model)

        return isSaved