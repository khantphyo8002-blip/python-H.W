import mysql.connector
def connectdb():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "admin123",
        database = "POS_db"
    )
try:
    conn = connectdb()
    print("Database Connect Succefully")
except:
    print("Connection Failed")