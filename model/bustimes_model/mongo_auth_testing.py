from pymongo import MongoClient

uri = "mongodb://admin:admin@localhost:27017/?authSource=admin"
client = MongoClient(uri)

try:
    client.admin.command("ping")
    print("✅ Authentication successful!")
except Exception as e:
    print(f"❌ Authentication failed: {e}")

