import streamlit as st
import pyodbc
import pandas as pd

# title of the app
st.title("Streamlit Database Connector")

# dropdown menu for database selection
database = st.selectbox(
     'Select a database',
     ('MySQL', 'DB2', 'Oracle'))

# text input for database connection details
if database == 'MySQL':
    host = st.text_input("MySQL Host")
    user = st.text_input("MySQL User")
    password = st.text_input("MySQL Password", type='password')
    database_name = st.text_input("MySQL Database Name")

    port = 3306  # default port for MySQL

    connection_string = f'DRIVER={{MySQL ODBC 8.0 Unicode Driver}};SERVER={host};PORT={port};DATABASE={database_name};UID={user};PWD={password}'

elif database == 'DB2':
    host = st.text_input("DB2 Host")
    user = st.text_input("DB2 User")
    password = st.text_input("DB2 Password", type='password')
    database_name = st.text_input("DB2 Database Name")

    port = 50000  # default port for DB2

    connection_string = f'DRIVER={{IBM DB2 ODBC DRIVER}};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={user};PWD={password};DATABASE={database_name}'

elif database == 'Oracle':
    host = st.text_input("Oracle Host")
    user = st.text_input("Oracle User")
    password = st.text_input("Oracle Password", type='password')
    database_name = st.text_input("Oracle Service Name")

    port = 1521  # default port for Oracle

    connection_string = f'DRIVER={{Oracle in OraHome92}};DBQ={database_name};UID={user};PWD={password}'

# button to connect to the database
if st.button("Connect to Database"):
    try:
        cnxn = pyodbc.connect(connection_string)
        st.write("Connection successful")
    except Exception as e:
        st.write("Error: ", e)

# text input for query
query = st.text_area("Enter a SQL query")

# run the query on the selected database
if st.button("Run Query"):
    try:
        df = pd.read_sql(query, cnxn)
        st.dataframe(df)
    except Exception as e:
        st.write("Error: ", e)

# close the connection
cnxn.close()