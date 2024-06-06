import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline
import MySQLdb

# Connect to MySQL database
db = MySQLdb.connect(host="localhost", user="root", passwd="Sqluser1", db="disaster_response")
cursor = db.cursor()

# Retrieve incident reports from the database
cursor.execute("SELECT id, description FROM incidents")
incidents_data = cursor.fetchall()

incident_descriptions = [incident[1] for incident in incidents_data]



vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(incident_descriptions)

num_clusters = 3
kmeans = KMeans(n_clusters=num_clusters)
kmeans.fit(X)

cluster_labels = kmeans.labels_

for incident_id, cluster_label in zip([incident[0] for incident in incidents_data], cluster_labels):
    print(f"Incident ID: {incident_id}, Cluster Label: {cluster_label}")

db.close()
