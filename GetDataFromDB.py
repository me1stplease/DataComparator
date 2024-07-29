import csv
import ibm_db  # for DB2
import mysql.connector  # for MySQL
import psycopg2  # for PostgreSQL
import cx_Oracle  # for Oracle

def connect_to_db(db_type, host, port, username, password, dbname):
    if db_type == 'db2':
        conn_str = f"DATABASE={dbname};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"
        conn = ibm_db.connect(conn_str, "", "")
    elif db_type == 'mysql':
        conn = mysql.connector.connect(host=host, port=port, user=username, password=password, database=dbname)
    elif db_type == 'postgres':
        conn = psycopg2.connect(host=host, port=port, user=username, password=password, dbname=dbname)
    elif db_type == 'oracle':
        conn = cx_Oracle.connect(f"{username}/{password}@{host}:{port}/{dbname}")
    return conn

def execute_query(conn, query):
    if isinstance(conn, ibm_db.Connection):
        stmt = ibm_db.exec_immediate(conn, query)
        result = ibm_db.fetch_assoc(stmt)
        data = []
        while result:
            data.append(list(result.values()))
            result = ibm_db.fetch_assoc(stmt)
    else:
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
    return data

def generate_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([desc[0] for desc in data[0].cursor_description])  # header row
        writer.writerows(data)

# Example usage:
db_type = 'db2'  # or 'mysql', 'postgres', 'oracle'
host = 'localhost'
port = 50000  # or 3306 for MySQL, 5432 for PostgreSQL, 1521 for Oracle
username = 'your_username'
password = 'your_password'
dbname = 'your_database'
query = 'SELECT * FROM your_table'

conn = connect_to_db(db_type, host, port, username, password, dbname)
data = execute_query(conn, query)
generate_csv(data, 'output.csv')