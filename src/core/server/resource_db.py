from flask_pymongo import PyMongo
from pymongo.errors import BulkWriteError
from src.config import Config
from src.core.server.instance import server
# Grava arquivos grandes no mongoDB > 16MB
import gridfs
import bson
import pickle

# Criar uma classe dinâmica gerenciar os dados
class ResourceDb(object):

    def __init__(self): #Construtor da classe.
        url = Config.getUrlConnectionMongo()
        self.__mongodb_client = PyMongo(server.app, url)
        self.__db =  self.__mongodb_client.db
    
    def getConnection(self):
        return self.__db

    # save many
    def insertMany(self, collection_name, data):
        try:
            self.__db[collection_name].insert_many(data, ordered=False)

        except BulkWriteError as e:
            res = e
            return False

        return True
    
    # save one
    def insertOne(self, collection_name, data):
        try:
            response = self.__db[collection_name].insert_one(data)

        except BulkWriteError as e:
            return -1

        return response.inserted_id

    # update one registry
    def updateOne(collection_name, data):
        pass

    # update many registrys
    def updateMany(collection_name, data):
        pass

    # delete one
    def deleteOne(collection_name, where):
        pass

    # delete many
    def deleteMany(collection_name, where):
        pass

    def selectOne(self, collection_name, where, select):
        # find_one({'email' : email, 'password' : password}, {'_id': 1})
        # or find_one({'_id': 1}, {'email' : email})
        row = self.__db[collection_name].find_one(where, select)
        return row

    def selectMany(self, collection_name, where, select):
        #find({'email' : email, 'password' : password}, {'_id': 1})
        rows = self.__db[collection_name].find(where, select)
        return rows

    def getNrows(self, collection_name, where):
        result = self.__db[collection_name].find(where).count()

        return result

    def exists(self, collection_name, where):
        result = self.__db[collection_name].find(where).count()
        if result > 0:
            return True
        return False

    def dropCollection(self, collection_name):
        try:
            self.__db[collection_name].drop()
            return True
        except:
            return False
    
    def deleteLargeData(self, name):
        try:
            row = self.__db['fs.files'].find_one({'filename': name}, {})
            if row != None:
                self.__db['fs.chunks'].remove({'files_id':row['_id']})
                self.__db['fs.files'].remove({'_id':row['_id']})
            return True
        except BulkWriteError as e:
            return False

    # Salva arquivos grandes
    def saveLargeData(self, name, modelInstance):
        try:
            fs = gridfs.GridFS(self.__db)
            fileID = fs.put(bson.Binary(pickle.dumps(modelInstance)), filename = name)
            return fileID

        except BulkWriteError as e:
            return None

    # Obtem arquivos grandes
    def getLargeData(self, name):
        try:
            fs = gridfs.GridFS(self.__db)
            gridout = fs.get_last_version(name)
            model = pickle.load(gridout)
            return model

        except BulkWriteError as e:
            return None

