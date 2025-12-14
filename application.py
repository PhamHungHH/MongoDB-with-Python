from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

# 1. SETUP DATABASE CONNECTION
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["library"]
    books_collection = db["books"]
   
    # authors_collection = db["authors"] 
    print("--- Connected to MongoDB successfully ---")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)

# 2. CRUD FUNCTIONS

def create_book():
    """C: Create a new document with a relationship (ObjectId)"""
    print("\n--- ADD NEW BOOK ---")
    title = input("Enter book title: ")
    year = input("Enter publication year: ")
    author_id = input("Enter Author ID (24-character Hex String): ")

    try:
        
        author_oid = ObjectId(author_id)

        new_book = {
            "title": title,
            "published_year": year,
            "author": author_oid 
        }

        books_collection.insert_one(new_book)
        print("SUCCESS: Book added with Author ID reference.")

    except Exception as e:
        print(f"ERROR: Invalid Author ID format. It must be a hex string. {e}")

def read_books():
    """R: Read all documents"""
    print("\n--- LIST OF BOOKS ---")
    books = books_collection.find()
    
    count = 0
    for book in books:
        book_id = str(book["_id"])
        title = book.get("title", "No Title")
        year = book.get("published_year", "N/A")
        
        # Get the author ObjectId
        author_ref = book.get("author", "No Author")
        
        print(f"ID: {book_id} | Title: {title} | Author (Ref ID): {author_ref} | Year: {year}")
        count += 1
    
    if count == 0:
        print("Database is empty.")

def update_book():
    """U: Update a document by ID"""
    print("\n--- UPDATE BOOK TITLE ---")
    read_books() 
    
    book_id_str = input("\nEnter the ID of the book to update: ")
    
    try:
        obj_id = ObjectId(book_id_str)
        
        if books_collection.count_documents({"_id": obj_id}) == 0:
            print("ERROR: Book not found.")
            return

        new_title = input("Enter new title: ")
        
        books_collection.update_one(
            {"_id": obj_id},
            {"$set": {"title": new_title}}
        )
        print("SUCCESS: Book title updated.")
        
    except Exception as e:
        print(f"ERROR: Invalid ID format. {e}")

def delete_book():
    """D: Delete a document by ID"""
    print("\n--- DELETE BOOK ---")
    read_books()
    
    book_id_str = input("\nEnter the ID of the book to delete: ")
    
    try:
        obj_id = ObjectId(book_id_str)
        result = books_collection.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            print("SUCCESS: Book deleted.")
        else:
            print("ERROR: Book not found.")
            
    except Exception as e:
        print(f"ERROR: Invalid ID format. {e}")

# 3. MAIN LOOP
def main():
    while True:
        print("\n==============================")
        print("   LIBRARY APP (RELATIONAL)")
        print("==============================")
        print("1. Add a Book (Create)")
        print("2. List all Books (Read)")
        print("3. Update Book Title (Update)")
        print("4. Delete a Book (Delete)")
        print("5. Exit")
        
        choice = input("Choose an option: ")

        if choice == '1':
            create_book()
        elif choice == '2':
            read_books()
        elif choice == '3':
            update_book()
        elif choice == '4':
            delete_book()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()