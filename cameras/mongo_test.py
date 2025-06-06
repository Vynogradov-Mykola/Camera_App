from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['test_db']
collection = db['test_collection']


def insert_document(data):
    """Створення нового документа"""
    result = collection.insert_one(data)
    return str(result.inserted_id)


def find_document(document_id):
    """Пошук документа за ID"""
    result = collection.find_one({'_id': ObjectId(document_id)})
    if result:
        result['_id'] = str(result['_id'])
    return result


def update_document(document_id, updated_data):
    """Оновлення документа за ID"""
    result = collection.update_one({'_id': ObjectId(document_id)}, {'$set': updated_data})
    return result.modified_count


def delete_document(document_id):
    """Видалення документа за ID"""
    result = collection.delete_one({'_id': ObjectId(document_id)})
    return result.deleted_count


# Test
if __name__ == "__main__":
    print("Test MongoDB:")

    # 1. INSERT
    data = {"name": "Test Device", "status": "active"}
    inserted_id = insert_document(data)
    print("Inserted ID:", inserted_id)

    # 2. FIND
    doc = find_document(inserted_id)
    print("Found Document:", doc)

    # 3. UPDATE
    update_count = update_document(inserted_id, {"status": "inactive"})
    print("Updated Documents:", update_count)

    # 4. DELETE
    delete_count = delete_document(inserted_id)
    print("Deleted Documents:", delete_count)
