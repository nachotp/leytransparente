from pymongo import *


class DBconnection:
    """
    Objeto conexión a la BD Mongo
    """
    url: str = "mongodb+srv://admin:leytransparente@leytransparente-m6y51.mongodb.net/test?retryWrites=true&w=majority"
    db: str = "leytransparente"

    def __init__(self):
        self.client = MongoClient(self.url)
        self.dbconn = self.client[self.db]

    def get_collection(self, coll):
        """
        Entrega un objeto collection de pymongo desde la base de datos
        :param coll: Nombre de la colección
        :return: Objeto collection de Pymongo
        """
        assert (coll in self.dbconn.list_collection_names()), "Collection not in Database."
        return self.dbconn[coll]

    def close(self):
        self.client.close()
