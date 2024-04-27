from pymongo import MongoClient

def init_db():
    client = MongoClient('localhost', 27017)
    db = client['recommendation_system']

    db.create_collection('users')
    db.create_collection('songs')
    db.create_collection('books')
    db.create_collection('movies')

    print("Database and collections created!")

if __name__ == "__main__":
    init_db()
