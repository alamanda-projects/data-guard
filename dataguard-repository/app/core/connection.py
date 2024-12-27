# # # =======================
# # # Project : DataGuard Repository
# # # Author  : Alamanda Team
# # # File    : app/core/connection.py
# # # Function: Connection to any databases / storages
# # # =======================

from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

string_connection = config("MONGODB_HOST")
db = config("MONGODB_DB")
col_dgr = config("MONGODB_COLLECTION_DGR")
col_usr = config("MONGODB_COLLECTION_USR")
# db_usr = config("MONGODB_DB_USR")

client = AsyncIOMotorClient(string_connection)
database = client[db]
# database_usr = client[db_usr]
