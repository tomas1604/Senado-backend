from pymongo import MongoClient
import json
import certifi 

ca = certifi.where()

##########################################
def loadConfigFile():
    with open('database/config.json') as f:
        data = json.load(f)
    return data

def dbConnection():
    dataConfig = loadConfigFile()
    try:
        #Conexión al mongo atlas
        client = MongoClient(dataConfig['MONGO_URI_SERVER'], tlsCAFile=ca)
        #Conexión Local
        #client = MongoClient(dataConfig['MONGO_URI_LOCAL'], dataConfig['LOCAL_PORT'])
        db = client["proyecto_ciclo_4"]
    except ConnectionError:
        print("Error de conexión con la db")
    return db