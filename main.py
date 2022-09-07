# Carrega instância do flask
from src.core.server.instance import Server, server
# Controller responsável pela autenticação
from src.core.controllers.authenticate import *
# Controller responsável pela importação dos dados
from src.core.controllers.import_data.sys_import import *
# Controller responsável pelo pré processamento dos dados
from src.core.controllers.process_data.pre_process import *
# Controller responsável por criar o modelo para recomendação
from src.core.controllers.create_model.sys_create_model import *
# Controller responsável por processar a recomendação
from src.core.controllers.recommendation.sys_recommendation import *

# Inicia a aplicação
server.run()