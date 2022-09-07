from src.config import Config
from src.core.server.jwt import Jwt

class Authenticate(object):

    def auth(self, data):
        response = {} 
        result = {}

        errors = self.__validate(data)

        if(len(errors) == 0):
            jwt = Jwt()
            # Faz a autenticação Jwt
            result = jwt.auth(data['username'], data['password'], data['sale_group'])
        
        if result != {}:
            response['result'] = result
        else:
            response['result'] = False
        response['errors'] = errors

        return response

    def __validate(self, data):
        errors = list()

        if Config.saleGroupExists(data["sale_group"]) == False:
            errors.append('Store group id is invalid')
        if isinstance(data["username"], str) == False or data["username"].strip() == '':
            errors.append('Inform the user')
        if isinstance(data["password"], str) == False or data["password"].strip() == '':
            errors.append('Inform the password')
    
        return errors