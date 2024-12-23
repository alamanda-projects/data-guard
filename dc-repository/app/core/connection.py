# # # =======================
# # # Project : Data Contract Repository 2.0
# # # Author  : Hani Perkasa
# # # File    : app/core/connection.py
# # # Function: connection to db / bucket / anything
# # # =======================

from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

string_connection = config("MONGODB_HOST")
db = config("MONGODB_DB")
col_dcr = config("MONGODB_COLLECTION_DCR")
col_usr = config("MONGODB_COLLECTION_USR")
# db_usr = config("MONGODB_DB_USR")

client = AsyncIOMotorClient(string_connection)
database = client[db]
# database_usr = client[db_usr]
