from src.core.server.resource_db import ResourceDb
import datetime
from src.core.server.instance import server

class SysImportResource(ResourceDb):

    def __init__(self): #Construtor da classe.
        self.__resource_db = ResourceDb()

    def saveData(self, sale_type, params, data):
        resourceDb = ResourceDb()
        result = False

        for collection_name in data:
            collection_name_group = collection_name + str(server.conf_sale_group['id'])

            # Caso for o primeiro registro
            if(params['drop'] == True):
                # Drop collection 
                self.__dropCollection(collection_name_group)

            # collection controll
            self.collectionControl(collection_name_group, sale_type)

            # Importação os dados agrupados por arquivo
            grouped = self.__checkGroupedArrays(data[collection_name])  
            if grouped == True:
                for value in data[collection_name]:
                    # insert data in collection
                    result = resourceDb.insertMany(collection_name_group, value)
            # Importação dados por API 
            else:
                result = resourceDb.insertMany(collection_name_group, data[collection_name])

            if result is not True:
                return 'Error saving data to '+ collection_name_group +' collection'

        return 'ok'
        
    def collectionControl(self, collection_name, sale_type):

        if self.__verifyCollectionControllExists(collection_name, sale_type) is not True:
            # add row in control_configuration
            self.__resource_db.insertOne(
                "control_configuration",
                {"collection_name": collection_name, "sale_type": sale_type, "sale_group": server.conf_sale_group['id'], 'update_at': datetime.datetime.now()}
            )


    # return True or False
    def __verifyCollectionControllExists(self, collection_name, sale_type):
        exists = self.__resource_db.exists(
            'control_configuration',
            {'collection_name': collection_name, 'sale_type': sale_type, 'sale_group': server.conf_sale_group['id']}
        )

        return exists
    
    # Deleta a collection se ela existir
    def __dropCollection(self, collection_name):
        n_rows = self.__resource_db.getNrows(collection_name, {})
        if n_rows > 0:
            self.__resource_db.dropCollection(collection_name)

    # Vefica se existe arrays agrupados
    def __checkGroupedArrays(self, data):
        for value in data:
            if isinstance(value, list):
                return True
        return False