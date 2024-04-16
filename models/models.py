from pymongo import MongoClient


# Get MongoDB connection details from environment variables
username = "admin"
password = "admin"
host = "mongo"
port = 27017

class Database:
    # Use environment variables for MongoDB connection in Docker
    _client_URL = MongoClient(
        f"mongodb+srv://aleksandranabozny:6q2IJGhbhseJENFz@cluster0.gd7trab.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    )
    db_name = _client_URL["PortfolyoFlask"]  # Database Name
