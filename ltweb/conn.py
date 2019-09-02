from pymongo import *

def connection():
    coll = {}
    myclient = MongoClient("mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites"
                           "=true&w=majority")
    mydb = myclient["leytransparente"]
    coll["decl"] = mydb["declaraciones"]
    coll["leyes"] = mydb["leyes"]
    coll["cats"] = mydb["categorias"]
    coll["confl"] = mydb["conflictos"]
    return coll