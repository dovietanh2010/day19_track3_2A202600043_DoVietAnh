from neo4j import GraphDatabase
from app.config import Config
from app.utils.logger import setup_logger

logger = setup_logger("Neo4jClient")

class Neo4jClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jClient, cls).__new__(cls)
            cls._instance.driver = GraphDatabase.driver(
                Config.NEO4J_URI, 
                auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
            )
        return cls._instance

    def close(self):
        if self.driver:
            self.driver.close()

    def query(self, cypher: str, parameters: dict = None):
        with self.driver.session() as session:
            result = session.run(cypher, parameters)
            return [record for record in result]

    def execute_write(self, cypher: str, parameters: dict = None):
        with self.driver.session() as session:
            session.run(cypher, parameters)
