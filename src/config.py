class Config(object):
    
    # Tipos de lojas aceitos
    __sales_types = {1: 'magento1', 2: 'magento2'}
    
    # Tipos de algorítmos implementados
    __algorithms = {
        1:'als',
        2:'a_priori'
    }

    # Configuração para acesso ao banco MongoDB
    __mongo_db = {
        'domain':'localhost:27017',
        'user':'user', # Colocar um nome dinâmico
        'password':'secret',
        'database':'database_name', # Colocar um nome dinâmico
    }

        # Configurações dos grupos das lojas(multi-stores)
    __sales_groups_conf = {
        # group id sale
        1:{
            'id': 1,
            'sale_type': 2, # type sale
            'username':'user',
            'password':'secret',
            'secret_key': '?????',
            'hours_exp_token': 30,
            'ip': '127.0.0.1'
        },
        2:{
            'id': 2,
            'sale_type': 1, # type sale
            'username':'user',
            'password':'secret',
            'secret_key': '?????',
            'hours_exp_token': 30,
            'ip': '127.0.0.1'
        }
    }
    
    # Configurações para cada loja independente(store_id)
    __sales = {
        1: {
            'name_store': 'store1', # name sale
            'increment_id': 1, # id sale
            'sale_group': 1, # id group sale
            # Configurações especificas que variam para cada tipo de loja
            'settings':{
                'store_id': 1, # store_id magento sale
                'website_id': 1, # website_id magento sale
                'group_id': 1 # group_id magento sale
            }
        },
        2: {
            'name_store': 'store2', # name sale
            'increment_id': 2, # id sale
            'sale_group': 2, # id group sale
            # Configurações especificas que variam para cada tipo de loja
            'settings':{
                'store_id': 1, # store_id magento sale
                'website_id': 1, # website_id magento sale
                'group_id': 1 # group_id magento sale
            }
        },
        3: {
            'name_store': 'store3', # name sale
            'increment_id': 3, # id sale
            'sale_group': 2, # id group sale
            # Configurações especificas que variam para cada tipo de loja
            'settings':{
                'store_id': 1, # store_id magento sale
                'website_id': 1, # website_id magento sale
                'group_id': 1 # group_id magento sale
            }
        },
        4: {
            'name_store': 'store4', # name sale
            'increment_id': 4, # id sale
            'sale_group': 1, # id group sale
            # Configurações especificas que variam para cada tipo de loja
            'settings':{
                'store_id': 1, # store_id magento sale
                'website_id': 1, # website_id magento sale
                'group_id': 1 # group_id magento sale
            }
        },
    }
    
    # Configurações dos parâmetros dos algoritmos de cada loja
    __params = {
        1:{
            'algorithm': 1,
            'train': 0.8,
            'test': 0.2,
            'random_state': 200,
            'factors': 20,
            'regularization': 0.1,
            'iterations': 20,
            'alpha_val': 15,
            'n_similar': 10,
            'num_items': 10
        },
        2:{
            'algorithm': 1,
            'train': 0.8,
            'test': 0.2,
            'random_state': 200,
            'factors': 20,
            'regularization': 0.1,
            'iterations': 20,
            'alpha_val': 15,
            'n_similar': 10,
            'num_items': 10
        },
        3:{
            'algorithm': 2,
            'min_support': 0.002,
            'use_colnames': True,
            'freq_sort_by': ['support'],
            'freq_sort_ascending': False,
            'freq_sort_head': 10,
            'assoc_rule_metric': "confidence",
            'assoc_rule_min_threshold': 0.1,
            'rule_sort_by': ['lift'],
            'rule_sort_ascending': False,
            'rule_sort_drop': ['antecedent support', 'consequent support', 'leverage', 'conviction'],
            'rule_axis': 1
        },
        4:{
            'algorithm': 2,
            'min_support': 0.002,
            'use_colnames': True,
            'freq_sort_by': ['support'],
            'freq_sort_ascending': False,
            'freq_sort_head': 10,
            'assoc_rule_metric': "confidence",
            'assoc_rule_min_threshold': 0.1,
            'rule_sort_by': ['lift'],
            'rule_sort_ascending': False,
            'rule_sort_drop': ['antecedent support', 'consequent support', 'leverage', 'conviction'],
            'rule_axis': 1
        }
    }


    # Obtem as configurações do MongoDB
    def getMongoDBSettings():
        return Config.__mongo_db

    # Obtem a url completa de conexao ao banco MongoDB
    def getUrlConnectionMongo():
        url = 'mongodb://' + Config.__mongo_db['user'] + ':' + Config.__mongo_db['password'] + '@' + Config.__mongo_db['domain'] + '/' + Config.__mongo_db['database']
        return url  
        
    # Obtem o nome da coleção pré processada
    def getNameCollectionPreProcessed(increment_id):
        nameCollectionPreProcessed = "collection_pre_processed_" + str(increment_id)
        return nameCollectionPreProcessed

    # Obtem o nome do arquivo do modelo
    def getNameModel(increment_id):
        nameCollectionPreProcessed = 'model_'+ str(increment_id)
        return nameCollectionPreProcessed


    # Obtem os tipos de lojas
    def getSaleTypes():
        return Config.__sales_types

    # Obtem o tipo do grupo
    def getSaleGroupType(sale_group_id):
        if Config.saleTypeIdExists(sale_group_id):
            sale_group = Config.__sales_groups_conf[sale_group_id]
            return Config.__sales_types[sale_group['sale_type']]
        return None  
    
    # Verifica se o nome do tipo da loja existe
    def saleTypeNameExists(sale_type_name):
        for key, value in Config.__sales_types.items():
            if(value == sale_type_name):
                return True
        return False
    
    # Verifica se o tipo da loja é aceito
    def saleTypeIdExists(sale_type_id):
        if sale_type_id in Config.__sales_types:
            return True
        return False

    # Obtem o tipo do algoritmo utilizado para recomendação na loja
    def getAlgorithm(increment_id):
        id_algorithm = Config.__params[increment_id]['algorithm']
        if Config.algorithmExists(id_algorithm):
            return Config.__algorithms[id_algorithm]
        return None

    # Verifica se o algoritimo existe
    def algorithmExists(id):
        for key, value in Config.__algorithms.items():
            if id == key:
                return True
        return False


    # Obtem as configurações do grupo da loja(multi-store)
    def getSaleGroup(sale_group):
        exists = Config.saleGroupExists(sale_group)
        if exists:
            return Config.__sales_groups_conf[sale_group] 

        return None;  

    # Verifica se o grupo existe
    def saleGroupExists(sale_group):
        for id, values in Config.__sales_groups_conf.items():
            if id == sale_group:
                return True
        return False


    # Obtem as configurações da loja
    def getSale(increment_id):
        if(Config.existsSale(increment_id) == True):
            return Config.__sales[increment_id]
        return None

    # Verifica se as configurações da loja foram declaradas
    def existsSale(increment_id):
        for key, value in Config.__sales.items():
            if increment_id == value['increment_id']:
                return True
        return False

    # Obtem os parâmetros de configuração da loja
    def getParams(increment_id):
        if Config.paramsExists(increment_id):
            return Config.__params[increment_id] 
        return None

    # Verifica se os parâmetros foram configurados
    def paramsExists(increment_id):
        for key, value in Config.__params.items():
            if increment_id == key:
                return True
        return False

