import pyodbc
from model.admin_user import adminUser

DB_Host = "127.0.1"
DB_Name = "GroupBuy"
DB_User = "user"
DB_Password = "getdata"

def initDb():
    print("Connecting to database using pyodbc...")

    db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + DB_Host + '; DATABASE=' + DB_Name + '; UID=' + DB_User + '; PWD=' + DB_Password)

    print("Succesfully Connected to database using pyodbc!")

    return db


def insertAdminUser(db,adminUserData):
    cursor = db.cursor()
    data = (adminUserData.user_id,adminUserData.user_name)
    cursor.execute("insert into dbo.admin_user (user_id, user_name) values (?, ?)", data)
    db.commit()
    print("intset success")
    

# def getAllBook(db):
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM dbo.book')
#     print("query success ,result =>")
#     data = []
#     for row in cursor:
#         print(row)
#         book = Book(row)
#         data.append(book)
#     return data
    
# def findBookByBookId(db,id):
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM dbo.book WHERE id = ?",id)
#     row = cursor.fetchone()
#     print("query success ,result =>")
#     print(row)
#     if row == None:
#         return None
#     book = Book(row)
#     return book

# def deleteBookById(db,id):
#     cursor = db.cursor()
#     deleted =cursor.execute("DELETE FROM dbo.book where id = ?",id)
#     print("delete data book")
#     print("id =>" + str(id))
#     db.commit()

# def updateBook(db, book):
#     cursor = db.cursor()
#     cursor.execute("""UPDATE dbo.book 
#                    SET book_number = ?, 
#                    book_type = ?, 
#                    book_name = ?, 
#                    book_prize = ?,
#                    book_publisher = ?,
#                    author = ? 
#                    where id = ?"""
#                    ,book.book_number
#                    ,book.book_type
#                    ,book.book_name
#                    ,book.book_prize
#                    ,book.book_publisher
#                    ,book.author
#                    ,book.id)
#     print("update success ,book id => " + str(book.id))
#     db.commit()