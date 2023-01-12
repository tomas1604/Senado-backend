from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json
import database.database as dbase
T = TypeVar('T')

class InterfazRepositorio(Generic[T]):
    #Constructor de la clase
    def __init__(self):
        self.db = dbase.dbConnection()
        theClass = get_args(self.__orig_bases__[0])
        self.collection = theClass[0].__name__.lower()

    #Va primero, recibe una lista
    #Trayendo el valor buscado
    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.db[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList


    #Va Segundo, recibe una lista
    #Trayendo el valor buscado
    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                laColeccion = self.db[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict) :
                x[k] = self.getValuesDBRef(x[k])
        return x

    # Va Tercero es para buscar un solo documento en las 
    # Colecciones
    def findById(self, id):
        laColeccion = self.db[self.collection]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x


    #va de cuarto transforma el argumento
    # en una lista y devuelve una lista
    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList


    #Va de Quinto transforma el obejto 
    # en lo que es
    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif  isinstance(x[attribute], dict):
                x[attribute]=self.transformObjectIds(x[attribute])
        return x

    # Va Sexto, función para buscar 
    # todo
    def findAll(self):
        laColeccion = self.db[self.collection]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    #Va de séptimo
    def update(self, id, item: T):
        _id = ObjectId(id)
        laColeccion = self.db[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    # Va de octavo
    def delete(self, id):
        laColeccion = self.db[self.collection]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}


    #Va de noveno
    def ObjectToDBRef(self, item: T):
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))

    #Va de décimo
    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item,k))
                setattr(item, k, newObject)
        return item

    # va de once
    def save(self, item: T):
        laColeccion = self.db[self.collection]
        elId = ""
        item  = self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion =  self.db[self.collection]
            delattr(item, "_id")
            item = item.__dict__
            updateItem =  {"$set":item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()
        x  = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)

    # va de doce
    def query(self, theQuery):
        laColeccion = self.db[self.collection]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data
        
    #Va de trece
    def queryAggregation(self, theQuery):
        laColeccion = self.db[self.collection]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    
 







    





  