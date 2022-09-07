from src.config import Config
from src.core.server.resource_db import ResourceDb
from src.core.server.instance import server

class PreProcessing():

    def __init__(self):
        self.__resource_db = ResourceDb()
        self._name_collection_pre_processed = Config.getNameCollectionPreProcessed(server.conf_sale['increment_id'])

    def process(self):

        result = {} 
        result = self.preProcessing()

        return result
    
    def preProcessing(self):
        row = {}
        # Obtem as todos os pedidos
        orders = self.__resource_db.selectMany('sales_order' + str(server.conf_sale['sale_group']), {"customer_id": { "$ne": None }, "store_id": str(server.conf_sale["settings"]["store_id"])}, {"_id": 0, "store_id": 1, "customer_id": 1, "entity_id": 1 })
        
        # Remove a collection
        is_delect_collection = self.__resource_db.dropCollection(self._name_collection_pre_processed)
        if is_delect_collection == False:
            return False

        for order in orders:
            # Obtem os itens dos pedidos
            order_items = self.__resource_db.selectMany('sales_order_item' + str(server.conf_sale['sale_group']), {"order_id": order["entity_id"]}, {"product_id": 1, "qty_ordered": 1})
            # Percorre os itens do pedido
            for order_item in order_items:
                # Add data in row collection ALS
                try:
                    row = {'product_id': int(order_item["product_id"]), 'customer_id': int(order["customer_id"]), 'qty_salable': float(order_item["qty_ordered"])}
                except ValueError as verr:
                    pass # do job to handle: s does not contain anything convertible to int
                except Exception as ex:
                    pass # do job to handle: Exception occurred while converting to int
                # Process validation
                valid = self.__validateData(row)
                if valid == True:
                    # Save row
                    self.__resource_db.insertOne(self._name_collection_pre_processed, row)

        return True

    def __validateData(self, row):
        valid = True
        # Valida se o produto existe no store
        n_rows_product = self.__resource_db.getNrows("catalog_product_entity_int" + str(server.conf_sale['sale_group']), {"entity_id": str(row['product_id']), "store_id": { "$in": ["0", str(server.conf_sale["settings"]["store_id"])] }})
        if n_rows_product == 0:
            valid = False
        # Valida se o produto esta ativo
        attribute = self.__resource_db.selectOne("eav_attribute" + str(server.conf_sale['sale_group']), {"attribute_code": "status", "source_model": "Magento\\Catalog\\Model\\Product\\Attribute\\Source\\Status"}, {"attribute_id": 1})
        product_is_active = self.__resource_db.getNrows("catalog_product_entity_int" + str(server.conf_sale['sale_group']), {"entity_id": str(row['product_id']), "attribute_id": attribute["attribute_id"], "value": "1"})
        if product_is_active == 0:
            valid = False
        # Valida se o produto tem em estoque
        stock_item = self.__resource_db.selectOne("cataloginventory_stock_item" + str(server.conf_sale['sale_group']), {"product_id": str(row['product_id'])}, {"is_in_stock": 1})
        if stock_item == None or stock_item["is_in_stock"] == 0:
            valid = False
        # Valida se o cliente existe no store
        customer_is_exists = self.__resource_db.getNrows("customer_entity" + str(server.conf_sale['sale_group']), {"entity_id": str(row['customer_id']), "website_id": str(server.conf_sale['settings']['website_id'])})
        if customer_is_exists == 0:
            valid = False
 
        return valid

