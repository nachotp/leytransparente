from .conn import DBconnection
from sklearn.cluster import DBSCAN


class VectorClustering:

    def __init__(self):
        self.myclient = DBconnection()
        mycol = self.myclient.get_collection("conflictos")

        self.conflicts = [x for x in mycol.find({"vector": 1}, {})]

    def cluster(self, algorithm=DBSCAN):
        vecs = [conf["vector"] for conf in self.conflicts]
        db = algorithm().fit(vecs)
        labels = db.labels_

        groups = {}

        for i in range(labels):

            if labels[i] not in groups:
                groups[labels[i]] = []

            groups[labels[i]].append(self.conflicts[i])

        clusters = list(filter(lambda x: len(x) > 1, groups.values()))

        mycol = self.myclient.get_collection("clusters")
        mycol.remove({})
        # mycol.bulk_write(clusters)

        return clusters
