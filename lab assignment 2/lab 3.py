import json
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(filename="library.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Task 1: Book Class
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.is_available():
            self.status = "issued"
            logging.info(f"Issued book: {self.title}")
            return True
        else:
            logging.warning(f"Attempted to issue unavailable book: {self.title}")
            return False

    def return_book(self):
        self.status = "available"
        logging.info(f"Returned book: {self.title}")

    def is_available(self):
        return self.status == "available"


# Task 2: LibraryInventory Class
class LibraryInventory:
    def __init__(self, file_path="books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        logging.info(f"Added book: {book.title}")
        self.save_books()

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_isbn(self, isbn):
        return [book for book in self.books if book.isbn == isbn]

    def display_all(self):
        if not self.books:
            print("No books in the inventory.")
        for book in self.books:
            print(book)

    # Task 3: File Persistence
    def save_books(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump([book.to_dict() for book in self.books], f, indent=4)
            logging.info("Books saved to JSON file.")
        except Exception as e:
            logging.error(f"Error saving books: {e}")

    def load_books(self):
        if not self.file_path.exists():
            logging.info("Books file does not exist, starting with empty inventory.")
            return
        try:
            with open(self.file_path, 'r') as f:
                books_data = json.load(f)
                self.books = [Book(**data) for data in books_data]
            logging.info("Books loaded from JSON file.")
        except json.JSONDecodeError:
            logging.error("Error decoding JSON file. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            logging.error(f"Unexpected error loading books: {e}")
            self.books = []


# Task 4: CLI Interface
def main_menu():
    inventory = LibraryInventory()

    while True:
        print("\n==== Library Inventory Manager ====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            isbn = input("Enter ISBN: ").strip()
            book = Book(title, author, isbn)
            inventory.add_book(book)
            print(f"Book '{title}' added successfully.")

        elif choice == "2":
            isbn = input("Enter ISBN of book to issue: ").strip()
            books = inventory.search_by_isbn(isbn)
            if books:
                book = books[0]
                if book.issue():
                    inventory.save_books()
                    print(f"Book '{book.title}' issued successfully.")
                else:
                    print(f"Book '{book.title}' is already issued.")
            else:
                print("Book not found.")

        elif choice == "3":
            isbn = input("Enter ISBN of book to return: ").strip()
            books = inventory.search_by_isbn(isbn)
            if books:
                book = books[0]
                book.return_book()
                inventory.save_books()
                print(f"Book '{book.title}' returned successfully.")
            else:
                print("Book not found.")

        elif choice == "4":
            inventory.display_all()

        elif choice == "5":
            search_choice = input("Search by (1) Title or (2) ISBN? ").strip()
            if search_choice == "1":
                title = input("Enter title to search: ").strip()
                results = inventory.search_by_title(title)
            elif search_choice == "2":
                isbn = input("Enter ISBN to search: ").strip()
                results = inventory.search_by_isbn(isbn)
            else:
                print("Invalid choice.")
                continue

            if results:
                for book in results:
                    print(book)
            else:
                print("No matching books found.")

        elif choice == "6":
            print("Exiting Library Inventory Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
