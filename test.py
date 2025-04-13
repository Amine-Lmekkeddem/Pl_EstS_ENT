# test_cassandra.py
from cassandra.cluster import Cluster

cluster = Cluster(["localhost"], port=9042)
try:
    session = cluster.connect()
    print(session.execute("SELECT now() FROM system.local").one())
except Exception as e:
    print(f"Error: {e}")
finally:
    cluster.shutdown()