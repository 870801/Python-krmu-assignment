# cli/main.py

from library_manager.inventory import LibraryInventory
from library_manager.book import Book
import logging


def menu():
    inv = LibraryInventory()

    while True:
        print("\n----- Library Inventory Manager -----")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")

                inv.add_book(Book(title, author, isbn))
                print("Book added successfully.")

            elif choice == "2":
                isbn = input("Enter ISBN to issue: ")
                book = inv.search_by_isbn(isbn)

                if book and book.issue():
                    inv.save_catalog()
                    print("Book issued.")
                else:
                    print("Cannot issue. Book not found or unavailable.")

            elif choice == "3":
                isbn = input("Enter ISBN to return: ")
                book = inv.search_by_isbn(isbn)

                if book and book.return_book():
                    inv.save_catalog()
                    print("Book returned.")
                else:
                    print("Cannot return. Book not found or already available.")

            elif choice == "4":
                for b in inv.display_all():
                    print(b)

            elif choice == "5":
                title = input("Enter title to search: ")
                results = inv.search_by_title(title)
                if results:
                    for r in results:
                        print(r)
                else:
                    print("No books found.")

            elif choice == "6":
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            logging.error(f"Runtime error: {e}")
            print("Something went wrong!")


if __name__ == "__main__":
    menu()
