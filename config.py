import datetime
# ----------------------------------------------------------------
# GENERAL CONFIGURATION
# ----------------------------------------------------------------
SECRET_KEY = 'Awsx1Sedc2Drfv3Ftgb4Gyhn5Hujm6'
# ----------------------------------------------------------------
# JWT CONFIGURATION
# ----------------------------------------------------------------
JWT_SECRET_KEY = 'change_me'
JWT_TOKEN_LOCATION = 'headers'
JWT_REFRESH_TOKEN_VALIDITY_DAYS = datetime.timedelta(days=90)
JWT_ACCESS_TOKEN_VALIDITY_HOURS = datetime.timedelta(hours=2)

# ----------------------------------------------------------------
# MONGO DATABASE CONFIGURATION
# ----------------------------------------------------------------
# MongoDB configuration parameters
MONGODB_DB = 'test'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# ----------------------------------------------------------------
# NEO4J DATABASE CONFIGURATION
# ----------------------------------------------------------------
NEO4J_USERNAME = 'username'
NEO4J_PASSWORD = 'change_me'
GRAPHENEDB_URL = 'http://localhost:7474'
