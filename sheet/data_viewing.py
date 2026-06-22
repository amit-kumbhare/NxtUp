import chromadb

# Point directly to your directory path
client = chromadb.PersistentClient(path="/home/amitk/cftracker/sheet/chroma_db")

# List your collections to find the right name
print("Collections:", client.list_collections())

# Grab your main collection (replace 'problems' with your actual collection name)
collection = client.get_collection(name="db_questions")

# Peek at the first 5 records inside the database
print(collection.peek(5))

# Check total count of successfully added items
print("Total records added:", collection.count())
