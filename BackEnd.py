import pandas as pd
import numpy as np
df = pd.read_csv("books1.csv") # --> Change this for a different file and make the proper changes to the rest of the code.
df2 = df.set_index("Title")
class BookStore:
    def __init__(self, added_book=None, book_name=None, added_author=None, added_genre=None, added_pages=None, added_publisher=None, added_price=None): # --> initiation function
        self.__book = book_name
        self.__add_book = added_book
        self.__add_author = added_author
        self.__add_genre = added_genre
        self.__add_pgs = added_pages
        self.__add_pub = added_publisher
        self.__add_price = added_price
        self.__db = df # --> to read the file (not necessary, but I believe it's a better practice to do so)

    @staticmethod
    def search_by_name(name): # --> For searching by book name.
        n = -1
        for i in df["Title"]:
            n += 1
            if i == name:
                return f"Author\t\t\t\t\t{df['Author'].loc[n]}\nGenre\t\t\t\t\t{df['Genre'].loc[n]}\nNumber of pages\t\t\t\t" \
                       f"{df['Number of pages'].loc[n]}\nPublisher\t\t\t\t{df['Publisher'].loc[n]}\nprice\t\t\t\t\t{df['price'].loc[n]}"

    @staticmethod
    def search_by_genre(): # --> For searching by genre
        genre = input("Enter genre here: ").lower()
        n = 0
        m = 0
        for i in df["Genre"]:
            n += 1
            if i == genre:
                m += 1
                return f"{m}- \nBook: {df.iloc[n - 1, 0]}, \nAuthor: {df.iloc[n-1, 1]}, \nPrice: {df.iloc[n-1, 5]}\n"

    @staticmethod
    def search_by_author(): # --> For searching by author name
        author = input("Enter the name of the author here: ").title()
        n = 0
        m = 0
        for i in df["Author"]:
            n += 1
            if i == author:
                m += 1
                return f"{m}- \nBook: {df.iloc[n - 1, 0]}, \nGenre: {df.iloc[n - 1, 2]}, \nPrice: {df.iloc[n - 1, 5]}\n"

    @staticmethod
    def search_by_publisher(): # --> For searching by publisher
        publisher = input("Enter the name of the publisher here: ").title()
        n = 0
        m = 0
        for i in df["Publisher"]:
            n += 1
            if i == publisher:
                m += 1
                return f"{m}- \nBook: {df.iloc[n - 1, 0]}, \nAuthor: {df.iloc[n-1, 1]}, \nGenre: {df.iloc[n - 1, 2]}, \nPrice: {df.iloc[n - 1, 5]}\n"

class Librarian(BookStore):
    def __init__(self, added_book=None, book_name=None, added_author=None, added_genre=None, added_pages=None, added_publisher=None, added_price=None):
        super().__init__(added_book, book_name, added_author, added_genre, added_pages, added_publisher, added_price)
    @staticmethod
    def add(added_book, added_author=np.NaN, added_genre=np.NaN, added_pages=np.NaN, added_publisher=np.NaN,
                added_price=np.NaN):  # --> a function to add items to your existing database
            df = pd.DataFrame([[added_book, added_author, added_genre, added_pages, added_publisher,
                                 added_price]])  # --> This is the Data Frame that'll get added to the database
            df.to_csv("books1.csv", mode="a", index=False, header=False)  # --> This is where the appending happens

class Customer(BookStore):
    cart1 = {}
    @staticmethod
    def cart(book_name): # --> This adds to a cart.
        book_name = book_name.split(", ")
        for i in book_name:
            try:
                Customer.cart1[i] = (df[df["Title"] == i].iloc[0, 5])
            except IndexError:
                print(f"{i} Not found, check case (lower/upper), punctuation and spelling")

    @staticmethod
    def check_out(): # --> This finalizes the cart and checks out.
        for j in Customer.cart1:
            print(f"{j}: {Customer.cart1[j]} EGP")
        return f"Total: {sum(Customer.cart1.values())}EGP\nThanks for your purchase :D"

# The idea behind the list and the if conditional is that, if I just check inside the for loop for the book, only one will print out the information and the rest will say that the book doesn't exist
# This way makes it possible to tell the user that the book they're looking for doesn't exist after it looks through the entire database.
def work():
    desire = input("Search(s), Buy(b)\n").lower()
    if desire == "b":
        Customer.cart(input("please enter the name of the book(s) you want, separate them with a comma:\n"))
        print(Customer.check_out())
    elif desire == "s":
        def search():
            how = input("Search by\nAuthor name(a), Book name(b), Genre(g), Publisher(p)\n").lower()
            if how == "a": print(BookStore.search_by_author())
            elif how == "b":
                name = input("Enter the name of the book here: ")
                book = BookStore.search_by_name(name)
                print(book)
                def purchase():
                    buy = input(f"Do you want to buy {name}? (y/n)\n").lower()
                    if buy == "y":
                        other = input("Anything else? (y/n)\n").lower()
                        if other == "n":
                            Customer.cart(name)
                            print(Customer.check_out())
                            print("Thanks for your purchase")
                        elif other == "y":
                            Customer.cart1[name] = df[df["Title"] == name].iloc[0, 5]
                            Customer.cart(
                                input("please enter the name of the book(s) you want, separate them with a comma:\n"))
                            print(Customer.check_out())
                    elif buy == "n":
                        print("Hope you had a good time with your friend :D")
                    else:
                        print("Enter a proper response")
                        purchase()
                purchase()
            elif how == "g": print(BookStore.search_by_genre())
            elif how == "p": print(BookStore.search_by_publisher())
            else: print("Please enter a proper response"); search()
        search()
    else:
        print("Please enter a proper response")
        work()
work()