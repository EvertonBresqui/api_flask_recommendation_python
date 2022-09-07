from src.core.server.resource_db import ResourceDb
from src.core.server.instance import server
from src.config import Config

from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

class CreateModel():

    __resource_db = None
    __name_collection_pre_processed = None
    __name_collection_model = None
    __rules = None

    def __init__(self) -> None:
        self.__name_collection_pre_processed = Config.getNameCollectionPreProcessed(server.conf_sale["increment_id"])
        self.__name_collection_model =  Config.getNameModel(server.conf_sale["increment_id"])
        self.__resource_db = ResourceDb()

    def process(self):
        # Obtem os dados da coleção pre processada
        collection_pre_processed = self.__resource_db.selectMany(self.__name_collection_pre_processed, {}, {"_id": 0})
        # Converte cursor para Data Frame
        df = pd.DataFrame(list(collection_pre_processed))
        # Obtem as melhores regras
        self.train(df)
        # Salva o modelo
        self.saveModel()

    def train(self, df):
        frequent_itemsets = apriori(df, min_support = server.conf_params['min_support'], use_colnames = server.conf_params['use_colnames'])
        frequent_itemsets.sort_values(by=server.conf_params['freq_sort_by'], ascending = server.conf_params['freq_sort_ascending']).head(server.conf_params['freq_sort_head'])
        self.__rules = association_rules(frequent_itemsets, metric=server.conf_params['assoc_rule_metric'], min_threshold=server.conf_params['assoc_rule_min_threshold'])
        self.__rules.sort_values(by=server.conf_params['rule_sort_by'], ascending = server.conf_params['rule_sort_ascending']).drop(server.conf_params['rule_sort_drop'], axis=server.conf_params['rule_axis'])
        

    def saveModel(self):
        # Deleta o modelo anterior
        self.__resource_db.deleteLargeData(self.__name_collection_model)
        # Salva o modelo
        isSaved = self.__resource_db.saveLargeData(self.__name_collection_model, self.__rules)

        return isSaved