from src.config import Config
from src.core.server.resource_db import ResourceDb
from src.core.server.instance import server

from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

class PreProcessing():

    def __init__(self):
        self.__resource_db = ResourceDb()
        self._name_collection_pre_processed = Config.getNameCollectionPreProcessed(server.conf_sale['increment_id'])
        self._transaction_encoder = TransactionEncoder()

    def process(self):

        result = {} 
        result = self.preProcessing()

        return result
    
    def preProcessing(self):
        list_all_transactions = []

        # Obtem as todos os pedidos
        orders = self.__resource_db.selectMany('sales_flat_order' + str(server.conf_sale['sale_group']), {"customer_id": { "$ne": None }, "store_id": str(server.conf_sale["settings"]["store_id"])}, {"_id": 0, "store_id": 1, "customer_id": 1, "entity_id": 1 })
        
        # Remove a collection
        is_delect_collection = self.__resource_db.dropCollection(self._name_collection_pre_processed)

        if is_delect_collection == False:
            return False
        
        for order in orders:
            transacation_items = []
            # Obtem os itens dos pedidos
            order_items = self.__resource_db.selectMany('sales_flat_order_item' + str(server.conf_sale['sale_group']), {"order_id": order["entity_id"]}, {"product_id": 1, "qty_ordered": 1})
            # Percorre os itens do pedido
            for order_item in order_items:
                # Add data in row collection
                try:
                    transacation_items.append(int(order_item["product_id"]))
                except ValueError as verr:
                    pass # do job to handle: s does not contain anything convertible to int
                except Exception as ex:
                    pass # do job to handle: Exception occurred while converting to int
            
            # Process validation
            valid = self.__validateData(transacation_items)
            if valid == True:
                list_all_transactions.append(transacation_items)
            
        # Realiza o encode dos dados
        te_ary = self._transaction_encoder.fit(list_all_transactions).transform(list_all_transactions)
        # Tranforma a lista em dataframe
        df = pd.DataFrame(te_ary, columns=self._transaction_encoder.columns_)
        # Tranforma os indices e colunas para string
        df.index = df.index.map(str)
        df.columns = df.columns.map(str)
        # Obtem os valores do dataframe 
        data = df.to_dict('records')

        # Salva os dados no mongo
        self.__resource_db.insertMany(self._name_collection_pre_processed, data)

        return True
        

    def __validateData(self, items):
        valid = True

        for item in items:
            # Valida se o produto existe no store
            n_rows_product = self.__resource_db.getNrows("catalog_product_entity_int" + str(server.conf_sale['sale_group']), {"entity_id": str(item), "store_id": { "$in": ["0", str(server.conf_sale["settings"]["store_id"])] }})
            if n_rows_product == 0:
                valid = False
            # Valida se o produto esta ativo
            attribute = self.__resource_db.selectOne("eav_attribute" + str(server.conf_sale['sale_group']), {"attribute_code": "status", "source_model": "catalog/product_status"}, {"attribute_id": 1})
            product_is_active = self.__resource_db.getNrows("catalog_product_entity_int" + str(server.conf_sale['sale_group']), {"entity_id": str(item), "attribute_id": attribute["attribute_id"], "value": "1"})
            if product_is_active == 0:
                valid = False
            # Valida se o produto tem em estoque
            stock_item = self.__resource_db.selectOne("cataloginventory_stock_item" + str(server.conf_sale['sale_group']), {"product_id": str(item)}, {"is_in_stock": 1})
            if stock_item == None or stock_item["is_in_stock"] == 0:
                valid = False
    
        return valid

