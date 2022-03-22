import cx_Oracle

username = "morph3_svc"
password = "Password123!" # Obtain password string from a user prompt or environment variable
target   = "1.3.3.7/foobar"

# String dbURL = "jdbc:oracle:file_server:@localhost:1521:foobar";


connection = cx_Oracle.connect(user=username, password=password, dsn=target, encoding="UTF-8")


cursor = connection.cursor()

print("[+] Databases ")
sql_query = "SELECT DISTINCT owner FROM all_tables"
for result in cursor.execute(sql_query):
    print(result)


print("[+] Tables ")
sql_query = "SELECT table_name FROM all_tables"
for result in cursor.execute(sql_query):
    print(result)

print("[+] Dumping users table")
sql_query = "select * from users"
for result in cursor.execute(sql_query):
    print(result)


connection.commit()

