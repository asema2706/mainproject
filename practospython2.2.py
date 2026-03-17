
from abc import ABC, abstractmethod
import pickle

def load_books():
    try:
        with open("books.pkl", "rb") as file:
            return pickle.load(file)
    except:
        return []

def save_books(books):
    with open("books.pkl", "wb") as file:
        pickle.dump(books, file)

def load_users():
    try:
        with open("users.pkl", "rb") as file:
            return pickle.load(file)
    except:
        return []

def save_users(users):
    with open("users.pkl", "wb") as file:
        pickle.dump(users, file)

class Person(ABC):
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def show_menu(self):
        pass

class Librarian(Person):
    def __init__(self, name):
        super().__init__(name)

    def add_book(self):
        title = input("Название книги: ").strip()
        author = input("Автор: ").strip()
        books = load_books()
        books.append(f"{title}|{author}|доступна")
        save_books(books)
        print("Книга добавлена!")

    def remove_book(self):
        title = input("Название книги для удаления: ").strip()
        books = load_books()
        new_books = []
        found = False
        for line in books:
            if line.strip().split("|")[0] == title:
                found = True
            else:
                new_books.append(line)
        save_books(new_books)
        if found:
            print("Книга удалена!")
        else:
            print("Книга не найдена.")

    def register_user(self):
        name = input("Имя нового пользователя: ").strip()
        users = load_users()
        users.append(name)
        save_users(users)
        print("Пользователь зарегистрирован!")

    def list_users(self):
        users = load_users()
        if users:
            print("\nСписок пользователей:")
            for i, user in enumerate(users, 1):
                print(f"{i}. {user}")
        else:
            print("Нет зарегистрированных пользователей.")

    def list_books(self):
        books = load_books()
        if books:
            print("\nСписок книг:")
            for line in books:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    print(f"- {parts[0]} ({parts[1]}) — статус: {parts[2]}")
        else:
            print("Нет книг в системе.")

    def show_menu(self):
        while True:
            print("\nМеню библиотекаря ")
            print("1. Добавить книгу")
            print("2. Удалить книгу")
            print("3. Зарегистрировать пользователя")
            print("4. Просмотреть список пользователей")
            print("5. Просмотреть список книг")
            print("6. Выйти")
            choice = input("Выберите действие: ").strip()
            if choice == "1": self.add_book()
            elif choice == "2": self.remove_book()
            elif choice == "3": self.register_user()
            elif choice == "4": self.list_users()
            elif choice == "5": self.list_books()
            elif choice == "6": break
            else: print("Неверный выбор!")

class User(Person):
    def __init__(self, name):
        super().__init__(name)

    def view_available_books(self):
        books = load_books()
        available = [f"- {parts[0]} ({parts[1]})" for line in books if (parts := line.strip().split("|")) and len(parts) == 3 and parts[2] == "доступна"]
        print("\nДоступные книги:" if available else "Нет доступных книг.")
        for book in available: print(book)

    def take_book(self):
        title = input("Введите название книги, которую хотите взять: ").strip()
        books = load_books()
        updated_books = []
        found = False
        for line in books:
            parts = line.strip().split("|")
            if len(parts) == 3 and parts[0] == title:
                if parts[2] == "доступна":
                    updated_books.append(f"{parts[0]}|{parts[1]}|выдана")
                    found = True
                    print(f"Вы взяли книгу: {title}")
                else:
                    print("Эта книга уже выдана!")
                    updated_books.append(line)
            else:
                updated_books.append(line)
        if found:
            save_books(updated_books)
        else:
            print("Книга с таким названием не найдена.")

    def show_menu(self):
        while True:
            print(f"\n=== Меню пользователя: {self.name} ===")
            print("1. Просмотреть доступные книги")
            print("2. Взять книгу")
            print("3. Выйти")
            choice = input("Выберите действие: ").strip()
            if choice == "1": self.view_available_books()
            elif choice == "2": self.take_book()
            elif choice == "3": break
            else: print("Неверный выбор!")

def main():
    print("Добро пожаловать в библиотеку!")
    role = input("Выберите роль (1 - библиотекарь, 2 - пользователь): ").strip()
    if role == "1":
        name = input("Введите ваше имя: ").strip()
        Librarian(name).show_menu()
    elif role == "2":
        name = input("Введите ваше имя: ").strip()
        User(name).show_menu()
    else:
        print("Неверный выбор роли!")

main()
