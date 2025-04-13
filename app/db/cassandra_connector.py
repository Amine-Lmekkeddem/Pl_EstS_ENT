from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from app.config import settings

def connect_to_cassandra():
    # auth_provider = None
    # if settings.CASSANDRA_USERNAME and settings.CASSANDRA_PASSWORD:
    #     auth_provider = PlainTextAuthProvider(
    #         username=settings.CASSANDRA_USERNAME,
    #         password=settings.CASSANDRA_PASSWORD
    #     )

    #cluster = Cluster([settings.CASSANDRA_HOST], port=settings.CASSANDRA_PORT)#, auth_provider=auth_provider)
    cluster = Cluster(["localhost"], port=9042)
    session = cluster.connect()
    session.set_keyspace(settings.CASSANDRA_KEYSPACE)
    return session

