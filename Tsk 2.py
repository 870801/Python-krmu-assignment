# library_manager/inventory.py

import json
import logging
from pathlib import Path
from .book import Book

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

CATALOG_FILE = Path("catalog.json")


class LibraryInventory:
    def __init__(self):
        self.books = []
        self.load_catalog()

    # -----------------------------
    # Book Operations
    # -----------------------------
    def add_book(self, book: Book):
        self.books.append(book)
        logging.info(f"Book added: {book.title}")
        self.save_catalog()

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return [str(book) for book in self.books]

    # -----------------------------
    # Persistence (JSON)
    # -----------------------------
    def save_catalog(self):
        try:
            data = [book.to_dict() for book in self.books]
            with open(CATALOG_FILE, "w") as f:
                json.dump(data, f, indent=4)
            logging.info("Catalog saved successfully.")
        except Exception as e:
            logging.error(f"Error saving catalog: {e}")

    def load_catalog(self):
        if not CATALOG_FILE.exists():
            logging.warning("Catalog file missing. Creating a new one.")
            self.save_catalog()
            return

        try:
            with open(CATALOG_FILE, "r") as f:
                data = json.load(f)

            for entry in data:
                self.books.append(
                    Book(entry["title"], entry["author"], entry["isbn"], entry["status"])
                )
            logging.info("Catalog loaded successfully.")

        except json.JSONDecodeError:
            logging.error("Corrupted catalog file. Resetting.")
            self.books = []
            self.save_catalog()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
