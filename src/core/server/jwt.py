from flask import request
from functools import wraps
import jwt
import datetime
from src.config import Config
from src.core.server.instance import server
from src.core.server.abstract_controller import AbstractController
app = server.app

class Jwt(AbstractController):

    # Faz a autenticação
    def auth(self, user, password, sale_group_id):
        result = {}
        sale_group = Config.getSaleGroup(sale_group_id)
        # Obtem o IP da solicitação
        ip_address = request.environ['REMOTE_ADDR']
        # Verifica se o IP informado é o setado nas configurações
        if(ip_address == sale_group['ip']):
            # Verifica se esta autenticado no JWT
            if(user == sale_group['username'] and password == sale_group['password']):
                
                app.config['SECRET_KEY'] = sale_group['secret_key']
                exp = datetime.datetime.now() + datetime.timedelta(hours=sale_group['hours_exp_token'])
                exp_str = str(exp)
                token = jwt.encode({
                    'username': sale_group['username'],
                    'sale_group': sale_group['id'],
                    'exp': exp
                    },
                    app.config['SECRET_KEY']
                )
                result = {'token': token.decode('UTF-8'), 'exp': exp_str}
                
        return result

    # Verifica se está autenticado
    def token_required(f):
        @wraps(f)

        def decorated(*args, **kwargs):
            token = request.args.get('token')
            if not token:
                return AbstractController.response(401, 'Token is missing')
            try:
                # Seta as configurações do contexto da aplicação
                server.setContextConfGeneral()
                # Obtem a configuração do grupo
                conf_sale_group = server.conf_sale_group
                if(len(conf_sale_group) == 0):
                    return AbstractController.response(401, 'Enter the store group id')
                # Seta a secret key
                app.config['SECRET_KEY'] = conf_sale_group['secret_key']
                user = jwt.decode(token, app.config['SECRET_KEY'])
            except:
                return AbstractController.response(401, 'Token is invalid or expired')
            # Verifica se o cliente logado é o mesmo que autenticou
            if(user['sale_group'] == conf_sale_group['id']):
                return f(user, *args, **kwargs)
            else:
                return AbstractController.response(401, 'You are not authenticated to access this group')
        return decorated
