import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_mysql(): 
    db_config = {
            "host": os.getenv('MYSQL_HOST_NAME'),
            "port": os.getenv('MYSQL_PORT'),
            "user": os.getenv('MYSQL_USER_NAME'),
            "password": os.getenv('MYSQL_PASSWORD'),
            "database": os.getenv('MYSQL_DB_NAME')
        }
    # connection_pool = pooling.MySQLConnectionPool(pool_name="pool", pool_size=2, **db_config)
    connection_pool = pooling.MySQLConnectionPool(pool_name='pool',pool_size=10, pool_reset_session=True, **db_config)  

    return connection_pool

def get_connection(connection_pool):
    try: 
        connection = connection_pool.get_connection()
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def close_connection(connection):
    try:
        if 'connection' in locals() and connection.is_connected():
            if connection.has_unread_result():
                connection.consume_results()
            connection.close()
    except Exception as e:
        print(f"Error closing connection: {e}")