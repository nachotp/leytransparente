from .conn import DBconnection
from sklearn.cluster import DBSCAN, OPTICS
from sklearn.decomposition import PCA
import numpy as np
from datetime import datetime

class VectorClustering:

    def __init__(self):
        self.myclient = DBconnection()
        mycol = self.myclient.get_collection("conflictos")

        self.conflicts = [x for x in mycol.find({"vector": {"$exists": True}})]

    def cluster(self, algo=DBSCAN):
        vecs = np.array([conf["vector"] for conf in self.conflicts])
        pca = PCA(n_components=15).fit_transform(vecs)

        print("PCA Applied", pca.shape)

        # pca + np.random.rand(pca.shape[0], pca.shape[1])/10000

        # metric = DistanceMetric.get_metric('mahalanobis', V=np.cov(pca))

        db = algo(eps=0.00001, algorithm="brute", metric="manhattan", n_jobs=-1).fit(pca)
        labels = db.labels_
        print(labels)
        groups = {}
        print(db.get_params())
        for i in range(len(labels)):

            if labels[i] > -1:
                if labels[i] not in groups:
                    groups[labels[i]] = []

                groups[labels[i]].append(self.conflicts[i])

        clusters = list(filter(lambda x: len(x) > 1, groups.values()))

        mycol = self.myclient.get_collection("clusters")
        mycol.remove({})
        mycol.insert({
            "date": datetime.today(),
            "clusters": clusters
        })

        return [len(x) for x in clusters]
