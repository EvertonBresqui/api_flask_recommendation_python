from src.core.resources.import_data.sys_import import SysImportResource
from src.config import Config
from src.core.server.instance import server

class SysImportModel(object):

    # Salva os dados
    def saveData(self, params, data):
        response = {} 
        result = {}

        sale_type = Config.getSaleGroupType(server.conf_sale_group['id'])
        errors = self.__validateCollections(sale_type, params, data)

        if len(errors) == 0:
            sysimport_resource = SysImportResource()
            result = sysimport_resource.saveData(sale_type, params, data)

        if result == 'ok':
            response['result'] = result
            response['errors'] = errors
        else:
            response['result'] = 'Failed to save data'
            response['errors'] = errors

        return response

    # Valida a estrutura tanto das collections quanto dos atributos
    def __validateCollections(self, sale_type, params, data):
        errors = list()

        if Config.saleTypeNameExists(sale_type) is not True:
            errors.append('The type of store informed is not supported by the platform')

        if 'drop' not in params:
            errors.append('Enter the drop parameter')

        for table_name in data:
            if table_name.strip() == '':
                errors.append('The table name has not been declared')
            
            if isinstance(data[table_name], list) is not True:
                errors.append('Unset data in table ' + table_name)

        return errors

    
