import datetime
# ----------------------------------------------------------------
# GENERAL CONFIGURATION
# ----------------------------------------------------------------
SECRET_KEY = 'Awsx1Sedc2Drfv3Ftgb4Gyhn5Hujm6'
# ----------------------------------------------------------------
# JWT CONFIGURATION
# ----------------------------------------------------------------
JWT_SECRET_KEY = 'Awsx1Sedc2Drfv3Ftgb4Gyhn5Hujm6'
JWT_TOKEN_LOCATION = 'headers'
JWT_REFRESH_TOKEN_VALIDITY_DAYS = datetime.timedelta(days=90)
JWT_ACCESS_TOKEN_VALIDITY_HOURS = datetime.timedelta(hours=2)

# ----------------------------------------------------------------
# MONGO DATABASE CONFIGURATION
# ----------------------------------------------------------------
# MongoDB configuration parameters

MONGODB_DB = 'thrive-piedad'
MONGODB_HOST = 'ds159344.mlab.com'
MONGODB_PORT = 59344
MONGODB_USERNAME = 'piedad'
MONGODB_PASSWORD = 'Wstinol123.'


# ----------------------------------------------------------------
# NEO4J DATABASE CONFIGURATION
# ----------------------------------------------------------------
NEO4J_SERVER = "subverticgraph.centralus.cloudapp.azure.com:7687"
NEO4J_USERNAME = 'neo4j'
NEO4J_PASSWORD = 'Awsx1Sedc2Drfv34'
DATABASE_URL = "bolt://" + NEO4J_USERNAME + ":" + NEO4J_PASSWORD + "@" + NEO4J_SERVER


